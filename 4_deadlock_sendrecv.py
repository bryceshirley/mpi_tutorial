"""
2. Deadlock Example (Recv-before-Send Circular Wait)
----------------------------------------------------

Two students wait to *receive* each other's papers before sending their own.
Since nobody sends first, both wait forever.

=> Both call Recv() before Send(), so neither side can proceed.

To run:
    mpirun -n 2 python3 4_deadlock_sendrecv.py

Try fixing it:
    - Have one process send first, then receive
    - Or use Sendrecv() to swap data safely
"""

from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size != 2:
    raise SystemExit("Please run with exactly 2 processes: mpirun -n 2 python3 deadlock_sendrecv.py")

partner = 1 - rank
data_to_send = f"Message from rank {rank}"

print(f"[Rank {rank}] waiting to receive from rank {partner}...", flush=True)

# --- Intentional Deadlock Section ---
# Both ranks try to receive first — no one has sent anything yet.
received_data = comm.recv(source=partner, tag=0)  # blocks indefinitely
print(f"[Rank {rank}] received: '{received_data}'", flush=True)

# This line is never reached
comm.send(data_to_send, dest=partner, tag=0)
print(f"[Rank {rank}] sent message, finished normally (this should never print!)", flush=True)

MPI.Finalize()
