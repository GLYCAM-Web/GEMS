#!/usr/bin/env python3
from pydantic import ValidationError
from gemsModules.common.json_string_manager import Json_String_Manager
from gemsModules.complex.glycomimetics.main_settings import WhoIAm
from gemsModules.complex.glycomimetics.main_api import Glycomimetics_Transaction
from gemsModules.complex.glycomimetics.transaction_manager import (
    Glycomimetics_Transaction_Manager,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Glycomimetics_Json_String_Manager(Json_String_Manager):

    def get_local_components(self):
        self.transaction = Glycomimetics_Transaction()
        self.entityType = WhoIAm
        self.transaction_manager_type = Glycomimetics_Transaction_Manager
