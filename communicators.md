# MPI MODEL: 
**Single Program, Multiple Data.** - each process runs the same code but on different chunks of data.

# Communication Types

### Point-to-Point 
- `Send`: one → one.
- `Recv`: one → one.

### Collectives (group operations)

- **Broadcast (`Bcast`)**: one → all.
- **Scatter (`Scatter`)**: one → many (distinct chunks).
- **Gather (`Gather`)**: many → one (collect chunks).
- **Allgather (`Allgather`)**: many → all (everyone gets everything).
- **Reduce (`Reduce`)**: many → one with an operation.
- **Allreduce (`Allreduce`)**: like Reduce, but **everyone** gets the result.
- **Barrier (`Barrier`)**: global sync point.
