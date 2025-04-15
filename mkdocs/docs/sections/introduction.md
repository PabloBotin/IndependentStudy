# Introduction

**Fluid dynamics** plays an important role in understanding natural phenomena and designing engineering systems. From the flow of air around an airplane wing to the movement of water in rivers, the behavior of fluids is governed by a set of partial differential equations known as the **Navier-Stokes equations**.

The original motivation for developing this solver was to model wake formation behind wind turbines in a wind farm using a lightweight, efficient computational tool. The goal was to enable **fast 2D real-time visualizations**, with potential extension into the 3D domain. While this notebook does not focus on that specific application, it centers on the **design and implementation** of the numerical method behind the solver.

This method targets the **2D incompressible Navier-Stokes equations**, which describe the motion of fluids with constant density. These equations are particularly relevant for liquid flows and low-speed gas flows where density variations are negligible.

In this notebook, we introduce the **governing equations**, discuss the **challenges of solving them numerically**, and present an **efficient solver implementation**. Along the way, we compare different **grid types**, **interpolation strategies**, and **iterative solvers** to highlight the numerical trade-offs involved.



