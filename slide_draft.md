
---
# MPI Presentation
## Slide 1: Motivation — Why Distributed Programming?
- Single machines hit **memory** and **compute** limits especially for modern applications.
- Need a model to:
  - **Split work** across nodes (distributed memory)
  - **Exchange results** efficiently and correctly

## Slide 2: Distributed Programming with MPI - What is MPI?
- **Message Passing Interface**: a **standard**, not a language.
- Introduced in **1991**  
- Scales from your laptop to HPC clusters
- Implementations: Open MPI, MPICH, vendor MPIs (Intel/Cray/IBM).
- Language bindings: C/C++/Fortran; Python via **mpi4py**.

---

## Slide 3: MPI Programming Model
- **SPMD**: Single Program, Multiple Data.
- Each process:
  - Has private memory
  - identified by a **rank** in a **communicator**
- You control **when/what** to communicate.

---

## Slide 4: Strengths & Limitations

**Strengths**

- Standardized & portable; excellent scalability - from your laptop to HPC clusters
- Rich collective operations; tuned by vendors.
- Works with heterogeneous nodes (CPU/GPU).

**Limitations**

- You manage data movement explicitly.
- **Deadlock** avoidance require care.

---
### Slide 5: Demo

### ADD USEFUL LINKS