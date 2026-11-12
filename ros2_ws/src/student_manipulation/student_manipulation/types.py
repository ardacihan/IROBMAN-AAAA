"""Data structures shared by the perception, planning and execution layers."""
from dataclasses import dataclass

from geometry_msgs.msg import PoseStamped, Vector3


@dataclass
class ObjectEstimate:
    id: str                    # stable unique id, e.g. "cube_red_0"
    label: str                 # colour or class, e.g. "red"
    pose: PoseStamped          # explicit frame and observation timestamp
    size: Vector3              # full extents in metres
    kind: str = 'cube'
    confidence: float = 1.0


@dataclass
class Grasp:
    object_id: str             # ObjectEstimate.id this grasp refers to
    tcp_pose: PoseStamped      # palm pose when closed (fr3_hand_tcp in this lab)
    approach: Vector3          # unit travel direction, pre-grasp -> grasp
    pre_offset_m: float = 0.10
    opening_m: float = 0.07    # total finger separation while approaching
    close_opening_m: float = 0.04  # total finger separation to command when closing
    attach_link: str = 'fr3_hand'


@dataclass
class Place:
    object_id: str             # ObjectEstimate.id being placed
    slot_id: str               # stable target slot id
    tcp_pose: PoseStamped      # palm pose when the object is released
    approach: Vector3          # unit travel direction, pre-place -> place
    pre_offset_m: float = 0.10
    opening_m: float = 0.08    # total finger separation when releasing
    detach: bool = True


@dataclass
class ExecutionResult:
    ok: bool
    reason: str = ''
    final_joint_error: float = 0.0
    measured_opening: float | None = None
