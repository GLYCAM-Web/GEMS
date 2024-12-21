from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging

from ..services.common_api import Modification_Position

log = Set_Up_Logging(__name__)


def execute(position: Modification_Position, project_dir: Path, GlycoWebtool_Path): # , libraries: list, charge: int):
    """ Constructs and writes the input file for the Glycomimetics service.
    
    Ex.
    
    ```
    ComplexPdb:cocomplex.pdbqt
    OpenValence:3_A_O4_H4-/programs/glycomimetic/library/test1-pdbqt  
    naturalCharge:-1
    ```
    """
    if position is None:
        raise RuntimeError("No valid Position selected.")
    
    # TODO: Libraries from API Something like this maybe? 
    #   libraries_str = "-".join([str(GW_Path / "/library/{lib}") for lib in position.Moiety_Library_Names])
    # This is based off an example input from the GM Webtool.
    libraries_str = str(GlycoWebtool_Path / "library/test1-pdbqt")
    # TODO: Charge from... Ask Yao/Oliver 
    charge_str = "-1"
    
    # Glycomimetics input file format is two lines:
    complex_str = "ComplexPdb:cocomplex.pdbqt"
    #open_valence = f"OpenValence:{position.Residue_Identifier}_{position.Chain_Identifier}_{position.Attachment_Atom}_{position.Replaced_Atom}-{libraries_str}"
    open_valence = f"OpenValence:{position.Residue_Number_Glycam}_{position.Chain_Identifier}_{position.Moiety_Attachment_Atom}-{position.Atom_Number_Glycam}-{libraries_str}"
    natural_charge = f"naturalCharge:{charge_str}"
    
    # warn if the input file already exists
    if (project_dir / "input.txt").exists():
        log.warning(f"Warning: {project_dir}/input.txt already exists. Overwriting.")
            
    with open(Path(project_dir) / "input.txt", "w") as f:
        f.write(f"{complex_str}\n{open_valence}\n{natural_charge}\n")