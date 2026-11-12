#Motion planning layer interface. Owns the MoveIt planning scene.
from dataclasses import dataclass

from geometry_msgs.msg import PoseStamped
from moveit_msgs.msg import RobotTrajectory

from .types import Grasp, ObjectEstimate, Place


@dataclass
class PlanResult:
    ok: bool
    trajectory: RobotTrajectory | None = None
    error_code: int = 0
    reason: str = ''


def sync_scene(objects: list[ObjectEstimate]) -> bool:

    raise NotImplementedError


def attach(object_id: str, link_name: str = 'fr3_hand') -> bool:
    """Attach the synced object ``object_id`` to ``link_name``.

    Call this after the gripper has closed and before planning the lift. The
    implementation must add suitable ``touch_links`` so the object may touch the
    hand and fingers without reporting a self-collision.
    """
    raise NotImplementedError


def detach(object_id: str, world_pose: PoseStamped | None = None) -> bool:
    """Detach ``object_id`` from the hand.

    If ``world_pose`` is given, re-add the object to the world there. Otherwise
    re-add it at its last attached pose, or let the next ``sync_scene`` call
    rebuild the world.
    """
    raise NotImplementedError


def grasp_candidates(obj: ObjectEstimate, *,
                     tcp_offset_m: float,
                     opening_m: float = 0.07,
                     pre_offset_m: float = 0.10) -> list[Grasp]:
    raise NotImplementedError


def place_pose(slot_id: str, object_id: str, slot_pose: PoseStamped, *,
               tcp_offset_m: float, pre_offset_m: float = 0.10,
               opening_m: float = 0.08) -> Place:
    raise NotImplementedError


def plan(goal: PoseStamped) -> PlanResult:
    raise NotImplementedError

def plan_to_grasp(grasp: Grasp) -> PlanResult:
    raise NotImplementedError


def plan_to_place(place: Place) -> PlanResult:
    raise NotImplementedError
