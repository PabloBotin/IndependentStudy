# Incompressible Navier Stokes Solver

# Index
1. [Introduction](#Introduction)
2. [Governing Equations](#Governing-Equations)
    - [Continuity equation](#Continuity-equation)
    - [Momentum equations](#Momentum-equations)
    - [Challenges in Solving the Incompressible Navier-Stokes Equations](#Challenges-in-Solving-the-Incompressible-Navier-Stokes-Equations)
4. [Discretization](#Discretization)
5. [Grid Types](#Grid-Types)
6. [Algorithm](#Algorithm)
7. [Poisson solver](#Poisson-solver)
   - [Jacobi](#Jacobi)
   - [Gauss-Seidel](#Gauss-Seidel)
8. [Results](#results)
9. [Conclusion](#conclusion)

# Introduction

Fluid dynamics plays an important role in understanding natural phenomena and designing engineering systems. From the flow of air around an airplane wing to the movement of water in rivers, the behavior of fluids is governed by a set of partial differential equations known as the Navier-Stokes equations.

The original motivation for developing this solver was to model wake formation behind wind turbines in a wind farm using a lightweight, efficient computational tool. The goal was to enable fast 2D real-time visualizations, with potential extension into the 3D domain. While this notebook does not focus on that specific application, it centers on the design and implementation of the numerical method behind the solver.

This method targets the 2D incompressible Navier-Stokes equations, which describe the motion of fluids with constant density. These equations are particularly relevant for liquid flows and low-speed gas flows where density variations are negligible.

In this notebook, we introduce the governing equations, discuss the challenges of solving them numerically, and present an efficient solver implementation. Along the way, we compare different grid types, interpolation strategies, and iterative solvers to highlight the numerical trade-offs involved.


# Governing Equations

The **incompressible Navier-Stokes equations** are fundamental to fluid dynamics and are used to model a wide range of physical phenomena, including airflow over airplane wings, water flow through pipes, and wake formation behind wind turbines. These equations express the conservation of mass (via the continuity equation) and the conservation of momentum (via the momentum equation) within a fluid.

By assuming **incompressibility**, we neglect variations in density, an accepted assumption for many liquid flows and low-speed gas flows. This simplification reduces the complexity of the equations while still capturing the essential physics of many practical problems.

The incompressible Navier-Stokes equations consist of:
- **Mass conservation**, ensuring mass conservation
- **Momentum conservation**, derived from Newton’s second law applied to fluid motion


## Continuity equation
The continuity equation ensures the **conservation of mass** in incompressible flows. For a velocity field 
u, the equation is written as $$∇⋅u= 0$$ In 2D derivative form, it becomes:  $$\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0$$
## Momentum equations
The momentum equations describe the conservation of momentum in the fluid, considering all the forces involved. For incompressible flows, they are expressed as:
$$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\frac{1}{\rho} \nabla p + \nu \nabla^2 \mathbf{u} + \mathbf{f}$$
In 2D derivative form:

**x-Momentum:**
$$\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} + v \frac{\partial u}{\partial y} = -\frac{1}{\rho} \frac{\partial p}{\partial x} + \nu \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\right) + F_x$$
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


# Grid Types 
Numerical solvers for the incompressible Navier-Stokes equations often use structured grids to discretize the computational domain. Two common types of grids are **collocated grids** and **staggered grids**. This section explains these grid configurations, discusses why staggered grids are often preferred for maintaining incompressibility and compares the results of using the different grids for the same cases. 

<p style="text-align: center;">
    <img src="/Users/pabo1849/Library/CloudStorage/OneDrive-UCB-O365/Documents/Research/IndependentStudy/images/GridTypes.png" alt="GridTypes" width="600">
    <br>
    <span style="display: block; text-align: center;">Grid Types: Collocated and staggered</span>
</p>

## Collocated Grid

In a **collocated grid** all flow variables—such as the velocity components $(u, v)$ and pressure $p$—are stored at the same grid points (typically at cell centers). This arrangement simplifies data storage and implementation, especially in structured solvers. However, this can lead to spurious pressure oscillations, often referred to as *checkerboard patterns*, which can make the numerical solution unstable or non-physical.

<p style="text-align: center;">
    <img src="/Users/pabo1849/Library/CloudStorage/OneDrive-UCB-O365/Documents/Research/IndependentStudy/images/Checkerboard.png" alt="Checkerboard" width="600">
    <br>
    <span style="display: block; text-align: center;"> (Undesired) Checkerboard effect </span>
</p>

In addition to pressure-velocity decoupling, another potential issue with collocated grids is the failure to fully enforce the mass conservation condition. This can result in non-zero divergence across the domain, particularly in regions with complex flow features or sharp gradients. The following divergence maps highlight this effect in three different scenarios. In the lid-driven cavity case (left), divergence appears primarily at the corners, likely due to abrupt changes in boundary conditions. In the channel flow with a square obstacle (center), and open flow around a wind turbine (right).</em>

In addition to pressure-velocity decoupling, another potential issue with collocated grids is the failure to fully enforce the mass conservation condition. This can result in non-zero divergence across the domain, particularly in regions with complex flow features or sharp gradients. The following divergence maps highlight this effect in three different scenarios. In the lid-driven cavity case (left), divergence appears primarily at the corners, most probably due to aggresive changes in boundary conditions. In the channel flow with a square obstacle (center), divergence is concentrated at the inlet corners and around the object, where strong velocity gradients and flow separation make it difficult to maintain a divergence-free field. In the open flow around a wind turbine (right), divergence is observed both in front of and behind the turbine, likely caused by large, concentrated velocity gradients. 


<p style="text-align: center;">
    <img src="/Users/pabo1849/Library/CloudStorage/OneDrive-UCB-O365/Documents/Research/IndependentStudy/images/Divergence_CavityFlow.png" alt="Divergence_CavityFlow" height="205" style="margin: 0 10px">
    <img src="/Users/pabo1849/Library/CloudStorage/OneDrive-UCB-O365/Documents/Research/IndependentStudy/images/Divergence_CFSquare.png" alt="Divergence_CFSquare" height="205" style="margin: 0 10px;">
    <img src="/Users/pabo1849/Library/CloudStorage/OneDrive-UCB-O365/Documents/Research/IndependentStudy/images/Divergence_Turbine.png" alt="Divergence_Turbine" height="205" style="margin: 0 10px;">
</p>
<p style="text-align: center;">
    <em>Divergence maps for lid-driven cavity flow (left), channel flow with square obstacle (center), and open flow around a wind turbine (right).</em>
</p>

To mitigate this issues, correction schemes can be employed to stabilize the pressure field. However, adopting a staggered grid potentially offers a more fundamental solution by addressing the root cause of the decoupling.

## Staggered Grid

In a **staggered grid**, different variables are stored at different spatial locations within each grid cell, in this case:

- Pressure $p$ is stored at the **cell center**.
- The horizontal velocity component $u$ is stored at the center of the **vertical cell faces**.
- The vertical velocity component $v$ is stored at the center of the **horizontal cell faces**.

<p style="text-align: center;">
    <img src="/Users/pabo1849/Library/CloudStorage/OneDrive-UCB-O365/Documents/Research/IndependentStudy/images/Staggered.png" alt="Staggered grid variables" width="600">
    <br>
    <span style="display: block; text-align: center;">Staggered grid. Variables location layout.</span>
</p>

This configuration naturally couples pressure and velocity by positioning them at offset locations—velocity components on the cell faces and pressure at the cell centers. This offset arrangement may help satisfy the discretized continuity equation more accurately. It could also reduce or eliminate pressure oscillations without the need for artificial interpolation, potentially making staggered grids more effective for incompressible flow solvers.

## Comparison of Solutions

To evaluate the practical impact of grid configuration, I implemented both a collocated and a staggered grid version of the solver and ran them on the same test case.

INSERT FIGURES OF VELOCITY AND DIVERGENCE FOR COLLOCATED AND STAGGERED. 
FIND SIMILAR CASES AND COMPARE. HOW DIFFERENT WERE THEY? CAN I FIND CHECKERBOARD AND NO CHECKERBOARD? 


EXPLAIN

> 📌 *Insert plots showing velocity fields and divergence magnitude for both grid types.*

This comparison illustrates the **numerical robustness and stability** of staggered grids for solving the incompressible Navier-Stokes equations.


# Discretization 
EXPLAIN how the equations were discretized on the staggered (and collocated) grid, including the different used interpolations. 

# Algorithm
In this section, we outline and compare two different numerical algorithms employed to solve the incompressible Navier-Stokes equations: **Chorin's Projection Method** and the **Predictor-Corrector Method**. These algorithms differ in their sequence of operations and the way they integrate the pressure and velocity fields over time. I will explain and implement both methods and compare their performance and results in terms of accuracy and computational efficiency.
## 1st order unsplit Euler's method (Laurena Barba's method)  
Chorin's projection method is a widely used technique to solve the incompressible Navier-Stokes equations. The primary goal of this method is to ensure that the computed velocity field remains divergence-free (i.e., mass-conserving) at each timestep. This is achieved through two main steps: pressure projection and advection-diffusion, which are alternated to ensure the incompressibility condition.
### Step 1. Solving the Poisson equation for pressure correction.
The first step in Chorin’s method is to solve the Poisson equation for the pressure, which is derived from the incompressibility condition $$\nabla^2 p = \nabla \cdot \mathbf{u}^*$$ The ultimate goal is to calculate the pressure gradient that will ensure zero divergence when performing the advection-diffusion step. 
### Step 2. Advection-Diffusion with Pressure Gradient.
The advection-diffusion step updates the velocity field by incorporating the pressure gradient ($\nabla p^*$) obtained from the solution of the Poisson solver. This step ensures the incompressibility of the flow by adjusting the velocity field based on the pressure distribution, while simultaneously advecting and diffusing the fluid. The advection-diffusion equation, which includes the pressure gradient, is:
$$
\mathbf{u}^{n+1} = \mathbf{u}^n + \Delta t \left[ -\frac{1}{\rho} \nabla p^* + \nu \nabla^2 \mathbf{u}^n - (\mathbf{u}^n \cdot \nabla) \mathbf{u}^n + \mathbf{f} \right]
$$

## Chorin's Projection method 
Chorin's fractional step algorithm is a widely used method to solve fluid dynamics equations, particularly when dealing with incompressible flows. The idea is to perform the advection-diffusion step without considering the pressure gradient. This step gives us an intermediate velocity field that may not be divergence-free (it does not satisfy the incompressibility condition). Then, we correct this predicted velocity field to ensure incompressibility, using the pressure gradient computed from the Poisson equation.

### Step 1. Prediction Step (Advection-Diffusion).
In the prediction step, the velocity field is updated by solving the advection-diffusion equation without considering the pressure gradient term. This means that the velocity field evolves based on the advection of the fluid and the diffusion effects, but the incompressibility constraint is not enforced at this stage.
$$
\mathbf{u}^{n+1} = \mathbf{u}^n + \Delta t \left[\nu \nabla^2 \mathbf{u}^n - (\mathbf{u}^n \cdot \nabla) \mathbf{u}^n + \mathbf{f} \right]
$$
The result of this step is an intermediate velocity field that may not satisfy the incompressibility condition ∇⋅u=0.

### Step 2. Solve the Poisson Equation. 
This step involves solving the Poisson equation for the pressure field with the fractional velocity field (u*). 
$$\nabla^2 p = \nabla \cdot \mathbf{u}^*$$
The solution to this equation provides the pressure distribution required to compute the pressure gradient that will be used to correct the velocity field in order to ensure that it is divergence-free.

### Step 3. Correction Step (Apply Pressure Gradient term)
After solving for the pressure p, we compute the pressure gradient which is the missing  used to correct the velocity field. The corrected velocity field is computed by subtracting the pressure gradient term from the intermediate velocity:
$$
\mathbf{u} = \mathbf{u}^* - \frac{\nabla p}{\rho}*\Delta t
$$
This method really ensures zero divergence because the Poisson equation is solved for the actual velocity field. 



# Poisson solver 
In incompressible flows, ensuring mass conservation requires solving the Poisson equation for pressure at each time step, based on the updated velocity field. This step is crucial for projecting the velocity field to satisfy the continuity equation:
where $$\nabla^2 p = \nabla \cdot \mathbf{u}^*$$
where p is the intermediate velocity field computed from the momentum equation.
To solve this equation efficiently, two common iterative solvers are used: Jacobi and Gauss-Seidel methods. In this section, I will explain both methods step by step, provide scripts for their implementation, and compare their performance.

## Jacobi 
The Jacobi method computes the solution iteratively by solving for each variable in terms of the others using values from the previous iteration.
### Algorithm steps 
1. **Initialize variables.** Start with the current p field & define the RHS (b) of the Poisson equation (derived from velocity divergence). 
2. **Precompute coefficients.** Precompute p_coef and b, which are adjusted for the grid spacings. $$p_{\text{coef}} = \frac{1}{2(\Delta x^2 + \Delta y^2)}$$ $$b_{i,j} \leftarrow b_{i,j} \cdot \frac{2(\Delta x^2 + \Delta y^2) \rho}{\Delta x^2 \Delta y^2}$$ The computation of b depends on the method used (projection or predictor-corrector). 
4. **Iteration.** Jacobian update of p on the interior grid points.  $$p_{i,j}^{(k+1)} = p_{\text{coef}} \left[ (p_{i+1,j}^{(k)} + p_{i-1,j}^{(k)}) \Delta y^2 + (p_{i,j+1}^{(k)} + p_{i,j-1}^{(k)}) \Delta x^2 \right] - b_{i,j}$$
5. **Enforce Boundary Conditions** Apply Neumann boundary conditions $\frac{\partial p}{\partial n} = 0$ in this case. This may change depending on the BC problem.
6. **Compute Error** Calculate the root-mean-square (RMS) error between successive pressure fields: $$\text{Error} = \sqrt{\frac{1}{N} \sum_{i,j} \left( p_{i,j}^{(k+1)} - p_{i,j}^{(k)} \right)^2}$$
7. **End of the iteration** Iteration automatically ends if: 
    A) Error is lower than tolerance.
    B) Maximum number of iterations is reached.
8. **Output** Return the final pressure field, which satisfies the Poisson equation within the specified tolerance.


```python
def pressure_poisson(p, b, dx, dy, tol, maxiter):
    """
    Solve the Poisson equation for pressure correction using Jacobi's iterative method.

    Parameters:
    -----------
    p : numpy.ndarray
        Current pressure field. This array will be updated iteratively.
    b : numpy.ndarray
        Right-hand side of the Poisson equation, derived from velocity divergence.
    dx, dy : float
        Grid spacing in the x and y directions.
    tol : float
        Convergence tolerance for the root-mean-square error.
    maxiter : int
        Maximum number of iterations. Accelerates the speed at the beginning of the iterations. 
    rho : density. 

    Returns:
    --------
    numpy.ndarray
        The updated pressure field that satisfies the Poisson eq. within the specified tolerance.

    Notes:
    ------
    - Implements Jacobi's method, iteratively updating the pressure field.
    - Enforces Neumann boundary conditions (zero pressure gradient) on all domain edges (this is just for the Cavity Flow case). 
    - The method stops when either the error falls below the specified tolerance or the maximum
      number of iterations is reached.
    """
    err = np.inf # Initialize huge error.
    nit = 0 # Reset num iterations.
    pcoef = 0.5 / (dx**2 + dy**2) # Simplifies code
    b *= rho * dx**2 * dy**2 / (2*(dx**2 + dy**2))

    while err > tol and nit < maxiter:
        pn = p.copy()

        p[1:-1, 1:-1] = (pcoef * ((pn[1:-1, 2:] + pn[1:-1, :-2])*dy**2
                        + (pn[2:, 1:-1] + pn[:-2, 1:-1])*dx**2) - b)

        # BCs. Openfield.
        p[:, 0] = p[:, 1] # dp/dx=0 at x=0.
        p[:, -1] = -p[:, -2] # p = 0 at x = L.
        p[0, :] = p[1, :]   # dp/dy = 0 at y = 0.
        p[-1, :] = p[-2, :] # dp/dx = 0 at y = 2.

        err = np.mean((p[1:-1, 1:-1] - pn[1:-1, 1:-1])**2)**0.5
        nit += 1

    return p
```

## Gauss-Seidel
The Gauss-Seidel method improves on Jacobi's iterative solver by updating the pressure values in-place, making it more computationally efficient. What is more, it has been implemented using Cython for an even faster convergence.
### Algorithm steps 
1. **Initialize variables.** Start with the current p field & define the RHS (b) of the Poisson equation (derived from velocity divergence). 
2. **Precompute coefficients.** Precompute p_coef and b, which are adjusted for the grid spacings. $$p_{\text{coef}} = \frac{1}{2(\Delta x^2 + \Delta y^2)}$$ $$b_{i,j} \leftarrow b_{i,j} \cdot \frac{2(\Delta x^2 + \Delta y^2) \rho}{\Delta x^2 \Delta y^2}$$ 
4. **Iteration.** Loop through the grid, updating the pressure values in-place at each grid point using the formula: $$p_{i,j} = p_{\text{coef}} \left[ (p_{i,j+1} + p_{i,j-1}) \Delta y^2 + (p_{i+1,j} + p_{i-1,j}) \Delta x^2 \right] - b_{i,j}$$
5. **Enforce Boundary Conditions** Apply Neumann boundary conditions $\frac{\partial p}{\partial n} = 0$ in this case. This may change depending on the BC problem.
6. **Compute Error** Calculate the root-mean-square (RMS) error between successive pressure fields: $$\text{Error} = \sqrt{\frac{1}{N} \sum_{i,j} \left( p_{i,j}^{(k+1)} - p_{i,j}^{(k)} \right)^2}$$
7. **End of the iteration** Iteration automatically ends if: 
    A) Error is lower than tolerance.
    B) Maximum number of iterations is reached.
8. **Output** Return the final pressure field, which satisfies the Poisson equation within the specified tolerance.

<p style="text-align: center;">
    <img src="/Users/pabo1849/Library/CloudStorage/OneDrive-UCB-O365/Documents/Research/IndependentStudy/images/ChorinAlgorithm.png" alt="Chorin Algorithm" width="600">
    <br>
    <span style="display: block; text-align: center;">Chorin's algorithm schematic.</span>
</p>




```python
def pressure_poisson_gauss_seidel(p, b, dx, dy, rho):
    """
    Solve the Poisson equation for pressure correction using the Gauss-Seidel method.

    This function iteratively solves the pressure Poisson equation, which is derived from 
    the incompressible Navier-Stokes equations to ensure mass conservation. It uses the 
    Gauss-Seidel method for in-place updates, leveraging the latest pressure estimates 
    during each iteration for faster convergence.

    Parameters:
    -----------
    p : numpy.ndarray
        The pressure field (2D array) that needs to be updated in order to satisfy the Poisson equation. 
    b : numpy.ndarray
        The Poisson's equation RHS (b term, 2D array) derived from the velocity divergence.
    dx : float
        Grid spacing in the x-direction.
    dy : float
        Grid spacing in the y-direction.
    rho : float
        Fluid density, used to scale the source term.

    Returns:
    --------
    p : numpy.ndarray
        Updated pressure field satisfying the Poisson equation within the specified tolerance.

    Key Features:
    --------------
    1. In-place updates using Gauss-Seidel accelerate convergence compared to Jacobi's method.
    2. Enforces Neumann boundary conditions (zero pressure gradient) on all domain edges (this is just for the Cavity Flow case).
    3. Convergence is determined based on the root-mean-square (RMS) error between iterations.
    """
    err = np.inf  # Initialize a large error.
    nit = 0  # Reset the number of iterations.
    pcoef = 0.5 / (dx**2 + dy**2)  # Precompute coefficient for simplicity.
    b *= rho * dx**2 * dy**2 / (2 * (dx**2 + dy**2))

    while err > tol and nit < maxiter:
        pn = p.copy()

        # Gauss-Seidel in-place update
        p = gauss_seidel_iteration(p, b, pcoef, dx, dy)

        # Apply boundary conditions
        p[:, 0] = p[:, 1] # dp/dx=0 at x=0.
        p[:, -1] = -p[:, -2] # p = 0 at x = L.
        p[0, :] = p[1, :]   # dp/dy = 0 at y = 0.
        p[-1, :] = p[-2, :] # dp/dx = 0 at y = 2.

        # Calculate error based on the new values
        err = np.mean((p[1:-1, 1:-1] - pn[1:-1, 1:-1])**2)**0.5
        nit += 1

    return p
```

## Comparison of Poisson Solvers: Jacobi vs. Gauss-Seidel

To assess the performance of the Jacobi and Gauss-Seidel methods in solving the Poisson equation, both algorithms were applied to the same flow setup. The figure below shows the resulting divergence fields for each method: the Jacobi solution is shown on the left, and the Gauss-Seidel solution on the right.

<p style="text-align: center;">
    <img src="/Users/pabo1849/Library/CloudStorage/OneDrive-UCB-O365/Documents/Research/IndependentStudy/images/Jacobi_vs_GaussSeidel.png" alt="Jacobi vs Gauss-Seidel divergence fields" width="900">
    <br>
    <span style="display: block; text-align: center;">Divergence field results using Jacobi (left) and Gauss-Seidel (right) solvers.</span>
</p>

For the same problem setup, the Gauss-Seidel method converged approximately 45% faster, requiring only 17 seconds compared to 32 seconds for the Jacobi solver. Furthermore, the final velocity field obtained with Gauss-Seidel had a divergence four orders of magnitude smaller than that obtained using Jacobi. This highlights Gauss-Seidel's improved numerical stability and effectiveness in enforcing the incompressibility constraint, making it a more efficient and accurate choice for solving the Poisson equation in this context.

What’s more, the Gauss-Seidel solver can be further optimized using Cython, allowing for substantial reductions in computation time by accelerating the most performance-critical loops in the algorithm.


### Performance Optimization with Cython make this more casual. 
To improve the performance of the iterative solver, Cython is used. Cython is a superset of Python that enables C-like performance optimizations while preserving the readability and ease of Python syntax. By compiling Python code to C, it allows the iterative solver to execute much faster, which is essential for large grid sizes in computational fluid dynamics simulations.

In particular, the `gauss_seidel_iteration` function is implemented using Cython, which allow direct and efficient interaction with NumPy arrays while avoiding the overhead of Python's dynamic typing. This approach enables fast and memory-efficient manipulation of large datasets, making it well-suited for CFD applications. Instructions for usage are included in the documentation of the function.


```python
def gauss_seidel_iteration(cnp.ndarray[cnp.double_t, ndim=2] p,
                           cnp.ndarray[cnp.double_t, ndim=2] b,
                           double pcoef,
                           double dy,
                           double dx):
    cdef int i,j

    for i in range(1,p.shape[0]-1):
        for j in range(1,p.shape[1]-1):
            p[i,j] = pcoef * ((p[i,j+1] + p[i,j-1]) * dy**2
                                + (p[i+1,j] + p[i-1,j]) * dx**2) - b[i-1,j-1]

    return p

# Instructions for usage:
# 1. Recompile the pyx file: python setup.py build_ext --inplace
# 2. Run main.py normally 
```

### Convergence of the Poisson Solver

The convergence behavior of the Gauss-Seidel solver is illustrated in the following figure, which plots the logarithm of the norm of the residual (the difference between successive pressure fields) as a function of the number of iterations. This metric provides a quantitative measure of how rapidly the solution approaches a steady state. The curve exhibits a steep decline during the first 700 iterations, indicating rapid error reduction in the early stages of the solution process. Beyond this point, the slope of the curve decreases, forming a slightly concave shape that reflects slower but continued convergence toward the final solution. This behavior highlights the diminishing returns of additional iterations once the residual has been sufficiently minimized. Therefore, it is important to define an appropriate convergence threshold to find a practical balance between computational efficiency and solution accuracy.

<p style="text-align: center;">
    <img src="/Users/pabo1849/Library/CloudStorage/OneDrive-UCB-O365/Documents/Research/IndependentStudy/images/PoissonConvergence.png" alt="Poisson solver convergence" width="500">
    <br>
    <span style="display: block; text-align: center;">Convergence of the Poisson solver: logarithm of the residual norm versus number of iterations.</span>
</p>


```python

```

References: 
- Cython: https://cython.org/
- Gauss Seidel and Jacobi. 
- Incompressible NS (Kelsea Boom)
- Lorena Barba
- Chorins paper
- Peter's 3030 course TextBook (Check which one he s using). 
