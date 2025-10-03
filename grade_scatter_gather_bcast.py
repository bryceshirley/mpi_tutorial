"""
2. Scatter + Gather + Broadcast
Teacher scatters papers, students grade.

Teacher gathers grades back, then broadcasts results.

Everyone knows all grades, but lots of data moved.

Run: mpirun -np 4 python filename.py
"""
from mpi4py import MPI
from exam_helpers import generate_assignments, grade_assignment


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# --- Teacher prepares "assigement" at root ---
if rank == 0:
    assignments = generate_assignments(size)
else:
    assigements = None

# --- SCATTER: each rank gets one assignment ---
my_assignment = comm.scatter(assignments, root=0)
print(f"[Rank {rank}] received assignment id={my_assignment['id']} raw={my_assignment['raw']}")

# --- Local grading ---
my_grade = grade_assignment(my_assignment)
print(f"[Rank {rank}] gradeed assignment id={my_assignment['id']} -> {my_grade}")

# --- GATHER: collect all grades at root ---
all_grades = comm.gather((my_assignment["id"], my_grade), root=0)

# --- Root sorts and broadcasts final per-assignment grades to everyone ---
if rank == 0:
    all_grades.sort(key=lambda x: x[0])
final_grades = comm.bcast(all_grades, root=0)

# Everyone prints the final grades they now all know
if rank != 0:
    # root already sorted/knows
    pass
print(f"[Rank {rank}] final per-assignment grades via Bcast: {final_grades}")

# Optional: purely for tidy timing/printing, not required for correctness
comm.Barrier()  # before timing or a big print
if rank == 0:
    print(f"Final per-assignment grades: {final_grades}")
