#!/usr/bin/env python
"""
4.
Teacher scatters papers, students grade.

We only care about the total score → Allreduce(SUM).

Everyone gets the result directly, no extra broadcast needed.

(Efficient if only the total matters).
Run: mpirun -np 4 python /home/dnz75396/mpi_example/grade_scatter_allreduce.py
"""
from mpi4py import MPI
from exam_helpers import generate_assignments, grade_assignment


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# --- Teacher prepares assignments ---
if rank == 0:
    assignments = generate_assignments(size)
else:
    assignments = None

# --- SCATTER: each rank gets one assignment ---
my_assignment = comm.scatter(assignments, root=0)
print(f"[Rank {rank}] received assignment id={my_assignment['id']} raw_score={my_assignment['raw_score']}")

# --- Local grading ---
my_grade = grade_assignment(my_assignment)
print(f"[Rank {rank}] gradeed assignment id={my_assignment['id']} -> {my_grade}")

# --- ALLREDUCE: compute average grade and distribute automatically ---
global_sum = comm.allreduce(my_grade, op=MPI.SUM)
final_average = global_sum / size
print(f"[Rank {rank}] knows class average via Allreduce: {final_average}")

# Explicitly finalize MPI (optional in mpi4py, but good for clarity)
MPI.Finalize()
