# Boundary Conditions

Boundary conditions (BCs) are a fundamental component of any numerical simulation, as they define how the system interacts with its surroundings. In the context of incompressible Navier-Stokes solvers, they play a critical role in ensuring accurate and stable solutions. This chapter introduces the main types of boundary conditions used in CFD and describes how they are applied in each of the configurations considered in this notebook.

---

## 1. Types of Boundary Conditions

- **Dirichlet Boundary Condition**  
  Specifies the value of a variable at the boundary. For example, setting a fixed inflow velocity or a zero pressure at a jet. When it comes to walls, there are two commonly used boundary conditions: 
    - **No-Slip Condition**  
  A type of Dirichlet BC where velocity is set to zero at solid walls.
    - **Slip Condition**  
  Allows tangential velocity but prevents normal velocity at walls, often used in inviscid or simplified flow models.

- **Neumann Boundary Condition**  
  Specifies the derivative (usually normal to the boundary) of a variable. Commonly used to model outflow conditions or natural walls where flux is zero.

- **Periodic Boundary Condition**  
  Used when the domain wraps around, like in fully developed flows or repeated geometries. Variables exiting one side re-enter on the opposite side.

---

## 2. Differerent boundary conditions per case

### Lid-Driven Cavity

ADD BC TABLE and RESULTS. 

### Channel Flow

In this section, we explore two alternative boundary condition configurations used to model steady, incompressible flow in a 2D channel. Although the geometry remains the same, the outlet treatment differs and leads to slightly different numerical behavior.

---

### Configuration 1: Fixed Inlet Velocity

This setup imposes a uniform velocity at the inlet and fixes the pressure at the outlet to anchor the pressure field. This configuration mimics an open channel where the flow is driven by a prescribed inlet velocity and develops downstream under a pressure gradient.

<!-- 
|   Boundary   |   Type   |      Velocity Condition      |    Pressure Condition     |
|:------------:|:--------:|:----------------------------:|:-------------------------:|
|    Inlet     |  Inflow  | Uniform inflow (Dirichlet)   | Zero-gradient (Neumann)   |
|   Outlet     | Outflow  | Zero-gradient (Neumann)      | Fixed pressure (Dirichlet)|
| Top/Bottom   |  Wall    | No-slip (u = 0, Dirichlet)   | Zero-gradient (Neumann)   | -->

<div style="display: flex; justify-content: center;">

  <table>
    <thead>
      <tr>
        <th style="text-align: center;">Boundary</th>
        <th style="text-align: center;">Type</th>
        <th style="text-align: center;">Velocity Condition</th>
        <th style="text-align: center;">Pressure Condition</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="text-align: center;">Inlet</td>
        <td style="text-align: center;">Inflow</td>
        <td style="text-align: center;">Uniform inflow (Dirichlet)</td>
        <td style="text-align: center;">Zero-gradient (Neumann)</td>
      </tr>
      <tr>
        <td style="text-align: center;">Outlet</td>
        <td style="text-align: center;">Outflow</td>
        <td style="text-align: center;">Zero-gradient (Neumann)</td>
        <td style="text-align: center;">Fixed pressure (Dirichlet)</td>
      </tr>
      <tr>
        <td style="text-align: center;">Top/Bottom</td>
        <td style="text-align: center;">Wall</td>
        <td style="text-align: center;">No-slip (u = 0, Dirichlet)</td>
        <td style="text-align: center;">Zero-gradient (Neumann)</td>
      </tr>
    </tbody>
  </table>

</div>

![BC_ChannelFlow](../images/BC_ChannelFlow.png)
<p style="text-align: center; font-size: 0.9em; color: #666;">
Divergenc map, pressure field and velocity magnitude for configuration 1 of the channel flow problem. 
</p>

The velocity field shows the expected behavior induced by the no-slip condition at the walls. A strong vertical gradient in the horizontal velocity component develops near the solid boundaries, forming a parabolic-like profile across the height of the channel. Additionally, we can observe how the flow gradually develops along the streamwise direction, transitioning from the uniform inlet condition to the characteristic profile of a fully developed channel flow. The following figure provides a closer look at this velocity profile by comparing simulated profiles at different streamwise locations with the analytical Poiseuille solution. Notice that the orange curve represents a uniform velocity, corresponding to the inlet condition, before the flow begins to develop.

![Poiseuille](../images/Poiseuille.png)
<p style="text-align: center; font-size: 0.9em; color: #666;">
Horizontal velocity profiles at multiple cross-sections along the channel, compared to the analytical Poiseuille solution.
</p>

The pressure field remains nearly constant in the vertical direction and exhibits a steady decrease along the length of the channel. This behavior reflects the well known **negative pressure gradient** that drives the flow in a pressure-driven channel.

Although the simulation reaches a steady state, a small region of **negative divergence** is visible near the inlet. This localized mass imbalance results from the interaction between the imposed inlet velocity and the developed pressure field. In the next configuration, I tried to **eliminate this divergence** by using boundary conditions that will simulate a fully developed inflow, as if that was not the actual entrance of the pipe. 

### Configuration 2: Fixed Inlet/Outlet Pressure

In this setup, the pressure is fixed at both the inlet and the outlet. Instead of prescribing a velocity profile, the flow develops naturally in response to the **imposed pressure difference**. This approach is usually used to simulate fully developed channel flow driven by a pressure gradient, and I am using it to try to get rid of divergence. 

REVIEW TABLE CONTENTS. 
<div style="display: flex; justify-content: center;">

  <table>
    <thead>
      <tr>
        <th style="text-align: center;">Boundary</th>
        <th style="text-align: center;">Type</th>
        <th style="text-align: center;">Velocity Condition</th>
        <th style="text-align: center;">Pressure Condition</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="text-align: center;">Inlet</td>
        <td style="text-align: center;">Inflow</td>
        <td style="text-align: center;">Uniform inflow (Dirichlet)</td>
        <td style="text-align: center;">Zero-gradient (Neumann)</td>
      </tr>
      <tr>
        <td style="text-align: center;">Outlet</td>
        <td style="text-align: center;">Outflow</td>
        <td style="text-align: center;">Zero-gradient (Neumann)</td>
        <td style="text-align: center;">Fixed pressure (Dirichlet)</td>
      </tr>
      <tr>
        <td style="text-align: center;">Top/Bottom</td>
        <td style="text-align: center;">Wall</td>
        <td style="text-align: center;">No-slip (u = 0, Dirichlet)</td>
        <td style="text-align: center;">Zero-gradient (Neumann)</td>
      </tr>
    </tbody>
  </table>

</div>

### Open Flow

ADD BC TABLE and RESULTS. 

### Object in Open Flow

ADD BC TABLE and RESULTS. 

### Wind Turbine in Open Flow

ADD BC TABLE and RESULTS. 

---
