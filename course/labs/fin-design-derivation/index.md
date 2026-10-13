# Module 7, Part II: Finite And Infinite Rod Theory

This is the second part of Module 7. Read [Part I: Thermal Transport
Foundations](../theory-bridge-chapter-1/index.md) first, then use this derivation
in [Part III: Rod Instrument And Stationary Fin](../lab-08/index.md).

This reference develops Lienhard and Lienhard Section 4.5, textbook
pp. 163-173. It collects Eqs. (4.27)-(4.51) in one place so you can follow the
logic from a physical fin to the finite-length and infinite-length rod models
used in Module 7, Part III.

## Learning Objectives

The objectives below are listed in priority order. By the end of Module 7,
Part II, you should be able to:

1. Use Fourier conduction, Newton cooling, and conservation of energy to derive
   the stationary one-dimensional fin equation and check every term's units.
2. Apply the base-temperature and insulated-tip boundary conditions to obtain
   the finite-rod temperature profile.
3. Interpret the transverse Biot number and the dimensionless group $mL$ as
   tests of two different approximations: uniform temperature across a section
   and negligible influence of the far end.
4. Obtain the semi-infinite exponential profile as a limit of the finite-rod
   solution and quantify the resulting approximation error at the sensor
   positions.

## How To Use This Reference

Read this page alongside Lienhard Section 4.5 for A4. The Module 7 workload
budget includes **150 minutes total** for reading the module, the textbook
section, and this guide. This page is not a separate submission and should not
be copied into another report.

Annotate the derivation with three questions in mind:

1. Which term comes from Fourier conduction along the rod?
2. Which term comes from Newton cooling through the rod's side?
3. Which boundary condition distinguishes the finite insulated-tip solution
   from the semi-infinite solution?

## What A Fin Does

A fin conducts heat along a solid while exchanging heat with the surrounding
fluid through its surface. Increasing surface area can greatly increase heat
transfer.

![Pin-fin heat exchanger](../../assets/pin-fin.gif)

![Pin-fin assembly](../../assets/pin-fin-3.jpg)

*Examples used in the historical Phys 39 course: extended metal surfaces
increase the area available for heat transfer.*

![Possible biological cooling fins](../../assets/lienhard-fig-4-7-fin-example.png)

*Lienhard and Lienhard, Fig. 4.7, textbook p. 165: a speculative biological
example of cooling fins.*

## Geometry And The One-Dimensional Assumption

![One-dimensional fin geometry and energy-balance slice](../../assets/lienhard-fig-4-8-fin-model.png)

*Lienhard and Lienhard, Fig. 4.8, textbook p. 166: a fin of length \(L\),
cross-sectional area \(A\), perimeter \(P\), conductivity \(k\), side
coefficient \(h\), and tip coefficient \(h_L\).*

The transverse Biot number must be small:

\[
\mathrm{Bi}_{\mathrm{fin}}
=\frac{h(A/P)}{k}\ll1.
\tag{4.27}
\]

### What The Transverse Biot Number Compares

The transverse Biot number does **not** compare radial heat transport with
axial heat transport. It compares conduction from the interior of a cross
section to its surface with convection from that surface to the surrounding
air.

