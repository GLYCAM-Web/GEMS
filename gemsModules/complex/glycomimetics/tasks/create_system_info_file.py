from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging
from gemsModules.systemoperations.environment_ops import is_GEMS_live_swarm


log = Set_Up_Logging(__name__)


def execute(project_dir: Path, GlycoWebtool_Path: Path):
    """
    
    Ex. From Harper host:
    ```
    installPath=/programs/glycomimeticsWebtool
    AMBERHOME=/cm/shared/apps/amber20/ 
    GEMSHOME=$installPath/internal/
    ```
    """
    
    log.debug(f"Creating system info file in {project_dir}")
    
    system_info_file = project_dir / "systemInfo.txt"
    
    # Note: Only valid on Harper at the moment.
    # TODO: Manage GlycoWebtool path with IC?
    with open(system_info_file, 'w') as f:
        f.write(f"installPath={GlycoWebtool_Path}\n")
        if is_GEMS_live_swarm(): 
            f.write("AMBERHOME=/cm/shared/apps/amber20/\n")
        else:
            f.write("AMBERHOME=/programs/amber/\n")
        f.write("GEMSHOME=$installPath/internal/\n")
    
    return system_info_file