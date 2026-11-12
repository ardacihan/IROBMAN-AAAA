"""Execution layer interface."""
from moveit_msgs.msg import RobotTrajectory

from .types import ExecutionResult, Grasp, Place


def execute(trajectory: RobotTrajectory) -> ExecutionResult:
    """Execute a trajectory and evaluate completion from feedback."""
    raise NotImplementedError


def set_gripper(opening_m: float) -> ExecutionResult:
    """Command the total finger separation (0-0.08 m) and evaluate the result."""
    raise NotImplementedError


def close_gripper(grasp: Grasp) -> ExecutionResult:
    raise NotImplementedError


def open_gripper(place: Place) -> ExecutionResult:
    raise NotImplementedError
