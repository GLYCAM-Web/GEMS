#!/usr/bin/env python3
from gemsModules.common.code_utils import GemsStrEnum
from gemsModules.systemoperations.filesystem_ops import (
    glob_matching_gemsModules_files,
    get_parent_path,
    gemsModules_path_to_import_path,
    get_last_folder_of_path,
    get_file_path_in_parent_dir,
    file_exists,
    load_json_file,
    dump_dict_to_json_file,
    remove_file_if_exists,
)
from gemsModules.systemoperations.environment_ops import (
    is_GEMS_test_workflow,
)
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

# Exported global symbols.z
__all__ = [
    "Known_Entities",
    "Known_Entity_Reception_Modules",
]

# Enabled entities and service configuration for new-style delegator.
DELEGATOR_CONFIG_FILE = get_file_path_in_parent_dir(__file__, "known_entities.json")

# This is a generated config that contains all the Entity.receive modules that are known to delegator.
BAKED_DELEGATOR_CONFIG_FILE = get_file_path_in_parent_dir(
    __file__, "known_entities.baked.git-ignore-me.json"
)


class KERM(dict):
    """Known_Entity_Reception_Modules (KERM) dict wrapper.

    This class provides the configurable population of the KERM with automated Entity discover
    as well as the ability to bake that configuration for faster loading or production.

    There is tentative support for loading the deprecated delegator module for old Entities.

    This class delays loading of the KERM until it is accessed. This is to avoid the need to
    glob the gemsModules directory at import time unless the KERM is actually used.
    """

    def __init__(self, known_entities) -> None:
        """Initialize the KERM_Loader.

        Args:
            known_entities (GemsStrEnum): The known entities used to load the reception modules.
        """
        self.__loaded = False

        self.deprecated_delegator = None
        self.known_entities = known_entities

        super().__init__()

        # Note: Forcing rebaking in test workflows to avoid complications with known_entities.json desyncing for now.
        self.load(force_rebake=is_GEMS_test_workflow())

        # log.debug(f"Known_Entity_Reception_Modules: {self}")

    def __getitem__(self, key):
        log.debug("Known_Entity_Reception_Modules[%s] accessed.", key)

        return super().__getitem__(key)

    def load(self, force_rebake=False) -> dict:
        """Loads the KERM by loading all Entity.receive modules.

        This function will populate the global `Known_Entity_Reception_Modules` dictionary with the Entity.receive
        modules that are found in the gemsModules subpackages. It uses the `Known_Entities` GemsStrEnum to determine
        which Entity.receive modules to load.

        KERM.try_load_reception_module will use the deprecated delegator if it exists and the Entity is listed
        in `Known_Entities` as "DeprecatedDelegator". Otherwise, it will use the new-style Entity.receive module
        if it exists and the Entity is listed in `Known_Entities`. If the Entity is not listed in `Known_Entities`
        or the Entity.receive module does not exist, then it will not be added to the `Known_Entity_Reception_Modules`
        dictionary.
        """
        self.__load_deprecated_delegator()

        # Rebake the config if it doesn't exist or if force_rebake is True.
        if not file_exists(BAKED_DELEGATOR_CONFIG_FILE) or force_rebake:
            self.bake()

        # Load the baked config.
        # log.debug("Loading baked config from %s", BAKED_DELEGATOR_CONFIG_FILE)
        reception_config = load_json_file(BAKED_DELEGATOR_CONFIG_FILE)
        for entity_typename, config in reception_config.items():
            self.__try_load_reception_module(entity_typename, config)

        return self

    def bake(self) -> None:
        """Bake the KERM to a file."""
        imported_entities = self.__import_known_entities()

        if len(imported_entities):
            remove_file_if_exists(BAKED_DELEGATOR_CONFIG_FILE)

            dump_dict_to_json_file(imported_entities, BAKED_DELEGATOR_CONFIG_FILE)
            log.debug(
                "Baked Known_Entity_Reception_Modules to %s",
                BAKED_DELEGATOR_CONFIG_FILE,
            )

    def __import_known_entities(self) -> dict:
        """Use Known_Entities to find used receive modules in the gemsModules subpackages."""
        imported_entity_reception_modules = {}

        # Find all receive.py files recursively in the gemsModules subpackages.
        receive_files = glob_matching_gemsModules_files("receive.py")
        entity_paths = [get_parent_path(f) for f in receive_files]

        # This is used to populate the Known_Entity_Reception_Modules dictionary from Known_Entities.
        for (
            entity_typename,
            exact_reception_module,
        ) in self.known_entities.__members__.items():
            # Lets find all the Entity folders by looking for their receive.py files.
            for entity_path in entity_paths:
                # If the last folder of the path matches the entity name, then we have found an Entity folder.
                if (
                    get_last_folder_of_path(entity_path).lower()
                    == entity_typename.lower()
                ):
                    import_path = gemsModules_path_to_import_path(entity_path)

                    config = {
                        "exact_reception_module": exact_reception_module,
                        "import_path": f"{import_path}",
                    }
                    self.__try_load_reception_module(entity_typename, config)
                    imported_entity_reception_modules[entity_typename] = config
                    log.debug(f"Loaded {entity_typename} from {import_path}")
                    break

        return imported_entity_reception_modules

    def __load_deprecated_delegator(self):
        """Attempts to load the deprecated delegator.

        Returns true if the deprecated delegator is loaded successfully, false otherwise.
        """

        if self.deprecated_delegator is None:
            try:
                # Attempt import of deprecated delegator.
                self.deprecated_delegator = __import__(
                    "gemsModules.deprecated.delegator.receive",
                    fromlist=["delegate"],
                )

                # To make deprecated delegator work we need to expose the delegate function as receive.
                setattr(
                    self.deprecated_delegator,
                    "receive",
                    self.deprecated_delegator.delegate,
                )
            except ModuleNotFoundError as mod_exc:
                log.warning(
                    "Could not import deprecated delegator reception module: %s",
                    mod_exc,
                )
                return False

            self["DeprecatedDelegator"] = self.deprecated_delegator

        return True

    def __try_load_reception_module(self, entity_typename, entity_config) -> bool:
        """Try to load a reception module for an Entity.

        Returns True if successful, False otherwise.
        """
        exact_reception_module = entity_config["exact_reception_module"]
        import_path = entity_config["import_path"]

        # For now, if the value in Known_Entities is "DeprecatedDelegator" and there exists a valid
        # entity in the gemsModules.deprecated package, then use the deprecated delegator.
        if "deprecated" in import_path:
            log.debug(
                f"Found deprecated {entity_typename} in Known_Entities. Using deprecated delegator."
            )
            # Lets use the deprecated delegator for an old-style Entity.
            if exact_reception_module == "DeprecatedDelegator":
                self[entity_typename] = self.deprecated_delegator
                log.debug(
                    f"Added deprecated {entity_typename} to Known_Entity_Reception_Modules"
                )
                return True
            else:
                # strip the deprecated from the import path to try to import a new-style Entity.receive module. (Will only work if same name)
                import_path = import_path.replace("deprecated.", "")

        # Lets try to import a new-style Entity.receive module if we haven't already used the deprecated delegator.
        if entity_typename not in self:
            # select the correct reception module if the entity_typename is not the same as the exact_reception_module
            if (
                exact_reception_module != entity_typename
                and exact_reception_module != "DeprecatedDelegator"
            ):
                # replace the entity_typename with the exact_reception_module in the import_path
                import_path = import_path.replace(
                    entity_typename, exact_reception_module
                )
            try:
                # Lets import a new-style Entity.receive module.
                reception_module = __import__(
                    f"gemsModules.{import_path}.receive", fromlist=["receive"]
                )

                self[entity_typename] = reception_module
                log.debug(f"Added {entity_typename} to Known_Entity_Reception_Modules")
                return True

            except ModuleNotFoundError as mod_exc:
                log.error(
                    "Could not import reception module for %s: %s",
                    entity_typename,
                    mod_exc,
                )


# This is a GemsStrEnum that contains all the Entities that are known to delegator.
Known_Entities = GemsStrEnum.from_json_file(DELEGATOR_CONFIG_FILE)
# This is a dictionary that contains all loaded Entity.receive modules that are known to delegator.
Known_Entity_Reception_Modules = KERM(Known_Entities)
