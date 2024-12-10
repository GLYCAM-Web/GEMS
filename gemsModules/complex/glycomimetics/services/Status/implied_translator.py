#!/usr/bin/env python3
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.implied_requests import Implied_Services_Inputs
from gemsModules.common.services.each_service.implied_translator import (
    Implied_Translator,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Status_Implied_Translator(Implied_Translator):
    """Inspect the Implied_Services_Inputs to figure out if this service needs to be run, and if so, how many times.
    Bundle resulting services into a service request package list (List[AAOP]).
    """

    # there are no ways to imply this service
    def process(self, input_object: Implied_Services_Inputs) -> List[AAOP]:
        return []
