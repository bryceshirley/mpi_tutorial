"""
3.
Lecturer scatters papers, students grade.

We only care about the total score → Allreduce(SUM).

Everyone gets the result directly, no extra broadcast needed.

(Efficient if only the total matters).
Run: mpirun -np 8 python 3_grade_scatter_allreduce.py
"""
from mpi4py import MPI
from exam_helpers import generate_assignments, grade_assignment

# Get MPI info
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    # Lecturer (root) prepares dictionary of "assignment"s
    assignments = generate_assignments(size)
else:
    assignments = None

# --- SCATTER: each rank gets one assignment --- 
my_assignment = comm.scatter(assignments, root=0)
print(f"[Rank {rank}] received assignment id={my_assignment['id']} raw_score={my_assignment['raw_score']}",flush=True)

# --- Local grading ---
my_grade = grade_assignment(my_assignment)
print(f"[Rank {rank}] gradeed assignment id={my_assignment['id']} -> {my_grade}")

# --- ALLREDUCE: compute average grade and distribute automatically ---
global_sum = comm.allreduce(my_grade, op=MPI.SUM)
final_average = global_sum / size
print(f"[Rank {rank}] knows class average via Allreduce: {final_average}")
