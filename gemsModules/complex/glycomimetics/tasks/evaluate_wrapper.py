import subprocess
import os

from gemsModules.logging.logger import Set_Up_Logging
from ..services.common_api import Modification_Position


log = Set_Up_Logging(__name__)


# Path to the evaluate_wrapper.sh script which is used to run the GM/Evaluation step.
EVALUATE_WRAPPER = os.path.join(os.path.dirname(__file__), "evaluate_wrapper.sh")

# substitute for actual API types
CondensedSequence = str

# custom exception to indicate no positions found for GEMS error logic.
class NoPositionsFoundError(Exception):
    pass


def execute(parent_dir: str, pdb_filename: str) -> tuple[list[CondensedSequence], list[Modification_Position]]:
    os.chdir(parent_dir)
    
    result = subprocess.run([EVALUATE_WRAPPER, parent_dir, pdb_filename])
    if result.returncode != 0:
        raise RuntimeError(f"Error running GM/Evaluation step, return code: {result.returncode}")
    
    output_file = os.path.join(parent_dir, "available_atoms.txt")
    if not os.path.exists(output_file):
        evaluate_err_file = os.path.join(parent_dir, "evaluate.err")
        if os.path.exists(evaluate_err_file):
            with open(evaluate_err_file) as f:
                err_msg = f.read().strip()
            log.error(f"Error during GM/Evaluation step: {err_msg}, raising RuntimeError")
            raise RuntimeError(f"Error during GM/Evaluation step: {err_msg}")
        else:
            raise FileNotFoundError(f"Output file not found: {output_file}")
    
    with open(output_file) as f:
        buffer = f.read().splitlines()
    
    # If empty, We'll need to catch this somehow.
    if len(buffer) == 0:
        raise ValueError("No available modification positions found during GM/Evaluation step")

    # These next few lines are definitely a simplification.
    # Assuming there are at least 2 lines,
    if len(buffer) < 2:
        raise ValueError("Unexpected data format during GM/Evaluation step, not enough data")  
    # and there is always a condensed sequence present on the first line that is colon delimited.
    
    line_idx = 0
    condensed_sequences = []
    while (buffer[line_idx].startswith("Oligosaccharide") and ":" in buffer[line_idx]):
        condensed_sequences.append(buffer[line_idx].split(":")[1].strip())
        line_idx += 1
        
    if len(condensed_sequences) == 0:
        raise ValueError("Unexpected data format during GM/Evaluation step, missing condensed sequence")

    # Also assuming the rest of the lines are modification positions. 
    # (But, maybe you chose to place a line delimiter between the condensed sequence and the modification positions instead, for example.)
    available_atoms = buffer[line_idx:]
     
    # I can parse these into a list of Modification_Position objects and
    available_positions = []
    for line in available_atoms:
        mp = line.split('-')
        if len(mp) != 8:
            raise ValueError(f"Unexpected data format during GM/Evaluation step, invalid modification position found: {line}")
        
        available_positions.append(Modification_Position(
            Residue_Name=mp[0],
            Chain_Identifier=mp[1],
            Residue_Number=mp[2],
            Moiety_Attachment_Atom=mp[3],
            Atom_Number=mp[4],
            Residue_Name_Glycam=mp[5],
            Residue_Number_Glycam=mp[6],
            Atom_Number_Glycam=mp[7]
        ))
        
    if len(available_atoms) == 0:
        raise NoPositionsFoundError("No available modification positions found during GM/Evaluation step")
    
    # return a tuple of the condensed sequence and the available positions.
    # This involves some upstream changes in the caller handling, as well as some API additions that I would need to notice Dan of.
    return condensed_sequences, available_positions