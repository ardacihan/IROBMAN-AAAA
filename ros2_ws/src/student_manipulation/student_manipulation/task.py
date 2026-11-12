import os
from dataclasses import dataclass, field
from enum import Enum, auto

import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node
from rclpy.parameter import Parameter

from .types import ExecutionResult, Grasp, ObjectEstimate, Place


class TaskState(Enum):
    """States of one complete cube-placement run."""
    INIT = auto()
    PERCEIVE = auto()
    PLAN_TASK = auto()
    COMPUTE_GRASP = auto()
    PLAN_PICK = auto()
    EXEC_PICK = auto()
    APPROACH = auto()
    CLOSE_GRIPPER = auto()
    ATTACH = auto()
    LIFT = auto()
    PLAN_PLACE = auto()
    EXEC_PLACE = auto()
    DESCEND = auto()
    OPEN_GRIPPER = auto()
    DETACH = auto()
    RETREAT = auto()
    VERIFY = auto()
    DONE = auto()
    FAILED = auto()


@dataclass
class Slot:
    """One target cube position, with a stable id."""
    id: str                    # e.g. "tower_a_bottom"
    label: str                 # colour expected in this slot, e.g. "red"
    pose: PoseStamped          # desired cube centre in world
    level: int = 0             # 0 = bottom of a tower


@dataclass
class Assignment:
    object_id: str             # ObjectEstimate.id to pick
    slot_id: str               # Slot.id to fill


@dataclass
class TaskPlan:
    assignments: list[Assignment] = field(default_factory=list)
    next_index: int = 0

    def current(self) -> Assignment | None:
        """Return the transfer currently being executed, if any."""
        if self.next_index >= len(self.assignments):
            return None
        return self.assignments[self.next_index]

    def advance(self) -> None:
        """Mark the current transfer as complete."""
        self.next_index += 1


def plan_task(objects: list[ObjectEstimate], slots: list[Slot],
              placed: frozenset[str] = frozenset()) -> TaskPlan:
    raise NotImplementedError


def next_state(state: TaskState, ok: bool) -> TaskState:
    raise NotImplementedError


class TaskNode(Node):

    def __init__(self):
        # Simulation time in the simulator container, wall-clock time on the real robot.
        sim = os.environ.get('LAB_MODE', 'sim') == 'sim'
        super().__init__('student_task',
                         parameter_overrides=[Parameter('use_sim_time', value=sim)])
        self.state = TaskState.INIT
        self.plan = TaskPlan()
        self.grasp: Grasp | None = None
        self.place: Place | None = None
        self.objects: list[ObjectEstimate] = []
        self.last_result: ExecutionResult | None = None
        self.get_logger().info('Task skeleton is idle. Implement the FSM handlers.')

    def tick(self) -> None:
        """Advance the FSM by one non-blocking step."""
        raise NotImplementedError

    def perceive(self) -> list[ObjectEstimate]:
        """Capture one synchronized observation and return object estimates."""
        raise NotImplementedError

    def sync_scene(self) -> None:
        """Update the motion-planning scene from ``self.objects``."""
        raise NotImplementedError

    def render_plan(self) -> TaskPlan:
        """Call ``plan_task`` with the current objects and target slots."""
        raise NotImplementedError

    def compute_grasp(self) -> list[Grasp]:
        """Ask motion planning for grasp candidates for the current object."""
        raise NotImplementedError

    def compute_place(self) -> Place:
        """Ask motion planning for the place goal of the current assignment."""
        raise NotImplementedError

    def step_motion(self) -> None:
        """Plan and execute one motion segment, then update ``last_result``."""
        raise NotImplementedError

    def verify(self) -> bool:
        """Check whether the last transfer achieved its goal."""
        raise NotImplementedError


def main():
    rclpy.init()
    node = TaskNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
