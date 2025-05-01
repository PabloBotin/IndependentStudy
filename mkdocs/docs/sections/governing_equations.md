# **Governing Equations**

The **incompressible Navier-Stokes equations** are fundamental to fluid dynamics and are used to model a wide range of physical phenomena, including airflow over airplane wings, water flow through pipes, and wake formation behind wind turbines. These equations express the **conservation of mass** (via the continuity equation) and the **conservation of momentum** (via the momentum equation) within a fluid.

By assuming **incompressibility**, we neglect variations in density—an accepted assumption for many liquid flows and low-speed gas flows. This simplification reduces the complexity of the equations while still capturing the essential physics of many practical problems.

The incompressible Navier-Stokes equations consist of:

- **Mass conservation**, ensuring mass conservation  
- **Momentum conservation**, derived from Newton’s second law applied to fluid motion

---

## **Continuity Equation**

The continuity equation ensures the **conservation of mass** in incompressible flows. For a velocity field $\mathbf{u}$, the equation is written as:

<div id="eq-continuity"></div>

\[
\nabla \cdot \mathbf{u} = 0 \tag{1}
\]

In two dimensions, this becomes:

<div id="eq-continuity-2d"></div>

\[
\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0 \tag{2}
\]

---

## **Momentum Equations**

The momentum equations describe the **conservation of momentum** in the fluid, accounting for convection, pressure, diffusion, and external forces. For incompressible flows, they are expressed as:

<div id="eq-momentum"></div>

\[
\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\frac{1}{\rho} \nabla p + \nu \nabla^2 \mathbf{u} + \mathbf{f} \tag{3}
\]

In 2D derivative form:

<div id="eq-xmomentum"></div>

**x-Momentum:**

\[
\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} + v \frac{\partial u}{\partial y} = -\frac{1}{\rho} \frac{\partial p}{\partial x} + \nu \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\right) + F_x \tag{4}
\]

<div id="eq-ymomentum"></div>

**y-Momentum:**

\[
\frac{\partial v}{\partial t} + u \frac{\partial v}{\partial x} + v \frac{\partial v}{\partial y} = -\frac{1}{\rho} \frac{\partial p}{\partial y} + \nu \left( \frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2} \right) + F_y \tag{5}
\]

---

## **Challenges in Solving the Incompressible Navier-Stokes Equations**

### **Coupling Between Velocity and Pressure**

A key challenge in solving the incompressible Navier-Stokes equations is the implicit coupling between velocity $\mathbf{u}$ and pressure $p$. Although the momentum and continuity equations appear decoupled, they are physically interdependent because:

- The **velocity field** influences the resulting **pressure distribution**.
- The **pressure field** must ensure that the **velocity field satisfies the incompressibility** constraint.

This apparent decoupling gives rise to several **numerical challenges**:

- There is no explicit **equation for pressure**, so it must be computed indirectly.
- Without proper treatment, the pressure-velocity relationship can become unstable, causing **oscillations** or **non-physical results**

To restore this coupling and enforce incompressibility, a Poisson equation for pressure can be derived from the divergence of the momentum equations. This acts as a surrogate for the continuity equation. A clear and pedagogical explanation of both the derivation of the Poisson equation and the discretization of the governing equations is provided in *CFD Python: 12 steps to Navier-Stokes* by Barba and Forsyth ([Barba & Forsyth, 2014](https://github.com/barbagroup/CFDPython)).

---

### **Nonlinearity of the Momentum Equations**

The **convective term** in the momentum equations introduces nonlinearity, which complicates the numerical solution:

<div id="eq-convective"></div>

\[
(\mathbf{u} \cdot \nabla)\mathbf{u} \tag{6}
\]

This nonlinearity leads to several numerical challenges:

- **Instabilities**: Small perturbations can grow rapidly unless stabilization techniques such as **upwinding** or **artificial diffusion** are applied.
- **Increased computational cost**: Nonlinear systems often require **iterative solvers** and **careful time-stepping**. One way to control this is by enforcing a **Courant–Friedrichs–Lewy (CFL) condition**, which limits the timestep based on local velocity and grid spacing.

---

### **Boundary Conditions**

Correctly specifying boundary conditions is critical for both **accuracy** and **stability**:

- Matching **inflow/outflow conditions** to avoid artificial reflections.
- Enforcing the **no-slip condition** on solid walls.
- Handling pressure/velocity gradients near boundaries to avoid **divergence** or **loss of accuracy**.

---

### **Discretization Challenges**

Discretizing the continuous equations introduces trade-offs:

- **Accuracy vs. cost**: Finer grids improve resolution but raise computational demand.
- **Numerical diffusion**: Some schemes may over-smooth the solution.
- **Pressure-velocity consistency**: Ensuring that the discrete velocity field remains divergence-free is essential.

These difficulties make it clear that choosing the right numerical approach is essential. All the mentioned factors will define the **stability and accuracy** of the solver. In the next chapter, we’ll look at how to turn the continuous equations into a form that we can solve cell by cell, a process called discretization.