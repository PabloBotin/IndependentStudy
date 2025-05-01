# Discretization 

The spatial derivative of a function can be approximated by a series of function evaluations at a finite number of discrete points, known as a **finite difference**. The simplest approximation is to use the difference of two points:

<div id="eq-first-deriv"></div>

\[
\frac{\partial f}{\partial x} = f' \approx \frac{1}{h}(f(x + h) - f(x)) \tag{1}
\]

The accuracy of this approximation depends on where the derivative is assumed to be located relative to the two points in the difference. These are referred to as **forward**, **backward**, and **central finite difference approximations**. If $f'$ is evaluated at $x$, this is known as a **forward difference**, which is **first-order accurate** (i.e., the error scales linearly with $h$). If $f'$ is evaluated at $x + h$, it's a **backward difference** (also first-order). However, if $f'$ is evaluated at the midpoint, $x + \tfrac{1}{2}h$, then it becomes a **central difference**, which is **second-order accurate**, with error scaling as $h^2$.

For a **second derivative**, one can take a finite difference of a finite difference:

<div id="eq-second-deriv"></div>

\[
\frac{\partial^2 f}{\partial x^2}
\approx \frac{1}{h}(f'(x + h) - f'(x))
\approx \frac{1}{h^2}(f(x + h) - 2f(x) + f(x-h)) \tag{2}
\]

As shown in [**(7)**](#eq-second-deriv), the second derivative is typically assumed to be located at the midpoint $x$, making it a second-order central difference approximation.

The [12 Steps to CFD][barba] lessons use a mixture of forward and central finite differences for interior grid points, and forward or backward differences for [Dirichlet boundary conditions](./boundary_conditions.md), as appropriate. However, for the remainder of this section, **we will only discuss central finite differences**.

## Central Finite Differences on Collocated Grids

A central finite difference scheme on a **collocated solution grid** requires a total of **three grid points**, with the approximation of the derivative located at the central point—**the same location where the variable itself is evaluated**. In this setup, the spacing between the outer points used in the approximation is $h = 2\Delta x$, rather than $\Delta x$ as in the standard grid.

> **Figure placeholder**: Add a diagram showing three equally spaced grid points, each separated by $\Delta x$, and annotate that $h = 2\Delta x$ in [**(7)**](#eq-second-deriv).

Since all the solution variables ($u$, $v$, and $p$), along with their spatial gradients, are **collocated at the same grid points**, no interpolation schemes are required to compute the pressure field or to advance the Navier-Stokes equations in time.

For more information, see the section on [collocated grids](./grid_types.md#collocated-grid).

## Central Finite Differences on Staggered Grids

A central finite difference scheme on a **staggered grid** uses a different set of solution grid points for each variable. Derivatives are evaluated between two adjacent points specific to each variable, and the resulting finite difference approximation lies between them. This location **may or may not** coincide with the grid point of another variable.

This scheme uses a nominal spacing of $h = \Delta x$, which provides **twice the approximation accuracy** of the collocated case for the same number of total solution points. This improvement in resolution directly follows from the standard second-derivative approximation in [**(7)**](#eq-second-deriv).

> **Figure placeholder**: Add a schematic showing the staggered layout: where $u$, $v$, and $p$ live, where $\partial u/\partial x$, $\partial v/\partial y$, and $\partial p/\partial x$ are computed, and note that $h = \Delta x$.

However, the **time integration** of each variable must occur at its corresponding grid location. For instance, the $u$-momentum equation must be evaluated at the $u$ grid points, but the associated $v$ and $p$ values—and even the gradients of $u$—are not naturally stored at those locations. As a result, staggered grids require **interleaving finite differencing with interpolation**.

> **Figure placeholder**: Add a visualization showing how interpolation is used on a staggered grid. Include the same figure, with more discussion, in the [staggered grid section](./grid_types.md#staggered-grid).

Despite the additional computational effort, staggered grids offer a significant advantage: **pressure gradients are evaluated at the correct physical locations** required by the Navier-Stokes equations. For example, $\partial p/\partial x$ is evaluated exactly where $u$ lives, and the divergence of velocity—$\partial u/\partial x + \partial v/\partial y$—is naturally computed at the pressure points.

For more details, see the section on [staggered grids](./grid_types.md#staggered-grid).

---
[barba]: https://github.com/barbagroup/CFDPython "Lorena Barba's CFD Python Tutorials"