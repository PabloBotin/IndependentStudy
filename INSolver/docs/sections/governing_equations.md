# Governing Equations

The **incompressible Navier-Stokes equations** are fundamental to fluid dynamics and are used to model a wide range of physical phenomena, including airflow over airplane wings, water flow through pipes, and wake formation behind wind turbines. These equations express the conservation of mass (via the continuity equation) and the conservation of momentum (via the momentum equation) within a fluid.

By assuming **incompressibility**, we neglect variations in density, an accepted assumption for many liquid flows and low-speed gas flows. This simplification reduces the complexity of the equations while still capturing the essential physics of many practical problems.

The incompressible Navier-Stokes equations consist of:
- **Mass conservation**, ensuring mass conservation
- **Momentum conservation**, derived from Newton’s second law applied to fluid motion


## Continuity equation
The continuity equation ensures the **conservation of mass** in incompressible flows. For a velocity field 
u, the equation is written as $∇⋅u= 0$ In 2D derivative form, it becomes:  $\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0$

## Momentum equations
The momentum equations describe the conservation of momentum in the fluid, considering all the forces involved. For incompressible flows, they are expressed as:
$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\frac{1}{\rho} \nabla p + \nu \nabla^2 \mathbf{u} + \mathbf{f}$. 
In 2D derivative form:

**x-Momentum:**
$$
\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} + v \frac{\partial u}{\partial y} = -\frac{1}{\rho} \frac{\partial p}{\partial x} + \nu \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\right) + F_x
$$

**y-Momentum:**
$$\frac{\partial v}{\partial t} + u \frac{\partial v}{\partial x} + v \frac{\partial v}{\partial y} = -\frac{1}{\rho} \frac{\partial p}{\partial y} + \nu \left( \frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2} \right) + F_y $$




## Challenges in Solving the Incompressible Navier-Stokes Equations

### Coupling Between Velocity and Pressure

A key challenge in solving the incompressible Navier-Stokes equations is the implicit coupling between velocity $\mathbf{u}$ and pressure $p$. Although the momentum and continuity equations appear decoupled in the incompressible form of the Navier-Stokes equations, they are physically interdependent because:

- The velocity field influences the resulting pressure distribution.
- The pressure field must ensure that the velocity field satisfies the incompressibility constraint, which is expressed by the mass conservation (continuity) equation.

This apparent decoupling gives rise to several numerical challenges:

- Since there is no explicit equation for pressure, it must be computed indirectly through the momentum and continuity equations.
- Without proper numerical treatment, the pressure-velocity relationship can become unstable, leading to artifacts such as pressure oscillations or non-physical velocity fields.


To restore the coupling between velocity and pressure and enforce incompressibility, a Poisson equation for pressure is derived from the divergence of the momentum equations. This Poisson equation acts as a surrogate for the continuity equation.

INSERT DERIVATION OR REFERENCE 2 LORENA BARBA's.


### Nonlinearity of the Momentum Equations

The convective term in the momentum equations,

$$
(\mathbf{u} \cdot \nabla)\mathbf{u}
$$

introduces nonlinearity, which significantly complicates the numerical solution. If boundary conditions, interpolations and other numerical techniques are not properly set, it can result in:

- Instabilities: Small numerical errors can grow rapidly unless stabilization techniques (e.g., upwinding or artificial diffusion) are used.
- Increased computational cost: Solving nonlinear systems often requires iterative approaches and careful time-stepping, such as the use of a CFL condition. 

---

### Boundary Conditions

Correctly specifying boundary conditions is critical for both accuracy and stability. Challenges include:

- Matching inflow and outflow conditions to avoid artificial reflections or contibuity interruption.
- Enforcing the no-slip condition on solid walls.
- Handling pressure and velocity gradients near boundaries, which may cause divergence or loss of accuracy.

---

### Discretization Challenges

Discretizing the continuous equations introduces trade-offs and numerical artifacts:

- Accuracy vs. cost: Finer grids yield better resolution but increase memory and computation time.
- Numerical diffusion: Some schemes may overly smooth the solution, hiding important flow features.
- Pressure-velocity consistency: Special care is needed to ensure that the discrete velocity field remains divergence-free, especially on collocated grids.


