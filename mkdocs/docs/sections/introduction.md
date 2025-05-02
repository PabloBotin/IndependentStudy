# Introduction

**Fluid dynamics** plays an important role in understanding natural phenomena and designing engineering systems. From the flow of air around an airplane wing to the movement of water in rivers, the behavior of fluids is governed by a set of partial differential equations known as the **Navier-Stokes equations**.

The  **incompressible Navier-Stokes equations** are a simplified version of these equations which describe the motion of fluids with constant density. They are particularly useful for liquid flows and low-speed gas flows where density variations are negligible.

This is an **educational** module designed to help fellow CFD students learn how to build their own solvers tailored to specific flow scenarios. In this notebook, I introduce the **governing equations**, discuss the **challenges of solving them numerically**, and seek for an **efficient solver implementation**. Along the way, I compare different **grid types**, **interpolation strategies**, **discretization techniques**, **boundary conditions** and **iterative solvers** to highlight the numerical pros and cons involved. 
 
### Motivation

This project originated from a research goal: to develop a solver capable of **simulating flow in wind farms**, where the interaction between turbines and wind requires both flexibility and a fast resolution. Along the path, I tried with several different approaches:

1. **Semi-Lagrangian Projection**. I worked with a solver developed by Matthias Müller from [*Ten Minute Physics*][muller]. The method combines **semi-Lagrangian advection**, a **projection step** to enforce continuity, and an added **diffusion step** to improve stability. While useful for early testing, this approach led to results that didn’t always behave as expected, which motivated me to develop a solver from scratch using a more traditional formulation.

2. **1st Order Unsplit Euler with a collocated grid**. To better understand the fundamentals, I decided to build my own solver from scratch using [Lorena Barba’s CFD Python tutorials][barba] as a guide. This approach uses a **collocated grid** and a **specific form of the projection method**: it solves the Poisson equation first and then advects using the resulting pressure field. While the implementation helped me solidify my understanding of key numerical components, the solutions were not strictly divergence-free. This raised concerns about the method's consistency, and led me to explore a more classical formulation along with a new grid structure: Chorin’s predictor-corrector method with a staggered grid.

3. **Fractional Step Method with a staggered grid**. I then implemented a solver using [Chorin’s classic predictor–corrector algorithm][chorin], this time on a **staggered grid** structure. This formulation improved pressure–velocity coupling and ensured mass conservation more effectively. I also incorporated more advanced interpolation schemes and special boundary condition treatments to increase the solver's accuracy and flexibility.

---
[muller]: https://github.com/matthias-research/pages/blob/master/tenMinutePhysics/17-fluidSim.html "Matthias Müller's Ten Minute Physics: Fluid Simulation"
[barba]: https://github.com/barbagroup/CFDPython "Lorena Barba's CFD Python Tutorials"
[chorin]: https://math.berkeley.edu/~chorin/chorin68.pdf "A.J. Chorin (1968) – Numerical Solution of the Navier-Stokes Equations"


### Objective

This notebook is intended to be an **educational module** for other CFD students. It aims to provide a practical guide to building a flow solver from scratch by:

- Introducing the **incompressible Navier Stokes equations** and explain the numerical challenges of their resolution.   
- Present and discuss different **types of grids**, **discretization**, **numerical methods**, **boundary conditions**, **iterative solvers**...   
- Provide **reproducible code** with figures. 
- Encourage other students to **customize, extend, and adapt** these methods to their own projects. 



