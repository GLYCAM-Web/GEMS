
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

def receive(jsonObjectString: str) -> str:
    return "I have received a string and am returning one."
