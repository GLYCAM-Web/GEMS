import json
import os, glob, shutil, socket
from pathlib import Path

# from gemsModules.logging.logger import Set_Up_Logging


# log = Set_Up_Logging(__name__)


class InstanceConfig(dict):
    """
    A class for parsing and using the instance_config.yml of the active GEMS installation.

    This class is a singleton, so it can be instantiated once and then used throughout the
    lifetime of the program.

    >>> instance_config = InstanceConfig()
    >>> instance_config.get_available_contexts('gw-grpc-delegator')


    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(InstanceConfig, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if self.__initialized:
            return
        super().__init__(*args, **kwargs)
        self.__initialized = True
        self.update(self.load())

    @staticmethod
    def load() -> dict:
        instance_config_path = Path(os.getenv("GEMSHOME", "")) / "instance_config.json"
        if not instance_config_path.exists():
            raise FileNotFoundError(
                "instance_config.yml not found at GEMSHOME: %s",
                instance_config_path,
            )

        with open(instance_config_path, "r") as f:
            instance_config = json.load(f)
        return instance_config

    def get_available_contexts(self, instance_hostname=None) -> list:
        """
        Returns a list of available contexts for the active GEMS instance.
        """
        if instance_hostname is None:
            instance_hostname = socket.gethostname()

        available_contexts = []
        for host in self["hosts"]:
            if instance_hostname in host["addresses"]:
                available_contexts.extend(host["contexts"])
        return available_contexts

    def get_possible_hosts_for_context(self, context: str) -> list:
        """
        Returns a list of possible hosts for a given context.
        """
        possible_hosts = []
        for host in self["hosts"]:
            for host_context in host["contexts"]:
                if host_context == context:
                    possible_hosts.extend(host["addresses"])
        return possible_hosts
