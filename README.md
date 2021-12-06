# CIL vs CVXPY

This repository contains several scipts that compare the solution of different imaging minimisation problems using the [Core Imaging Library (CIL)](https://github.com/TomographicImaging/CIL) and [cvxpy](https://github.com/cvxpy/cvxpy). All the cvxpy scripts are initially implemented in Matlab for [1](https://link.springer.com/article/10.1007%2Fs10851-015-0624-6) and [2](https://link.springer.com/chapter/10.1007/978-3-319-55795-3_15)

## Imaging Problems

- [Total Variation Denoising](https://github.com/epapoutsellis/CIL_and_CVXPY/blob/main/TotalVariation.py)
- [Total Generalised Variation Denoising](https://github.com/epapoutsellis/CIL_and_CVXPY/blob/main/TotalGeneralisedVariation.py)
- [Directional Total Variation Denoising](https://github.com/epapoutsellis/CIL_and_CVXPY/blob/main/Directional_TotalVariation.py)

## Note

- For the cvxpy implementation, the [Splitting Conic Solver](https://github.com/cvxgrp/scs) is used by default. Another option is to use the [MOSEK](https://www.cvxpy.org/tutorial/advanced/index.html) solver but requires a licence. Institutional Academic License is free.

## References

[1] Infimal Convolution Regularisation Functionals of BV and L^p Spaces. Part I: The finite p case
Burger, Martin, Papafitsoros, Konstantinos, Papoutsellis, E, and Schönlieb, Carola-Bibiane
Journal of Mathematical Imaging and Vision 2016

[2] Infimal Convolution Regularisation Functionals of BV and L^p Spaces. The Case p=∞
Burger, Martin, Papafitsoros, Konstantinos, Papoutsellis, E, and Schönlieb, Carola-Bibiane
In System Modeling and Optimization 2016


