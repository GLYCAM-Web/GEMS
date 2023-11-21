import argparse
from pathlib import Path
import json
import sys
import os


GEMS_HOME = os.getenv("GEMSHOME")
sys.path.append(GEMS_HOME)
if GEMS_HOME is None:
    print(f"Where am I? I can't find the GEMSHOME from here {__file__}. Exiting. (1)")
    sys.exit(1)


from gemsModules.delegator.redirector_settings import (
    Known_Entity_Reception_Modules,
    DELEGATOR_CONFIG_FILE,
    BAKED_DELEGATOR_CONFIG_FILE,
)


def argparser():
    parser = argparse.ArgumentParser(description="Manage gemsModules")
    parser.add_argument("--add", help="Entity to add to config file by key")
    parser.add_argument("--remove", help="Entity to remove from config file by key")
    parser.add_argument(
        "--list", help="List all entities in config file", action="store_true"
    )

    parser.add_argument(
        "--unbake", help="Remove the baked Delegator config file", action="store_true"
    )
    parser.add_argument(
        "--bake", help="Create the baked Delegator config file", action="store_true"
    )

    return parser.parse_args()


def main():
    args = argparser()

    if os.path.isfile(DELEGATOR_CONFIG_FILE):
        with open(DELEGATOR_CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            old_config = config.copy()
    else:
        config = {}
        old_config = {}

    new_entity = args.add
    if new_entity:
        if new_entity in config:
            print(
                f"{new_entity} already exists in {DELEGATOR_CONFIG_FILE}. Exiting. (1)"
            )

        config[new_entity] = new_entity

    remove_entity = args.remove
    if remove_entity:
        if remove_entity not in config:
            print(
                f"{remove_entity} does not exist in {DELEGATOR_CONFIG_FILE}. Exiting. (1)"
            )

        del config[remove_entity]

    if args.list:
        print(json.dumps(config, indent=4))
        sys.exit(0)

    config_updated = config != old_config
    if config_updated:
        with open(DELEGATOR_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, sort_keys=True, indent=4)

    if args.unbake or config_updated:
        if os.path.isfile(BAKED_DELEGATOR_CONFIG_FILE):
            os.remove(BAKED_DELEGATOR_CONFIG_FILE)
            print(f"Removed {BAKED_DELEGATOR_CONFIG_FILE}.")

    if args.bake or config_updated:
        Known_Entity_Reception_Modules.bake()


if __name__ == "__main__":
    main()
