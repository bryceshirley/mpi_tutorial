# MPI Demos

This directory contains simple examples demonstrating **MPI (Message Passing Interface)** using Python’s `mpi4py` library.
Each file includes a docstring showing the command needed to run the demo.

A presentation explaining the concepts behind these examples is available in **`MPI_presentation.pdf`**.

## Setup

Suggested setup with Python virtual environment (ensure python is installed):

```bash
python -m venv mpi-env
source mpi-env/bin/activate  # On Windows: mpi-env\Scripts\activate
pip install mpi4py
```

## Running

Each demo includes its own docstring with the exact command to run it.
In general, you can execute any demo using:

```bash
mpiexec -n <num_processes> python <demo_file>.py
```

Example:

```bash
mpiexec -n 4 python 1_grade_sendrecv.py
```

### Demo Overview

* **Point-to-Point Communication:**
  `1_grade_sendrecv.py`

* **Collective Communication:**
  `2_grade_scatter_gather_bcast.py`, `3_grade_scatter_allreduce.py`

* **Deadlock Examples:**
  `4_deadlock_sendrecv.py`, `5_deadlock_fixed_order.py`, `6_deadlock_fixed_sendrecv.py`

Ensure that an MPI implementation (e.g. OpenMPI or MPICH) is installed on your system.

---

**Authors:** Bryce Shirley and Maciej Kaczorek
