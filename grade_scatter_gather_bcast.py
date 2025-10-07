"""
2. Scatter + Gather + Broadcast
Teacher scatters papers, students grade.

Teacher gathers grades back, then broadcasts results.

Everyone knows all grades, but lots of data moved.

Run: mpirun -np 4 python grade_scatter_gather_bcast.py
"""
from mpi4py import MPI
from exam_helpers import generate_assignments, grade_assignment

# Get MPI info
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


if rank == 0:
    # Teacher (root) prepares dictionary of "assignment"s
    assignments = generate_assignments(size)
else:
    assignments = None

# --- SCATTER: each rank gets one assignment --- 
my_assignment = comm.scatter(assignments, root=0)
print(f"[Rank {rank}] received assignment id={my_assignment['id']} raw_score={my_assignment['raw_score']}",flush=True)


# Sync all ranks before timing/printing
comm.Barrier()

# --- Local grading ---
my_grade = grade_assignment(my_assignment)
print(f"[Rank {rank}] gradeed assignment id={my_assignment['id']} -> {my_grade}")

# --- GATHER: collect all grades at root ---
all_grades = comm.gather({"id": my_assignment["id"], "grade": my_grade}, root=0)

# --- Root sorts and broadcasts final per-assignment grades to everyone ---
if rank == 0:
    all_grades.sort(key=lambda x: x["id"])
    
final_grades = comm.bcast(all_grades, root=0)

print(f"[Rank {rank}] final per-assignment grades via Bcast: {final_grades}")