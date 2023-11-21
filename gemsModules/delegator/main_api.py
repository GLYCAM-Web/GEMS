#!/usr/bin/env python3
from pydantic import validator, Field, typing
from gemsModules.common import main_api, main_api_entity, main_api_services

from gemsModules.delegator.main_settings import WhoIAm
from gemsModules.delegator.services.settings.known_available import Available_Services
from gemsModules.delegator.redirector_settings import Known_Entities


from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class Delegator_Service_Request(main_api_services.Service_Request):
    typename: Available_Services = Field(
        "Delegator",
        alias="type",
        title="Services offered by Delegator Entity",
        description="The service requested of the Delegator Servicer",
    )


class Delegate_Service_Response(main_api_services.Service_Response):
    typename: Available_Services = Field(
        None,
        alias="type",
        title="Services offered by Delegator Entity",
        description="The service response from Delegator",
    )


class Delegator_Service_Requests(main_api_services.Service_Requests):
    __root__: typing.Dict[str, Delegator_Service_Request] = None


class Delegator_Service_Responses(main_api_services.Service_Responses):
    __root__: typing.Dict[str, Delegate_Service_Response] = None


class Delegator_Entity(main_api_entity.Entity):
    entityType: typing.Literal[
        "Delegator"
    ] = Field(  # This is the only required field in all of the API
        ..., title="Type", alias="type"
    )
    # Delegator overrides services so that it's own available services are used, which includes the common services too.
    services: Delegator_Service_Requests = Delegator_Service_Requests()
    responses: Delegator_Service_Responses = Delegator_Service_Responses()


# The Delegator uses the main_api.Transaction class to define the transaction
class Delegator_API(main_api.Common_API):
    entity: Delegator_Entity


class Delegator_Transaction(main_api.Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
        return Delegator_API


# The Redirector just redirects the transaction to the appropriate service module
class Redirector_Entity(main_api_entity.Entity):
    inputs: typing.Any = None
    services: typing.Any = None
    responses: typing.Any = None
    resources: typing.Any = None
    notices: typing.Any = None

    @validator("entityType")
    def checkEntityType(cls, v):
        if v not in Known_Entities.__members__.keys():
            raise ValueError(
                f"From Delegator: The requested entity, {v}, is not known. Use entity 'Delegator' and service 'KnownEntities' to get a list of known entities"
            )
        return v


class Redirector_API(main_api.Common_API):
    entity: Redirector_Entity
    project: typing.Any = None
    notices: typing.Any = None


class Redirector_Transaction(Delegator_Transaction):
    def get_API_type(self):
        return Redirector_API
