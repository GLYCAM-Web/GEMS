#!/usr/bin/env python3
from uuid import UUID
from typing import Dict, Optional, TypeVar, Generic
from pydantic import BaseModel, Field, typing
from pydantic.generics import GenericModel

from gemsModules.common.main_api_notices import Notices
from gemsModules.common.services.settings.known_available import Available_Services

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


T = TypeVar("T")


class GenericServiceRequest(GenericModel, Generic[T]):
    class Config:
        title = "Service"

    typename: T = Field(
        "Status",
        alias="type",
        title="Common Services",
        description="The service requested of the Common Servicer",
    )
    givenName: str = Field(
        None,
        title="The name given this object in the transaction",
        description="A place for users to specify a name.",
    )
    myUuid: UUID = Field(
        None,
        title="My UUID",
        description="ID to allow correlations between services and responses.",
    )
    inputs: typing.Any = None
    options: Dict[str, str] = Field(
        None,
        description="Key-value pairs that are specific to each entity, service, etc",
    )

    def __repr__(self) -> str:
        return f"{{ {self.typename} : {self.givenName}\n\t{self.myUuid}\n\t{self.inputs=}\n\t{self.options=}\n}}"


# For the services container
class GenericServiceRequests(GenericModel, Generic[T]):
    __root__: Dict[str, GenericServiceRequest[T]] = None

    def add_service(self, key_string: str, service: GenericServiceRequest[T]):
        if self.__root__ is None:
            self.__root__ = {}
        self.__root__[key_string] = service

    def is_present(self, typename: T):
        if self.__root__ is None or self.__root__ == {}:
            return False
        the_services = self.__root__.values()
        for service in the_services:
            if service.typename == typename:
                return True
        else:
            return False


# The original Common Service Request, most entities will want to use GenericServiceRequest with their own Available_Services instead.
Service_Request = GenericServiceRequest[Available_Services]
Service_Requests = GenericServiceRequests[Available_Services]


class Service_Response(BaseModel):
    """
    Holds information about a response to a service request.
    This object will have different forms in each Entity.
    """

    typename: str = Field(
        None,
        title="Responding Service.",
        alias="type",
        description="The type service that produced this response.",
    )
    givenName: str = Field(
        None,
        title="The name given this object in the transaction",
        description="A place for users to specify a name.",
    )
    myUuid: UUID = Field(
        None,
        title="My UUID",
        description="ID to allow correlations between services and responses.",
    )
    outputs: typing.Any = None
    notices: Optional[Notices] = Notices()

    class Config:
        title = "Response"


class Service_Responses(BaseModel):
    __root__: Dict[str, Service_Response] = None

    def add_response(self, key_string: str, response: Service_Response):
        if self.__root__ is None:
            self.__root__: Dict[str, Service_Response] = {}
        self.__root__[key_string] = response

    class Config:
        title = "Responses"


def generateSchema():
    import json

    print(Service_Requests.schema_json(indent=2))


#    print(Service_Responses.schema_json(indent=2))
