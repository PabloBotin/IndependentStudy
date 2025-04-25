# Discretization 

The spatial derivate of a function can be approximated by a series of function evaluations at a finite number of discrete points, known as a finite difference. The simplest approximation is to use the difference of two points,
$$ 
\frac{\partial f}{\partial x} = f' \approx \frac{1}{h}(f(x + h) - f(x)).
$$

The accuracy of this approximation is dependent on where the derivative is assumed to be located relative to the two points in the differece, which are referred to as forward, backward, and central finite difference approximations. If $f'$ is evaluated at $x$, this is known as a forward finite difference, which is first-order accurate (i.e., the error scales with the separation, $h$). If $f'$ is evaluated at the point $x+h$, this is a backward finite difference (also first-order). However, if $f'$ is evaluated at the midpoint, $x + \tfrac{1}{2}h$, then we have the second-order accurate central finite difference (i.e., the error scales as $h^2$)

For a second derivative, it is simple enough to take a finite difference of a finite difference,
$$\begin{aligned}
\frac{\partial^2 f}{\partial x^2} &{}\approx \frac{1}{h}(f'(x + h) - f'(x))\\
&{}\approx \frac{1}{h^2}(f(x + h) - 2f(x) + f(x-h)).
\end{aligned}$$
In this case, the second derivative is virtually always assumed to be located at the midpoint, $x$, in which case it is a second-order accurate central difference approximation.

The *12 Steps to CFD* lessons utilize a mixture of forward and central finite differences for interior grid points, and forward or backward differences for [Dirichlet boundary conditions](./boundary_conditions.md), as appropriate. However, for the remainder of this section we will only discuss central finite differences.

## Central Finite Differences on collocated grids
A central finite difference scheme on a "collocated" solution grid requires a total of three grid points, with the approximation of the derivate located at the central solution grid point that \emph{is located at the same point as} an evaluation of the differentiated variable itself. This results in a scheme with $h = 2\Delta x$.

> **add figure of three points, each separated by $\Delta x$ and note that $h = 2\Delta x$ for the formula above**

Because all of the solution variables ($u$, $v$, and $p$) and each of their spatial gradients are collocated at the same grid points, no spatial interpolation schemes are required to solve for the pressure field, or integrate the Navier-Stokes equations forward in time.

For more information, see the section on [collocated grids](./grid_types.md#collocated-grid).

## Central Finite Differences on staggered grids
A central finite difference scheme on a "staggered" grid uses a different set of solution grid points for each variable and then evaluates derivatives of each variable using two adjacent grid points. Therefore, the resulting finite difference approximation always lies between these two points, which may or may not correspond to the location of a solution point for one of the other variables. This results in a scheme with a nominal spacing of $h = \Delta x$, providing twice the approximation accuracy of a collocated scheme with the same total number of solution points for all variables. 

> **add figure of staggered grid points, demonstrating where each velocity and pressure component lives, and where each of their derivatives in x and y live, and note that $h = \Delta x$.**

However, the time integration of each solution variable must occur on a collocated set of grid points. For instance, the governing equation for $u$ must be evaluated at the $u$ grid points, while the values of $v$ and $p$ are not stored at these same points, nor are the gradients of $u$ evaluated at these points. This necessitates a solution procedure that interleaves finite differencing and linear interpolation. Thus a staggered grid requires more computational effort than a collocated grid. 

> **add a figure demontrating interpolation. Also include the same figure, with more detailed discussion, in the staggered grid section**

What makes a staggered grid worth this extra effort is that pressure gradients are evaluated at the correct solution points for the Navier-Stokes equations (e.g., $\partial p/\partial x$ is evaluated at the $u$ solution points), while the velocity gradients $\partial u/\partial x$ and $\partial v/\partial y$, which are central to the Poisson equation for pressure, are evaluated at the $p$ solution points.

For more information, see the section on [staggered grids](./grid_types.md#staggered-grid).