# CIL vs CVXPY

This repository contains several scipts that compare the solution of different imaging minimisation problems using the [Core Imaging Library (CIL)](https://github.com/TomographicImaging/CIL) and [cvxpy](https://github.com/cvxpy/cvxpy).

## Imaging Problems

- Total Variation Denoising
- Total Generalised Variation Denoising
- Directional Total Variation Denoising

## Note

- For the cvxpy implementation, the [Splitting Conic Solver](https://github.com/cvxgrp/scs) is used by default. Another option is to use the [MOSEK](https://www.cvxpy.org/tutorial/advanced/index.html) solver but requires a licence. Institutional Academic License is free.

$$\begin{equation}
u^{*} =\underset{u}{\operatorname{argmin}} \frac{1}{2} \| \mathcal{A} u - g\|^{2} +
\underbrace{
\begin{cases}
\alpha\,\|u\|_{1}, & \\[10pt]
\alpha\,\|\nabla u\|_{2}^{2}, & \\[10pt]
\alpha\,\mathrm{TV}(u) + \mathbb{I}_{\{u\geq 0\}}(u).
\end{cases}}_{Regularisers}
\tag{1}
\end{equation}$$

