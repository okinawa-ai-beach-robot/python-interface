from dataclasses import dataclass
from ..robot import RobotInterface

@dataclass
class BoxDef:
    left: float = 0.5
    top: float = 0.5
    w: float = 0.5
    h: float = 0.5
    class_name: str = "unknown"


class RobotController:
    def __init__(self):
        pass

    def update(self, robot: RobotInterface, detections: list[BoxDef] = None):
        raise NotImplementedError()

