"""
1. Point-to-point (Send/Recv) only
Teacher sends papers to each student, waits for results.

Problem: Teacher becomes the bottleneck (too many messages).
mpirun -n 4 python3 grade_sendrecv.py
"""
from mpi4py import MPI
from exam_helpers import generate_assignments, grade_assignment

# Get MPI info
comm = MPI.COMM_WORLD # communicator
rank = comm.Get_rank() # rank of this process
size = comm.Get_size()  # total number of processes


if rank == 0:
    # Teacher (root) prepares dictionary of "assignment"s
    assignment = generate_assignments(size)
else:
    assignment = None
print(f"[Rank {rank}] starting with assignment {assignment}",flush=True)

# # Sync all ranks before timing/printing
comm.Barrier()

# Distribute assignment via Send/Recv
if rank == 0:
    # teacher keeps assignment 0 and sends the rest
    my_assignment = assignment[0]
    for i in range(1, size):
        comm.send(assignment[i], dest=i, tag=1) # tag=1 labels a the "assignment" message
else:
    # Wait for assignment from teacher
    my_assignment = comm.recv(source=0, tag=1)

print(f"[Rank {rank}] received assignment id={my_assignment['id']} with raw_score={my_assignment['raw_score']}",flush=True)



# --- Local grading ---
my_grade = grade_assignment(my_assignment)
print(f"[Rank {rank}] graded assignment id={my_assignment['id']} -> {my_grade}",flush=True)



# --- Send grades back to teacher (manual fan-in) ---
if rank == 0:
    all_grades = [{"id": my_assignment["id"], "grade": my_grade}]

    # Receive from all other ranks
    for src in range(1, size):
        grade_info = comm.recv(source=src, tag=2) # tag=2 for grade
        all_grades.append(grade_info)
else:
    comm.send({"id": my_assignment["id"], "grade": my_grade}, dest=0, tag=2)

# Teacher prints all grades
if rank == 0:
    all_grades.sort(key=lambda x: x["id"]) # sort by assignment id
    print(f"\n[Rank {rank} Teacher] Final per-assignment grades:")
    for grade_info in all_grades:
        print(f"  assignment {grade_info['id']}: {grade_info['grade']}")


# Explicitly finalize MPI (optional in mpi4py, but good for clarity)
MPI.Finalize()