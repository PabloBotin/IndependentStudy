# Boundary Conditions

Boundary conditions (BCs) are a fundamental part of any numerical simulation, as they define how the system interacts with its surroundings. In the context of incompressible Navier-Stokes solvers, they play a crucial role in ensuring accurate and stable solutions. This chapter introduces the main types of boundary conditions used in CFD and describes how they are applied in each of the configurations considered in this notebook.

---

## 1. Types of Boundary Conditions

- **Dirichlet Boundary Condition**  
  Specifies the value of a variable at the boundary. For example, setting a fixed velocity (inflow, wall movement) or pressure at a boundary.
    - **No-Slip Condition**  
  A type of Dirichlet BC where velocity is set to zero at solid walls.

    - **Slip Condition**  
  Allows tangential velocity but prevents normal velocity at walls, often used in inviscid or simplified flow models.

- **Neumann Boundary Condition**  
  Specifies the derivative (usually normal to the boundary) of a variable. Commonly used to model outflow conditions or natural walls where flux is zero.

- **Periodic Boundary Condition**  
  Used when the domain wraps around, like in fully developed flows or repeated geometries. Variables exiting one side re-enter on the opposite side.



- **Open/Outflow Boundary**  
  Typically uses a Neumann condition for velocity and a fixed pressure (Dirichlet) to allow flow to exit freely.

---

## 2. Boundary Conditions Used per Case

### Lid-Driven Cavity

- **Top lid**: Dirichlet condition for horizontal velocity (set to lid speed), no vertical velocity (Dirichlet = 0).  
- **Other walls**: No-slip condition (Dirichlet = 0 for both velocity components).  
- **Pressure**: Neumann condition (zero-gradient) at all boundaries; pressure is anchored by setting a reference value at one point.

### Channel Flow

- **Inlet**: Dirichlet condition for velocity profile (parabolic or constant), Neumann for pressure.  
- **Outlet**: Dirichlet condition for pressure (e.g., \( p = 0 \)), Neumann for velocity.  
- **Walls**: No-slip condition for velocity, Neumann for pressure.

### Open Flow

- **Inlet**: Prescribed velocity (Dirichlet), Neumann for pressure.  
- **Outlet**: Neumann for velocity, Dirichlet for pressure.  
- **Top and bottom**: Free-slip or open boundaries depending on setup.

### Object in Open Flow

- **Object surface**: No-slip condition.  
- **Inlet/outlet**: Same as in open flow.  
- **Top and bottom**: Often treated as open (Neumann), or walls (no-slip), depending on domain size.

### Wind Turbine in Open Flow

- **Inlet**: Dirichlet velocity, Neumann pressure.  
- **Outlet**: Neumann velocity, Dirichlet pressure.  
- **Turbine surface**: No-slip boundary.  
- **Top and sides**: Open boundaries (Neumann for velocity and pressure) or symmetry/slip depending on context.

---

Let me know if you want this turned into a collapsible section for MkDocs, or if you'd like to add figures for each BC case.
