#Ground-truth cube poses from Gazebo, for debugging only.
import re
import threading

import rclpy
from geometry_msgs.msg import Pose, PoseArray, TransformStamped
from rclpy.node import Node
from tf2_msgs.msg import TFMessage

CUBE_NAME = re.compile(r'^cube_(\d+)$')


class CubeGroundTruth(Node):

    def __init__(self):
        super().__init__('cube_ground_truth')
        self.declare_parameter('gz_topic', '/world/franka_table/pose/info')
        self.declare_parameter('frame_id', 'world')
        self.declare_parameter('rate_hz', 30.0)

        try:
            import gz.transport13 as transport
            from gz.msgs10.pose_v_pb2 import Pose_V
        except ImportError as error:
            raise RuntimeError(
                'Gazebo transport Python bindings are missing; run this node '
                'inside the lab container with /opt/ros/jazzy sourced') from error

        self._lock = threading.Lock()
        self._cubes = []
        self._stamp = None

        self._poses = self.create_publisher(PoseArray, '/ground_truth/cubes', 10)
        self._tf = self.create_publisher(TFMessage, '/ground_truth/cube_tf', 10)

        self._gz = transport.Node()
        topic = self.get_parameter('gz_topic').value
        if not self._gz.subscribe(Pose_V, topic, self._on_pose_info):
            raise RuntimeError(f'Could not subscribe to Gazebo topic {topic}')

        rate = max(float(self.get_parameter('rate_hz').value), 1.0)
        self.create_timer(1.0 / rate, self._publish)
        self.get_logger().info(f'Publishing cube ground truth from {topic}')

    def _on_pose_info(self, msg):
        cubes = []
        for pose in msg.pose:
            match = CUBE_NAME.match(pose.name)
            if match is None:
                continue  # links, visuals, robot entities
            cubes.append((
                int(match.group(1)),
                pose.name,
                pose.position.x, pose.position.y, pose.position.z,
                pose.orientation.x, pose.orientation.y,
                pose.orientation.z, pose.orientation.w,
            ))
        cubes.sort(key=lambda cube: cube[0])
        with self._lock:
            self._cubes = cubes
            self._stamp = (msg.header.stamp.sec, msg.header.stamp.nsec)

    def _publish(self):
        with self._lock:
            cubes = list(self._cubes)
            stamp = self._stamp
        if stamp is None:
            return

        array = PoseArray()
        array.header.frame_id = self.get_parameter('frame_id').value
        array.header.stamp.sec, array.header.stamp.nanosec = stamp

        transforms = []
        for _, name, x, y, z, qx, qy, qz, qw in cubes:
            pose = Pose()
            pose.position.x, pose.position.y, pose.position.z = x, y, z
            pose.orientation.x, pose.orientation.y = qx, qy
            pose.orientation.z, pose.orientation.w = qz, qw
            array.poses.append(pose)

            transform = TransformStamped()
            transform.header = array.header
            transform.child_frame_id = name
            transform.transform.translation.x = x
            transform.transform.translation.y = y
            transform.transform.translation.z = z
            transform.transform.rotation = pose.orientation
            transforms.append(transform)

        self._poses.publish(array)
        message = TFMessage()
        message.transforms = transforms
        self._tf.publish(message)


def main():
    rclpy.init()
    node = CubeGroundTruth()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
