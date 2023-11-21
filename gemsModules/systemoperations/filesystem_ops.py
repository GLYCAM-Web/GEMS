import json
import os, glob, shutil
from pathlib import Path

import gemsModules
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def get_current_working_directory() -> str:
    return os.getcwd()


def build_filesystem_path(*path_parts: str):
    """Builds an operating-system-specific path string from its parts as strings."""
    log.info("build_filesystem_path was called")
    log.debug("The path parts are: ")
    log.debug(path_parts)
    try:
        the_path = ""
        for x in path_parts:
            the_path = os.path.join(the_path, x)
        log.debug("The final path is:  >>>" + str(the_path) + "<<<")
        return the_path
    except Exception as e:
        log.error("build_filesystem_path failed with the following error:")
        log.error(e)
        raise RuntimeError


def directory_exists(Dir_Path: str) -> bool:
    return os.path.isdir(Dir_Path)


def make_directory(Dir_Path: str):
    os.mkdir(Dir_Path)


def check_make_directory(Dir_Path: str):
    Path(Dir_Path).mkdir(parents=True, exist_ok=True)


def separate_path_and_filename(File_Path: str) -> tuple[str, str]:
    this_dir, this_filename = os.path.split(File_Path)
    return this_dir, this_filename


def copy_file_from_A_to_B(A: str, B: str):
    # Make me more resilient one day
    log.info(f"copy_file_from_A_to_B was called with A={A} and B={B}.")
    shutil.copy(A, B)


def copy_all_files_from_dir_A_to_dir_B(
    A: str, B: str, follow_symlinks=True, copymode=shutil.copy
):
    log.info("copy_all_files_from_dir_A_to_dir_B was called.")
    log.debug("Directory A (source) is: " + str(A))
    log.debug("Directory B (destination) is: " + str(B))
    log.debug("follow_symlinks is :" + str(follow_symlinks))
    log.debug("The copy mode is:")
    log.debug(copymode)
    check_make_directory(B)
    try:
        src_files = build_filesystem_path(A, "*")
        for file in glob.glob(src_files):
            log.debug(file)
            copymode(file, B)
    except Exception as e:
        log.error("Unable to copy files from " + str(A) + " to " + str(B) + ".")
        log.error("Here is the exception:")
        log.error(e)
        raise RuntimeError


def copy_all_files_from_dir_A_to_dir_B_preserve_metadata(
    A: str, B: str, follow_symlinks=True
):
    log.info("copy_all_files_from_dir_A_to_dir_B_preserve_metadata was called.")
    copy_all_files_from_dir_A_to_dir_B(A, B, follow_symlinks, copymode=shutil.copy2)


def copy_dir_A_to_become_dir_B():
    pass


def copy_dir_A_inside_of_dir_B():
    pass


def replace_bash_variable_in_file(path, vars: dict[str, any]):
    """Replace a value for a bash script variable. Only works in the simplest cases."""
    # a bash var is usually set like this:  varname="varvalue"
    # so we need to replace the varname= with varname="varvalue"
    # we also need to make sure that the varvalue is quoted
    # first find the line in question
    # then split the line into two parts
    modified = False
    with open(path, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        # Just to be safe, we're not interested in lines that start with "if"
        # might as well skip comments too
        if line.strip().startswith("if") or line.startswith("#"):
            continue

        if line.startswith("export"):
            line = line[7:]
        for vname, vval in vars.items():
            if f"{vname}=" in line:
                log.debug(f"Found {vname} in {line}")
                old_val = line.split("=")[1]
                lines[i] = line.replace(old_val, f"'{vval}'\n")
                modified = True

    if modified:
        # write back lines
        with open(path, "w") as f:
            f.writelines(lines)
            return True


#
def file_exists(File_Path: str) -> bool:
    return os.path.isfile(File_Path)


def remove_file_if_exists(path):
    """Remove a file at path if it exists."""
    if os.path.isfile(path):
        os.remove(path)


def directory_exists(Dir_Path: str) -> bool:
    return os.path.isdir(Dir_Path)


def get_last_folder_of_path(path) -> str:
    """Get the last folder of path."""
    return str(Path(path).parts[-1])


def get_parent_path(path) -> str:
    """Get the parent path of path."""
    return str(Path(path).parent)


def get_relative_path(path, root=None) -> str:
    """Get the relative path of path to root or $CWD."""
    if root:
        return str(Path(path).relative_to(Path(root)))
    else:
        return str(Path(path).relative_to(Path.cwd()))


def get_file_path_in_parent_dir(path, file):
    return build_filesystem_path(get_parent_path(path), file)


def get_relative_path_to_gemsModules(path) -> str:
    """Get the relative path of path to gemsModules.

    This will fail if the path is not a subdirectory of gemsModules.
    """
    return str(Path(path).relative_to(Path(gemsModules.__path__[0])))


def path_to_import_path(path) -> str:
    """Convert a path to a Python import path."""
    return ".".join(Path(path).parts)


def gemsModules_path_to_import_path(path) -> str:
    """Convert a service path to a Python import path.

    This will fail if the path is not a subdirectory of gemsModules.
    """
    path = get_relative_path_to_gemsModules(path)
    return path_to_import_path(path)


def glob_matching_files(pattern, root, recursive=True):
    """Find all files matching pattern under root."""
    if recursive:
        pattern = f"**/{pattern}"

    return glob.glob(str(Path(root) / pattern), recursive=recursive)


def glob_matching_gemsModules_files(pattern, recursive=True):
    """Find all files matching pattern under gemsModules."""
    return glob_matching_files(pattern, gemsModules.__path__[0], recursive=True)


def dump_dict_to_json_file(dict, path):
    """Dump dict to a json file at path."""
    with open(path, "w") as f:
        json.dump(dict, f, indent=4)


def load_json_file(path):
    """Load a json file at path to a dict."""
    with open(path, "r") as f:
        return json.load(f)
