#!/usr/bin/env python3
from typing import List, Callable
from abc import ABC, abstractmethod

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api_entity import Entity
from gemsModules.common.services.explicit_requests import (
    Explicit_Service_Request_Manager,
)
from gemsModules.common.services.service_packages_list import (
    Services_Package_List_Utilities,
)
from gemsModules.common.services.implied_requests import (
    common_Implied_Services_Request_Manager,
)
from gemsModules.common.services.default_requests import (
    common_Default_Service_Request_Manager,
)
from gemsModules.common.services.duplicate_requests import (
    common_Duplicate_Requests_Manager,
)
from gemsModules.common.services.workflow_manager import (
    common_Workflow_Manager,
)

from gemsModules.common.services.request_data_filler import common_Request_Data_Filler
from gemsModules.common.services.settings.known_available import Available_Services
from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Request_Manager(ABC):
    def __init__(self, entity: Entity):
        self.entity: Entity = entity
        # Project needs to be initialized by the project_manager.
        self.response_project: Project = None

        # TODO/Q: Do we need to keep all these aaop lists? If so, the manager that processes could be the only owners.
        self.default_aaops: List[AAOP] = []
        self.explicit_aaops: List[AAOP] = []
        self.aaop_list: List[AAOP] = []
        self.deduplicated_aaop_list: List[AAOP] = None

        self.explicit_manager_type: Callable = None
        self.unknown_manager_type: Callable = None
        self.implied_manager_type: Callable = None
        self.duplicate_manager_type: Callable = None
        self.default_manager_type: Callable = None
        self.workflow_manager_type: Callable = None
        self.data_filler_type: Callable = None
        self.available_services: List[str] = None

        self.explicit_manager = None
        self.unknown_manager = None
        self.implied_manager = None
        self.duplicate_manager = None
        self.default_manager = None
        self.workflow_manager = None
        self.data_filler = None

        self.set_local_modules()

    @abstractmethod
    def set_local_modules(self):
        self.explicit_manager_type: Callable = Explicit_Service_Request_Manager
        self.unknown_manager_type: Callable = Services_Package_List_Utilities
        self.implied_manager_type: Callable = common_Implied_Services_Request_Manager
        self.duplicate_manager_type: Callable = common_Duplicate_Requests_Manager
        self.default_manager_type: Callable = common_Default_Service_Request_Manager
        self.workflow_manager_type: Callable = common_Workflow_Manager
        self.data_filler_type: Callable = common_Request_Data_Filler
        self.available_services: List[str] = Available_Services.get_list()

    def set_response_project(self, response_project: Project):
        self.response_project = response_project

    def process(self) -> List[AAOP]:
        log.debug("Processing request for entity")

        self.set_explicit_aaops()
        self.remove_unknown_services()
        self.gather_implicit_services()
        self.manage_duplicates()
        # TODO: Resolve before duplicates.
        self.resolve_dependencies()
        
        return self.deduplicated_aaop_list

    def set_explicit_aaops(self):
        log.debug("about to set explicit aaops")

        self.explicit_manager = self.explicit_manager_type(entity=self.entity)
        self.explicit_aaops: List[AAOP] = self.explicit_manager.process()

        log.debug("the explicit aaop list is: %s", self.explicit_aaops)

    def remove_unknown_services(self):
        log.debug("about to remove unknown services")

        self.unknown_manager = self.unknown_manager_type(aaop_list=self.explicit_aaops)
        self.managed_explicit_aaops: List[
            AAOP
        ] = self.unknown_manager.manage_unknown_services(
            available_services=self.available_services
        )

        log.debug("the managed explicit aaop list is: %s", self.managed_explicit_aaops)

    def gather_implicit_services(self):
        log.debug("about to gather implicit services")

        self.implied_manager = self.implied_manager_type(input_object=self.entity)
        self.implicit_aaops: List[AAOP] = self.implied_manager.process()
        log.debug("the implicit aaop list is: %s", self.implicit_aaops)

        # ordering here doesn't really matter, dependencies will be resolved later.
        self.aaop_list = self.implicit_aaops + self.managed_explicit_aaops
        log.debug("the current aaop list is: %s", self.aaop_list)

    def resolve_dependencies(self):
        """Service Requests may have Service dependencies which need to be run first for the service to complete successfully."""
        log.debug("about to resolve dependencies")

        if self.workflow_manager_type is None:
            log.warning("No workflow manager type set, skipping dependency resolution.")
            return

        self.workflow_manager = self.workflow_manager_type(entity=self.entity)
        # self.aaop_list = self.workflow_manager.process(
        #     self.aaop_list
        # )
        #log.debug("\tthe ordered aaop request list is: %s", self.aaop_list)
        
        self.deduplicated_aaop_list = self.workflow_manager.process(
            self.deduplicated_aaop_list
        )
        
    def manage_duplicates(self):
        log.debug("about to manage duplicates")

        self.duplicate_manager = self.duplicate_manager_type(aaop_list=self.aaop_list)
        self.deduplicated_aaop_list: List[AAOP] = self.duplicate_manager.process()

        if self.deduplicated_aaop_list == []:
            self.deduplicated_aaop_list = self.get_default_aaops()

        log.debug("the current aaop list is: %s", self.deduplicated_aaop_list)

    def get_default_aaops(self) -> List[AAOP]:
        self.default_manager = self.default_manager_type()
        self.default_aaops: List[
            AAOP
        ] = self.default_manager.get_default_services_aaops()
        return self.default_aaops

    def fill_request_data_needs(self, transaction):
        log.debug("about to fill request data needs")

        self.data_filler = self.data_filler_type(
            aaop_list=self.deduplicated_aaop_list,
            transaction=transaction,
            response_project=self.response_project,
        )
        self.deduplicated_aaop_list = self.data_filler.process()
        # RDF would be able to fill dependencies better:
        # However, if we resolve here, it seems then the aoop_list is not complete by the time we start serving
        # self.resolve_dependencies()


class common_Request_Manager(Request_Manager):
    def set_local_modules(self):
        super().set_local_modules()
