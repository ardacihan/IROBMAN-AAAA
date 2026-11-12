"""Perception layer interface."""
from sensor_msgs.msg import CameraInfo, Image

from .types import ObjectEstimate


def detect(rgb: Image, depth: Image, calibration: CameraInfo,
           tf_buffer=None, target_frame: str = 'world') -> list[ObjectEstimate]:
    """Estimate labels, poses and sizes from synchronized observations.

    Every estimate must carry a unique, stable ``id`` for the duration of the
    task. The same physical cube must keep the same id across frames, because
    planning uses it for collision-object names and attached objects.
    """
    raise NotImplementedError
