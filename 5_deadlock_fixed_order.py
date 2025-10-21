"""
Fixed Deadlock Example 1: Correct Send/Recv Order
-------------------------------------------------

Fix for the "Recv-before-Send" deadlock.

Rank 0 sends first, then receives.
Rank 1 receives first, then sends.

=> Communication completes safely.
To run:
    mpirun -n 2 python3 5_deadlock_fixed_order.py
"""

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
partner = 1 - rank

data_to_send = f"Message from rank {rank}"

if rank == 0:
    print(f"[Rank {rank}] sending first...", flush=True)
    comm.send(data_to_send, dest=partner, tag=0)
    received_data = comm.recv(source=partner, tag=0)
else:
    print(f"[Rank {rank}] receiving first...", flush=True)
    received_data = comm.recv(source=partner, tag=0)
    comm.send(data_to_send, dest=partner, tag=0)

print(f"[Rank {rank}] received: '{received_data}'", flush=True)
print(f"[Rank {rank}] finished successfully!", flush=True)

MPI.Finalize()
