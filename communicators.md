# Communication Types

### Point-to-Point 
- **Blocking**: `Send`/`Recv` — completes only when it’s safe (may wait).
- **Nonblocking**: `Isend`/`Irecv` + `Wait/Test` — overlap compute/comm.

### Collectives (group operations)
- **Broadcast (`Bcast`)**: one → all.
- **Scatter (`Scatter`)**: one → many (distinct chunks).
- **Gather (`Gather`)**: many → one (collect chunks).
- **Allgather (`Allgather`)**: many → all (everyone gets everything).
- **Reduce (`Reduce`)**: many → one with op (SUM/MIN/MAX/…).
- **Allreduce (`Allreduce`)**: like Reduce, but **everyone** gets the result.
- **Barrier (`Barrier`)**: global sync point.

> Rule of thumb: prefer **collectives** for performance & correctness; use **nonblocking** to hide latency.