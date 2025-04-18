# Discretization 
This part should come either before the Grid-splitting discussion, or be a part of it...

- A derivate (time or space) of a function can be approximated by discrete points, or function evaluations. The simplest approximation is to use two points,
$$ 
\frac{\partial f}{\partial x} \approx \frac{1}{h}(f(x + h) - f(x)).
$$
- Note that the accuracy of this approximation is affected by where the derivative is assumed to be located relative to the two points in the differece, which are referred to as forward, backward, and central finite difference approxiations.
$$
\frac{\partial}{\partial x}f(x) \approx \frac{1}{h}((x + h) - f(x)) + O(h),\quad \text{Forward difference (1st-order accurate)},
$$
$$
\frac{\partial}{\partial x}f(x) \approx \frac{1}{h}(f(x) - f(x - h)) + O(h),\quad \text{Backward difference (1st-order accurate)},
$$
$$
\frac{\partial}{\partial x}f(x) \approx \frac{1}{h}(f(x + 0.5 h) - f(x - 0.5 h)) + O(h^2),\quad \text{Central difference (2nd-order accurate)},
$$
- A central finite difference scheme on a ``collocated'' grid requires a total of three points, as the approximation of the derivated \emph{is located at the same points as} the function evaluations. This results in a scheme with $h = 2\Delta x$: [add figure of three points, each separated by $\Delta x$ and note that $h = 2\Delta x$ for the formula above]

- A central finite difference scheme on a ``staggered" grid uses only two adjacent points of a function, for instance $x$-velocity $u_x$, but locates the resulting finite difference approximation in between these two points, at a point where pressure is located. This results in a scheme with $h = \Delta x$, providing twice the resolution without twice the number of variables stored in memory! [add figure of staggered grid points, demonstrating where each velocity and pressure component lives, and where each of their derivatives in x and y live, and note that $h = \Delta x$].

- Talk about discretization of the Boundary Conditions