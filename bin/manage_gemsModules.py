#!/usr/bin/env python3
import argparse
from pathlib import Path
import json
import sys
import os

from gemsModules.systemoperations.filesystem_ops import remove_file_if_exists

GEMS_HOME = os.environ.get("GEMSHOME")
if GEMS_HOME is None:
    print(f"Where am I? I can't find the GEMSHOME from here {__file__}. Exiting. (1)")
    sys.exit(1)


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

    # generate new entity from template


def main():
    args = argparser()
    config_path = os.path.join(
        GEMS_HOME, "gemsModules/delegator/baked_config-git-ignore.json"
    )

    if os.path.isfile(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            old_config = config.copy()
    else:
        config = {}
        old_config = {}

    # add new entity to config file
    new_entity = args.add
    if new_entity:
        if new_entity in config:
            print(f"{new_entity} already exists in {config_path}. Exiting. (1)")

        config[new_entity] = new_entity

    # remove entity from config file
    remove_entity = args.remove
    if remove_entity:
        if remove_entity not in config:
            print(f"{remove_entity} does not exist in {config_path}. Exiting. (1)")

        del config[remove_entity]

    if args.bake or args.unbake:
        from gemsModules.delegator.redirector_settings import (
            Known_Entity_Reception_Modules,
            BAKED_DELEGATOR_CONFIG_FILE,
        )

        if args.unbake:
            remove_file_if_exists(BAKED_DELEGATOR_CONFIG_FILE)

        if args.bake:
            Known_Entity_Reception_Modules.bake()

    # list all entities in config file
    if args.list:
        print(json.dumps(config, indent=4))
        sys.exit(0)

    # save if changed
    if config != old_config:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
