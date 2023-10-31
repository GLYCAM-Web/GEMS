import json, os, glob, shutil, socket
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, List, Optional, Literal
from abc import ABC, abstractmethod

from gemsModules.systemoperations.environment_ops import (
    is_GEMS_test_workflow,
    is_GEMS_live_swarm,
)

from gemsModules.logging.logger import Set_Up_Logging

from . import *


log = Set_Up_Logging(__name__)


class DateReversioner:
    """A class to check if a ConfigManger's config file is older than the updated config file.

    This class should not modify production configuratoin files. It should only run in a DevEnv.
    """

    ...


class InstanceConfig(KeyedArgManager):
    """The main GEMS class for parsing it's active instance configuration file.

    This class only has active GEMS instance specific methods and configuration.
    It inherits all it's configuration functionality.

    A class for parsing and using the instance_config.yml of the active GEMS installation.

    This class is deeply coupled with the active state of your GEMS environment.
    It has properties and methods which convey active environmental information.

    >>> instance_config = InstanceConfig()
    >>> instance_config.get_available_contexts('gw-grpc-delegator')
    """

    # Not an enum so we can extend here, in the InstanceConfig class, where the most specific GEMS instance configuration is defined.
    Contexts = ContextManager.Contexts + ["MDaaS-RunMD"]

    @staticmethod
    def get_default_path(example=False) -> Path:
        """The default path is the active GEMS instance configuration.

        TODO: change to active_path property.
        """
        name = "instance_config.json"
        if example:
            name += ".example"

        return Path(os.getenv("GEMSHOME", "")) / name

    # TODO: Context needs an enum.
    def get_keyed_arguments(
        self,
        key: KeyedArgManager.ConfigurationKeys,
        host: str = None,
        context: Contexts = None,
    ):
        if context not in self.Contexts:
            log.warning(f"Context {context} not found in {self.Contexts}.")

        if context is None:
            # TODO: Is this sensible?
            if is_GEMS_test_workflow():
                context = self.Contexts.DEV_ENV
            elif host is not None and self.Context.SWARM in self.get_available_contexts(
                host
            ):
                context = self.Contexts.SWARM

        return super().get_keyed_arguments(key, host, context)

    # specialized md cluster host helpers aka "MDaaS-RunMD" context helpers
    def get_md_filesystem_path(self) -> str:
        """Returns the filesystem path for the MD compute cluster by hostname defined in the instance config's hosts dict."""
        if (
            "md_cluster_filesystem_path" not in self.config
            or len(self.config["md_cluster_filesystem_path"]) == 0
        ):
            log.error(
                "Access attempted but MD Cluster filesystem path not set in instance_config.json."
            )

        return self.config["md_cluster_filesystem_path"]

    def set_md_filesystem_path(self, path):
        """Sets the filesystem path for the MD compute cluster by hostname defined in the instance config's hosts dict.

        You probably want to save the instance config after this.
        """
        self.config["md_cluster_filesystem_path"] = path
