"""
Fixed Deadlock Example 2: Using Sendrecv
----------------------------------------

Fix for the "both send first" or "simultaneous send/recv" deadlock.

MPI provides a combined Sendrecv() call that performs
both operations atomically and safely.

To run:
    mpirun -n 2 python3 6_deadlock_fixed_sendrecv.py
"""

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
partner = 1 - rank

data_to_send = f"Message from rank {rank}"

print(f"[Rank {rank}] safely exchanging messages with Sendrecv...", flush=True)

# Send and receive in one step — atomic, no deadlock possible
received_data = comm.sendrecv(sendobj=data_to_send,
                              dest=partner, sendtag=0,
                              source=partner, recvtag=0)

print(f"[Rank {rank}] received: '{received_data}'", flush=True)
print(f"[Rank {rank}] finished successfully!", flush=True)

MPI.Finalize()
