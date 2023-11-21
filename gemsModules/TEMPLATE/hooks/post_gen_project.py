import glob
import os
import re
import subprocess
import sys

module_name = "{{cookiecutter.gems_module}}"

# find all patterns matching `.*import ({module_name}.*)` and use those matches to capitalize the class imported
# in all files.
# for instance, f'import {module_name}_Project_Manager' should result in all usages of f'{module_name}_Project_Manager'
# being replaced with a capitalized variant
pattern = re.compile(f".*import ({module_name}\\S*)\n")

# first glob all python files in CWD
python_files = glob.glob("**/*.py", recursive=True)

class_names = []
for file in python_files:
    with open(file, "r") as f:
        buffer = f.read()
        for m in pattern.findall(buffer):
            class_names.append(m)


def capitalize_snake_case(s, sep="_"):
    return f"{sep}".join([w.capitalize() for w in s.split("_")])


# now we have a list of all class names that need to be capitalized
# we can now iterate over all files again and replace all occurrences of the class names with the capitalized variant
for file in python_files:
    with open(file, "r") as f:
        buffer = f.read()
        for class_name in class_names:
            buffer = buffer.replace(class_name, capitalize_snake_case(class_name))
    with open(file, "w") as f:
        f.write(buffer)


# Let us also add this new Entity to Delegator's known entities.
if (
    input(
        "Would you like to add this new Entity to Delegator's known entities? [y/N] "
    ).lower()
    == "y"
):
    GEMSHOME = os.getenv("GEMSHOME", "$GEMSHOME")
    add_cmd = f"python3 {GEMSHOME}/bin/manage_gemsModules.py --add {module_name} --bake"

    if GEMSHOME is None:
        print(
            "GEMSHOME is not set, skipping adding new Entity to Delegator's known entities. You may manually run:\n\n"
            f"{add_cmd}\n\n when you have set GEMSHOME."
        )
        sys.exit(0)

    result = subprocess.run(add_cmd.split(" "), env=os.environ.copy())
