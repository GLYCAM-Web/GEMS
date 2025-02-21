#!/usr/bin/env python3
from enum import Enum
from typing import List

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class GemsStrEnum(str, Enum):
    """
    A base class for all String-based Gems Enumerations.

    The additions simplify some uses of Enums that are convenient, particularly
    since our classes interact with Pydantic.
    """

    # TODO: Wait, how are these classmethods working? These look like instance getters.
    @classmethod
    def get_list(self):
        return self.get_value_list()

    @classmethod
    def get_json_list(self):
        return self.get_value_list()

    @classmethod
    def get_value_list(self):
        theList = []
        for item in self:
            theList.append(item.value)
        return theList

    @classmethod
    def get_key_list(self):
        return self.get_name_list()

    @classmethod
    def get_internal_list(self):
        return self.get_value_list()

    @classmethod
    def get_name_list(self):
        theList = []
        for item in self:
            theList.append(item.name)
        return theList

    @classmethod
    def from_lists(cls, *lists, name="Generic_GemsStrEnum"):
        """Create a new Enum class from a list of lists.

        The first item in each list is the name, and the second is the value.
        """

        init = []
        for l in lists:
            init.append((l[0], l[1]))

        return cls(name, init)


class Annotated_List(list):
    """The purpose of this class is to provide list metadata.
    The list can be ordered or unordered.  The default is ordered.
    If set to ordered, it should be assumed that the items must be
    processed in the order they are listed.  If set to unordered,
    items can be processed in any order, or in parallel, etc.
    """

    # TODO: items -> *items, calls will need to be updated - Annotated_List([1, 2, 3]) vs Annotated_List(1, 2, 3)
    def __init__(
        self,
        items: List = None,
        ordered: bool = True,
    ) -> None:
        if items:
            super().__init__(items)
        else:
            super().__init__()

        self._ordered: bool = ordered

    def add_item(self, item):
        super().append(item)

    def get_items(self):
        return super()

    @property
    def ordered(self):
        return self._ordered

    def get_ordered(self):
        return self.ordered

    def set_ordered(self, ordered):
        self._ordered = ordered

    def __iadd__(self, other):
        super().__iadd__(other)
        return self


# These may belong somewhere else
def resolve_dependency_list(service: str, Service_Dependencies: dict):
    dependencies = Service_Dependencies.get(service)
    if dependencies:
        return list(dependencies)
    return []


def find_aaop_by_id(aaop_list: List, id_string: str):
    """For general usage on list[AAOP].

    Assumes unique ID_Strings.

    Useful for accessing the requesting AAOP (AAOP.Requester if not None) by ID_String or
    it's dependent AAOPs from AAOP.Dependencies.

    S/N: I believe we could deprecate this if we rely on AAOP_Tree instead of bare AAOP lists.
    """
    for aaop in aaop_list:
        if aaop.ID_String == id_string:
            return aaop
    return None
