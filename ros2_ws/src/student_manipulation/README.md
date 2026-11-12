# Optional student workspace

The simulation does not depend on this package. Delete it, empty the modules,
or replace it with your team's package without changing the environment.

- `perception.py`: turn camera observations into labeled poses and dimensions
  with stable object ids.
- `planning.py`: motion planning. Own the MoveIt scene, build grasp/place
  goals, and return collision-free trajectories.
- `execution.py`: command the arm/gripper and evaluate feedback.
- `task.py`: task planning and FSM coordination. The supplied node only waits.

See [TYPE_DEPENDENCIES.md](TYPE_DEPENDENCIES.md) for the data flow and type
relationships between the layers.

The function signatures are suggestions, not a required architecture. All
algorithm functions raise `NotImplementedError`; no solution is implemented.
Start the idle shell with `ros2 run student_manipulation task`.