Refer back to [Fig. 1.10 and the accompanying Part I discussion of lumped
cooling and the Biot number](../theory-bridge-chapter-1/index.md#5-lumped-cooling-and-the-biot-number).
That figure shows the same two processes in sequence: heat first conducts
through the solid to its surface and then crosses from the surface to the
surroundings. Here we apply that picture across each cross section of the rod.

Consider a rod element of length $\delta x$. Its curved surface area is
$P\delta x$, and the characteristic transverse conduction length is

\[
L_c=\frac{A}{P}.
\]

For a circular rod, $A=\pi R^2$ and $P=2\pi R$, so

\[
L_c=\frac{A}{P}=\frac{R}{2}.
\]

Thus $L_c$ is the characteristic radial distance: it is of order the rod
radius $R$. The factor of $1/2$ comes from the standard volume-to-surface-area
definition $L_c=V/A_s$ applied to a cylindrical element.

A cylinder has two independent geometric lengths: its radius $R$ and its
length $L$. We must therefore state which length is being used to
nondimensionalize the problem and why:

- The radial scale $R$ (or, with the $V/A_s$ convention, $L_c=R/2$) is used in
  the transverse Biot number because that number tests whether temperature
  variation across a cross section can be neglected.
- The axial scale $L$ is used in $\xi=x/L$ and in $mL$ because those quantities
  describe variation along the rod and whether the far-end boundary affects
  the measured region.

These choices answer different physical questions; one characteristic length
cannot replace the other. A sphere, by contrast, has only one independent
geometric length, its radius $R$. The conventional volume-to-surface-area
length for a sphere is $L_c=V/A_s=R/3$, but it is still set entirely by the
single scale $R$.

Using the same representative temperature difference $\Delta T$ for both
processes, their characteristic heat-transport capacities are

\[
\dot Q_{\mathrm{radial\ conduction}}
\sim \frac{k(P\delta x)}{L_c}\Delta T,
\qquad
\dot Q_{\mathrm{side\ convection}}
\sim h(P\delta x)\Delta T.
\]

Their ratio is

\[
\boxed{
\frac{\dot Q_{\mathrm{side\ convection}}}
{\dot Q_{\mathrm{radial\ conduction}}}
\sim \frac{hL_c}{k}
=\mathrm{Bi}_{\perp}
}.
\]

These are characteristic rates evaluated using the same $\Delta T$, not two
independent actual heat rates. In steady operation, radial conduction to the
surface and convection from the surface occur in series, so their actual rates
must be equal. Equivalently,

\[
\mathrm{Bi}_{\perp}
\sim
\frac{R_{\mathrm{radial\ conduction}}}
{R_{\mathrm{surface\ convection}}}.
\]

When $\mathrm{Bi}_{\perp}\ll1$, radial conduction offers little resistance.
Only a small center-to-surface temperature difference is needed to replace the
heat lost by convection, so each cross section is nearly isothermal.

The comparison between **axial conduction** and **side convection** is a
different dimensionless ratio:

\[
\frac{\dot Q_{\mathrm{side\ convection}}}
{\dot Q_{\mathrm{axial\ conduction}}}
\sim \frac{hPL^2}{kA}
=(mL)^2.
\]

Thus $\mathrm{Bi}_{\perp}$ tests whether radial temperature variation may be
neglected, whereas $(mL)^2$ describes how strongly side cooling competes with
conduction along the rod.

The small-transverse-Biot criterion allows us to use one cross-sectional
temperature \(T(x)\).

## Energy Balance And Differential Equation

An energy balance on a slice of width \(\delta x\) is

\[
-kA\left.\frac{dT}{dx}\right|_{x+\delta x}
+kA\left.\frac{dT}{dx}\right|_x
+hP\delta x\,[T(x)-T_\infty]=0.
\tag{4.28}
\]

As \(\delta x\rightarrow0\),

\[
\frac{
\left.dT/dx\right|_{x+\delta x}
-\left.dT/dx\right|_x
}{\delta x}
\rightarrow
\frac{d^2T}{dx^2}
=\frac{d^2(T-T_\infty)}{dx^2}.
\tag{4.29}
\]

Therefore,

\[
\frac{d^2(T-T_\infty)}{dx^2}
=\frac{hP}{kA}(T-T_\infty).
\tag{4.30}
\]

For a convecting tip,

\[
(T-T_\infty)_{x=0}=T_0-T_\infty,
\qquad
-kA\left.\frac{d(T-T_\infty)}{dx}\right|_{x=L}
=h_LA(T-T_\infty)_{x=L}.
\tag{4.31a}
\]

For an insulated tip,

\[
(T-T_\infty)_{x=0}=T_0-T_\infty,
\qquad
\left.\frac{d(T-T_\infty)}{dx}\right|_{x=L}=0.
\tag{4.31b}
\]

## Dimensional Analysis And Dimensionless Form

The dimensional functional relation is

\[
T-T_\infty
=\operatorname{fn}(T_0-T_\infty,x,L,kA,hP,h_LA).
\tag{4.32}
\]

Define

\[
\Theta=\frac{T-T_\infty}{T_0-T_\infty},
\qquad
\xi=\frac{x}{L},
\qquad
m=\sqrt{\frac{hP}{kA}},
\qquad
\mathrm{Bi}_{\mathrm{axial}}=\frac{h_LL}{k}.
\]

Then a convecting-tip fin has

\[
\Theta=\operatorname{fn}
\left(\xi,mL,\mathrm{Bi}_{\mathrm{axial}}\right),
\tag{4.33a}
\]

whereas an adiabatic-tip fin has

\[
\Theta=\operatorname{fn}(\xi,mL).
\tag{4.33b}
\]

### Choosing A Dimensionless Position Coordinate

The quantity $m$ is not itself a dimensionless coordinate: it has units of
inverse length. Both

\[
\xi=\frac{x}{L}
\qquad\text{and}\qquad
X=mx=\frac{x}{1/m}
\]

are valid dimensionless coordinates, but they emphasize different length
scales. The rod length $L$ is the geometric scale, whereas $1/m$ is the
thermal decay length set by axial conduction and side cooling.

For a finite rod, $\xi=x/L$ is convenient because the base is always at
$\xi=0$ and the tip is always at $\xi=1$. The physics then appears in the
separate dimensionless group

\[
mL=\frac{L}{1/m},
\]

which compares the rod length with the thermal decay length. We could instead
use $X=mx$. Equation (4.34) would then become

\[
\frac{d^2\Theta}{dX^2}=\Theta,
\]

but the tip would be located at $X=mL$ rather than at a fixed coordinate.
Nothing physical changes because $X=(mL)\xi$; the two choices merely organize
the same information differently. When the rod is effectively infinite and
the tip no longer matters, $mx$ becomes the natural coordinate and the solution
is $\Theta=e^{-mx}$.

[Lienhard, p. 167, Eqs. (4.32)-(4.33b)](../../references/lienhard-heat-transfer-textbook-v6.pdf#page=181)
uses $\xi=x/L$ for the finite-fin dimensional analysis. On
[p. 173, Eq. (4.50)](../../references/lienhard-heat-transfer-textbook-v6.pdf#page=187),
the long-fin limit is written as $e^{-mL\xi}=e^{-mx}$, and the following
paragraph interprets $(mL)^2$ as a hybrid Biot number comparing axial
conduction resistance with the overall resistance to side convection.

### Why The Axial Biot Number Disappears For An Adiabatic Tip

For a convecting tip, $h_L$ enters through the tip boundary condition:

\[
-\left.\frac{d\Theta}{d\xi}\right|_{\xi=1}
=\underbrace{\frac{h_LL}{k}}_{\mathrm{Bi}_{\mathrm{axial}}}\Theta(1).
\]

Thus $\mathrm{Bi}_{\mathrm{axial}}$ measures the strength of convection from
the tip relative to axial conduction. For an adiabatic tip, the heat flux at
the tip is zero:

\[
\left.\frac{d\Theta}{d\xi}\right|_{\xi=1}=0.
\]

There is no tip heat-transfer coefficient $h_L$ in this boundary condition.
Consequently, $h_L$ is absent from the dimensional functional relation and no
independent axial Biot number can be formed. Equivalently, one may set $h_L=0$
and obtain $\mathrm{Bi}_{\mathrm{axial}}=0$, but saying that the parameter
**drops out of the problem** better expresses the dimensional-analysis logic.
The transverse Biot number does not disappear: it remains the separate test of
whether each cross section can be assigned one temperature.

[Lienhard, p. 167, immediately following Eq. (4.33a)](../../references/lienhard-heat-transfer-textbook-v6.pdf#page=181)
makes this variable-counting argument explicitly: removing $h_L$ leaves one
fewer variable but the same fundamental dimensions, so the corresponding
dimensionless group $\mathrm{Bi}_{\mathrm{axial}}$ is removed, giving
Eq. (4.33b).

The differential equation becomes

\[
\frac{d^2\Theta}{d\xi^2}=(mL)^2\Theta.
\tag{4.34}
\]

Its general solution is

\[
\Theta=C_1e^{mL\xi}+C_2e^{-mL\xi}.
\tag{4.35}
\]

<details class="note" markdown="1">
<summary><strong>Sidebar: Finite Rod With An Insulated Tip</strong></summary>

The dimensionless boundary conditions are

\[
\Theta(0)=1,
\qquad
\left.\frac{d\Theta}{d\xi}\right|_{\xi=1}=0.
\tag{4.36}
\]

Substitution into the general solution gives

\[
C_1+C_2=1,
\qquad
C_1e^{mL}-C_2e^{-mL}=0.
\tag{4.37}
\]

The hyperbolic functions used to simplify the result are

\[
\begin{aligned}
\sinh z&=\frac{e^z-e^{-z}}{2},&
\cosh z&=\frac{e^z+e^{-z}}{2},\\
\tanh z&=\frac{\sinh z}{\cosh z},&
\coth z&=\frac{\cosh z}{\sinh z}.
\end{aligned}
\tag{4.38}
\]

Their needed derivatives are

\[
\frac{d}{dz}\sinh z=\cosh z,
\qquad
\frac{d}{dz}\cosh z=\sinh z.
\tag{4.39}
\]

The constants are

\[
C_1=\frac{e^{-mL}}{2\cosh(mL)},
\qquad
C_2=1-\frac{e^{-mL}}{2\cosh(mL)}.
\tag{4.40}
\]

The finite insulated-tip temperature distribution is

\[
\Theta(\xi)
=\frac{\cosh[mL(1-\xi)]}{\cosh(mL)}
=\frac{\cosh[m(L-x)]}{\cosh(mL)}.
\tag{4.41}
\]

The heat-transfer rate at the base is

\[
\dot Q_0
=-kA\left.\frac{d(T-T_\infty)}{dx}\right|_{x=0}.
\tag{4.42}
\]

Thus,

\[
\frac{\dot Q_0L}{kA(T_0-T_\infty)}
=mL\frac{\sinh(mL)}{\cosh(mL)}
=mL\tanh(mL),
\tag{4.43}
\]

or

\[
\frac{\dot Q_0}
{\sqrt{kAhP}\,(T_0-T_\infty)}
=\tanh(mL).
\tag{4.44}
\]

At the tip,

\[
\Theta_{\mathrm{tip}}=\frac{1}{\cosh(mL)}.
\tag{4.45}
\]

</details>

<details class="note" markdown="1">
<summary><strong>Sidebar: Exact Convecting-Tip Solution</strong></summary>

The dimensionless boundary conditions become

\[
\Theta(0)=1,
\qquad
-\left.\frac{d\Theta}{d\xi}\right|_{\xi=1}
=\mathrm{Bi}_{\mathrm{axial}}\Theta(1).
\tag{4.46}
\]

Substitution into the general solution gives

\[
\begin{aligned}
C_1+C_2&=1,\\
-mL(C_1e^{mL}-C_2e^{-mL})
&=\mathrm{Bi}_{\mathrm{axial}}
(C_1e^{mL}+C_2e^{-mL}).
\end{aligned}
\tag{4.47}
\]

The exact temperature distribution is

\[
\Theta(\xi)
=
\frac{
\cosh[mL(1-\xi)]
+(\mathrm{Bi}_{\mathrm{axial}}/mL)\sinh[mL(1-\xi)]
}{
\cosh(mL)
+(\mathrm{Bi}_{\mathrm{axial}}/mL)\sinh(mL)
}.
\tag{4.48}
\]

The corresponding base heat rate is

\[
\frac{\dot Q_0}
{\sqrt{kAhP}\,(T_0-T_\infty)}
=
\frac{
(\mathrm{Bi}_{\mathrm{axial}}/mL)+\tanh(mL)
}{
1+(\mathrm{Bi}_{\mathrm{axial}}/mL)\tanh(mL)
}.
\tag{4.49}
\]

</details>

## Infinite-Rod Limit

When \(mL\gg1\), the finite solution approaches

\[
\lim_{mL\rightarrow\infty}\Theta
=e^{-mL\xi}
=e^{-mx}.
\tag{4.50}
\]

The base heat rate becomes

\[
\dot Q_0=\sqrt{kAhP}\,(T_0-T_\infty).
\tag{4.51}
\]

Lienhard recommends \(mL\gtrsim5\) when using the infinite-fin approximation
for temperature and \(mL\gtrsim3\) when using it for the base heat rate. In
In Module 7, Part III, you will calculate the actual finite-versus-infinite error at every
sensor rather than relying only on these general thresholds.

## What To Be Able To Explain

1. Why does Eq. (4.27) concern the **radius**, whereas \(mL\) concerns the
   **length**?
2. Which term in Eq. (4.28) represents side heat loss?
3. What physical assumption changes Eq. (4.31a) into Eq. (4.31b)?
4. How does Eq. (4.41) retain information about the far end?
5. Why is Eq. (4.50) an approximation rather than a new physical law?
6. Starting from Eq. (4.28), derive Eq. (4.30) and check every term's units.
7. Starting from the general solution, use the base and insulated-tip boundary
   conditions to obtain Eq. (4.41).
8. Show mathematically how Eq. (4.41) approaches Eq. (4.50) when the far end
   becomes irrelevant.

These are assessed in the [A4 written derivation](../lab-08/index.md#a4-finite-length-and-small-biot-guided-study)
and may be sampled in the C5 oral check. Understanding the derivation matters
more than reproducing a long sequence of algebra from memory.
