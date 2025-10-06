"""
1. Point-to-point (Send/Recv) only
Teacher sends papers to each student, waits for results.

Problem: Teacher becomes the bottleneck (too many messages).
"""
from mpi4py import MPI
from exam_helpers import generate_assignments, grade_assignment


# Get MPI info
comm = MPI.COMM_WORLD # communicator
rank = comm.Get_rank() # rank of this process
size = comm.Get_size()  # total number of processes

# --- Teacher prepares "assignment" at root ---
if rank == 0:
    assignment = generate_assignments(size)
else:
    assignment = None

# --- Distribute assignment via Send/Recv ---
if rank == 0:
    # teacher keeps assignment 0 and sends the rest
    my_assignment = assignment[0]
    for i in range(1, size):
        comm.send(assignment[i], dest=i, tag=1) # tag=1 for assignment
else:
    # Wait for assignment from teacher
    my_assignment = comm.recv(source=0, tag=1)
print(f"[Rank {rank}] received assignment id={my_assignment['id']} raw_score={my_assignment['raw_score']}")



# --- Local grading ---
my_grade = grade_assignment(my_assignment)
print(f"[Rank {rank}] graded assignment id={my_assignment['id']} -> {my_grade}")



# --- Send grades back to teacher (manual fan-in) ---
if rank == 0:
    all_grades = [(my_assignment["id"], my_grade)]

    # Receive from all other ranks
    for src in range(1, size):
        sid, grade = comm.recv(source=src, tag=2) # tag=2 for grade
        all_grades.append((sid, grade))

    # Sort by assignment id for pretty output
    all_grades.sort(key=lambda x: x[0])
    print("\n[Teacher] Final per-assignment grades:")
    for sid, grade in all_grades:
        print(f"  assignment {sid}: {grade}")
else:
    comm.send((my_assignment["id"], my_grade), dest=0, tag=2)


# Explicitly finalize MPI (optional in mpi4py, but good for clarity)
MPI.Finalize()