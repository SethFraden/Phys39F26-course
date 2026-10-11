# Module 6, Part II: TEC Process Model And The Simulation

This is the second part of Module 6. Complete
[Part I: P/PI Control And Lumped Modeling](../lab-06/index.md) first.
Both parts use the same prepared
[simulation](#how-to-run-the-python-gui): Part I emphasizes
the one-lump model, while Part II compares the one- and two-lump models.

## Introductory Material

### Purpose

This part follows the first Module 6 modeling work and the initial physical PI
implementation. Before beginning Part II, complete the physical $K_p$ and
$K_i$ study and generate the comparison plots required by [Module 6, Part I,
A3 Question 5](../lab-06/index.md#a3-question-5). Part II connects three
things:

1. the physical TEC/block/thermistor system,
2. the feedback-control equations,
3. a [Python simulation GUI](#how-to-run-the-python-gui) that lets you change
   model parameters and watch the predicted temperature response.

This module is not about perfect quantitative prediction. It is about learning
how a simple model can qualitatively or semi-quantitatively explain droop,
overshoot, lag, and the onset of instability.

### Learning Objectives

By the end of Module 6, Part II, you should be able to:

- write and interpret the coupled energy balances for the TEC-side and
  measured-block thermal masses;
- show how two coupled first-order temperature equations produce one
  second-order equation for the measured temperature;
- use the two-lump model to explain phase lag, overshoot, and underdamped
  behavior that the one-lump model cannot reproduce;
- predict and verify how $K_p$, the coupling conductance, and the two thermal
  capacitances affect the simulated transient;
- characterize matched physical P and PI responses using rise time,
  overshoot, settling time, steady-state error, and oscillation period; and
- apply and justify a controlled protocol for selecting $K_p$ and $K_i$ by
  connecting theory, simulation, and measurement.

These objectives are assessed through the two-lump derivation and theory
assignment, the Part 3 and Part 6 simulation records, the completed six-run
physical protocol from Part I, and A3 Questions 3 and 5–7.

### Class Theme

**Use Models To Explain Measurements**

In control theory, the **process** is the physical cause-and-effect system that
turns the controller output into a measured response. Here, the PWM command
changes the heat transported by the TEC; thermal capacitances store energy;
thermal conductances move heat through the aluminum block and to the room; and
the thermistor measures the resulting temperature. This chain from PWM command
to measured temperature is the process we are modeling.

### At A Glance

Before class, spend your time in this order:

- **35-45 min**: Read [Lienhard](../../references/lienhard-heat-transfer-textbook-v6.pdf)
  Chapter 1 with emphasis on energy balance, heat flux, conduction, thermal
  resistance, heat capacity, and [lumped models](#lumped-model-figure). Read through p. 28. Skip most of the last section on radiation.
- **20-30 min**: Prepare Problem 1.3 for possible board work and use Problem
  1.8 as a quick review of the one-lump model already developed in Part I.
- **15-20 min**: Run the [Python demo and GUI](#how-to-run-the-python-gui)
  once so class time can focus on interpretation instead of setup.
- **20 min**: Annotate the two-lump equations and review your completed
  physical P/PI plots from Part I.

During class on October 19, the approximate schedule for one 170-minute meeting is:

1. **0-15 min**: Inspect the completed P/PI plots and state what the one-lump
   model explains and fails to explain.
2. **15-35 min**: Opening discussion and board work on
   [Lienhard](../../references/lienhard-heat-transfer-textbook-v6.pdf)
   Problem 1.3 and the one-lump review in Problem 1.8.
3. **35-70 min**: Develop the coupled two-lump balances and reduce them to a
   second-order equation for the measured temperature.
4. **70-110 min**: Compare one- and two-lump responses and connect thermal lag
   to the experimental plots.
5. **110-140 min**: Vary one parameter at a time and interpret the results
   using the equations.
6. **140-160 min**: Complete the two-lump theory assignment in groups.
7. **160-170 min**: Wrap up: what the model explains, what it leaves out, and
   why the long-rod experiment will require a spatial model.

### Outside-Class Workload Budget

| Session | Work | Planned time |
| --- | --- | ---: |
| S14 | Read this assignment and the selected Lienhard Chapter 1 material | 45 minutes |
| S14 | Prepare Problem 1.3 and review Problem 1.8 | 30 minutes |
| S14 | Run the simulation, annotate the two-lump equations, and organize the completed P/PI plots | 40 minutes |
| S14 | **Total associated with S14** | **1 hour 55 minutes** |
| S15 | Complete the model comparisons and A3 evidence | 120 minutes |
| S15 | Complete the two-lump theory assignment | 45 minutes |
| S15 | Commit, push, and prepare the A3 submission | 45 minutes |
| S15 | **Total associated with S15** | **3 hours 30 minutes** |

The Chapter 1 time is for reading with equations and physical interpretation,
not for a quick skim. The optional extension is not part of the four-hour
budget and should be attempted only after required work is complete.

### Vocabulary

- **Process**: the physical system being controlled. Here, the process is the
  TEC/block/thermistor thermal system.
- **State variable**: a number that describes the current state of the model,
  such as temperature.
- **Heat**: energy transferred because of a temperature difference. Heat is not
  the same thing as temperature; temperature tells how hot something is, while
  heat is energy moving into or out of the system.
- **Lumped model**: a model that treats an extended object as if the entire
  object were at the same temperature. The lump can be viewed as a point
  object of finite thermal mass. See the [one-lump/two-lump
  figure](#lumped-model-figure).
- **Thermal mass**: a synonym for heat capacity. A larger thermal mass changes
  temperature more slowly.
- **Thermal lag**: delay between changing the actuator and observing the
  measured temperature response.
- **Droop**: steady-state error in proportional-only control.
- **Saturation**: the actuator command reaches its limit, such as PWM 255. This could be a physical or software imposed limit.

### Model Equations And Numerical Algorithm

The [Python GUI](#how-to-run-the-python-gui) separates the physical model
from the controller. Select either a one-lump or two-lump process, then select
open-loop, P, or PI control.

#### One-Lump Physical Model

<details class="note" markdown="1">
<summary><strong>Symbols Used In Module 6, Part II</strong></summary>

| Symbol | Meaning | Units |
| --- | --- | --- |
| $T$ | One-lump temperature, or TEC-side temperature in the two-lump model | $^\circ$C |
| $T_m$ | Measured-block temperature in the two-lump model | $^\circ$C |
| $T_{\mathrm{amb}}$ | Ambient room temperature | $^\circ$C |
| $T_{\mathrm{set}}$ | Controller setpoint | $^\circ$C |
| $C$ | One-lump thermal capacitance, $C=C_T+C_m$ | J/K |
| $C_T$ | TEC-side thermal capacitance | J/K |
| $C_m$ | Measured-block thermal capacitance | J/K |
| $G$ | Passive thermal conductance between the two lumps | W/K |
| $H$ | Passive thermal conductance from the measured lump to the room | W/K |
| $u$ | Signed PWM command | PWM counts |
| $P_u$ | TEC thermal-power coefficient for the active direction | W/PWM count |
| $P_{u,h}$, $P_{u,c}$ | Heating and cooling thermal-power coefficients | W/PWM count |
| $\chi_h$, $\chi_c$ | Heating and cooling susceptibilities | $^\circ$C/PWM count |
| $r=\chi_h/\chi_c$ | Heating-to-cooling susceptibility ratio | dimensionless |
| $e=T_{\mathrm{set}}-T_{\mathrm{meas}}$ | Temperature error | $^\circ$C |
| $K_p$ | Proportional gain | PWM counts/$^\circ$C |
| $K_i$ | Integral gain | PWM counts/($^\circ$C s) |
| $\Delta t$ | Numerical time step | s |
| $\theta_T$, $\theta_m$ | Deviations from the steady-state temperatures | $^\circ$C |

</details>

The one-lump model treats the TEC-side region and the measured block as one
temperature. If their separate thermal capacitances are $C_T$ and $C_m$, the
combined thermal capacitance is

\[
C=C_T+C_m,
\qquad
C\frac{dT}{dt}=P_u(u)u-H(T-T_{\mathrm{amb}}).
\]

Every term has units of watts. The TEC coefficient is piecewise: the program
uses $P_{u,h}$ for a positive heating command and $P_{u,c}$ for a negative
cooling command. Their ratio is

\[
r=\frac{P_{u,h}}{P_{u,c}}=\frac{\chi_h}{\chi_c}.
\]

#### Two-Lump Physical Model

The two-lump model separates the TEC-side temperature $T$ from the measured
temperature $T_m$:

\[
C_T\frac{dT}{dt}=P_u(u)u-G(T-T_m),
\]

\[
C_m\frac{dT_m}{dt}=G(T-T_m)-H(T_m-T_{\mathrm{amb}}).
\]

Here $C_T$ and $C_m$ are thermal capacitances. The conductance $G$ couples the
two lumps through the passive heat flow $G(T-T_m)$. The same heat that leaves
the TEC-side lump enters the measured lump, so this term appears with opposite
signs in the two equations. We simplify the apparatus by giving the TEC-side
lump no separate path to the room; all heat loss to the room is represented by
$H(T_m-T_{\mathrm{amb}})$ in the measured-lump equation.

The controller responds to $T_m$, but $T$ and $T_m$ do not change at the same
time. Which temperature changes first if someone opens a window and
$T_{\mathrm{amb}}$ suddenly decreases? Which changes first if
$T_{\mathrm{set}}$ changes? This lag can produce overshoot or oscillation.

#### From Two First-Order Equations To One Second-Order Equation

Consider one heating or cooling direction so that $P_u$ is constant, assume
the PWM is not saturated, and use P control:

\[
u=K_p(T_{\mathrm{set}}-T_m).
\]

Let $\theta_T$ and $\theta_m$ be deviations of $T$ and $T_m$ from their
steady-state values. The constant steady-state terms cancel, leaving

\[
C_T\dot\theta_T=-G\theta_T+(G-P_uK_p)\theta_m,
\]

\[
C_m\dot\theta_m=G\theta_T-(G+H)\theta_m.
\]

The second equation gives the hidden TEC-side temperature in terms of the
measured temperature and its rate of change:

\[
G\theta_T=C_m\dot\theta_m+(G+H)\theta_m.
\]

Differentiate the second equation, use the first equation to replace
$\dot\theta_T$, and then use the expression above to replace $\theta_T$. The
result is one second-order differential equation for the measured temperature:

\[
\boxed{
C_TC_m\ddot\theta_m+
\left[C_T(G+H)+C_mG\right]\dot\theta_m+
G(H+P_uK_p)\theta_m=0.
}
\]

Thus two coupled first-order equations for two stored-energy states are
equivalent to one second-order equation for $T_m$. Substituting
$\theta_m\propto e^{st}$ gives

\[
C_TC_m s^2+
\left[C_T(G+H)+C_mG\right]s+
G(H+P_uK_p)=0.
\]

Depending on the parameters, the two eigenvalues can be real or a complex
conjugate pair. Complex eigenvalues produce an underdamped transient even
though the apparatus contains no mechanical momentum.

At steady state, both temperature derivatives are zero, so

\[
P_u u=G(T-T_m)=H(T_m-T_{\mathrm{amb}}).
\]

The internal conductance $G$ sets the temperature difference between the two
lumps, but it cancels from the overall balance
$P_u u=H(T_m-T_{\mathrm{amb}})$. This is the quantitative reason the one-lump
model can predict the final measured temperature and P-control droop even when
it fails to predict the high-gain transient.

#### Controller Choices

The measured temperature is $T$ for the one-lump model and $T_m$ for the
two-lump model. Define

\[
e=T_{\mathrm{set}}-T_{\mathrm{meas}}.
\]

The three controller choices are

\[
u=u_{\mathrm{user}}\quad\text{(open loop)},
\]

\[
u=K_pe\quad\text{(P control)},
\]

\[
u=K_pe+K_i\int e\,dt=u_P+u_I\quad\text{(PI control)}.
\]

The signed command is clamped to the PWM limit. If the anti-windup option is
enabled, the program prevents the integral state from continuing to grow when
the actuator is saturated in the same direction as the error.

#### What The Algorithm Does At Each Time Step

The simulation described in [How To Run The Python
GUI](#how-to-run-the-python-gui) performs the numerical work, but you should
understand its sequence:

1. Read the model's measured temperature, $T_n$ or $T_{m,n}$.
2. Calculate the error $e_n$.
3. For PI control, propose the integral update
   $q_{n+1}=q_n+e_n\Delta t$. Accept it unless anti-windup prevents the
   update; otherwise use $q_{n+1}=q_n$.
4. Calculate the requested command for the selected controller:
   $u_n=u_{\mathrm{user}}$ for open-loop control, $u_n=K_pe_n$ for P control,
   or $u_n=K_pe_n+K_iq_{n+1}$ for PI control.
5. Clamp $u_n$ to the signed PWM limit.
6. Select $P_{u,h}$ or $P_{u,c}$ from the sign of the applied command.
7. Evaluate the heat-balance derivatives and advance $T$ and, for the
   two-lump model, $T_m$ by one Euler step.

For example, the first two-lump Euler updates are

\[
T_{n+1}=T_n+\frac{\Delta t}{C_T}
\left[P_u(u_n)u_n-G(T_n-T_{m,n})\right],
\]

\[
T_{m,n+1}=T_{m,n}+\frac{\Delta t}{C_m}
\left[G(T_n-T_{m,n})-H(T_{m,n}-T_{\mathrm{amb}})\right].
\]

You are not required to write this code. Use it to develop physical intuition:
vary one model, parameter, or initial condition at a time; predict the result;
observe the response; and interpret it using the heat balances and controller
equations.

<a id="lumped-model-figure"></a>

![One-lump and two-lump thermal models](../../assets/lumped_thermal_models.svg)

*Course-specific lumped-model diagram.*

### Thermal Transport Theory Assignments

This part of the course uses **lumped thermal models**. A lumped model assumes
that one object, such as the TEC/block assembly, can be described by one
temperature. This is an approximation. It is useful before we move to the long
rod, where temperature depends on position.

#### One-Lump Results Carried Forward From Part I

In [Module 6, Part I](../lab-06/index.md#part-2-express-the-one-lump-model-using-measured-parameters),
you derived the one-lump energy balance, expressed it using the measured
$\chi$ and $\tau$, and found its steady-state temperature. Use those results
here; do not repeat that assignment.

#### Two-Lump Theory Assignment

The one-temperature model assumes that the measured temperature instantly equals
the actuator-side temperature. The next model separates them:

```text
T  = actuator-side TEC/block temperature
Tm = measured thermistor/block temperature
```

A simple two-temperature model is:

```text
C_T dT/dt  = Q_tec - G*(T - Tm)
C_m dTm/dt = G*(T - Tm) - H*(Tm - T_amb)
```

Here `C_T` and `C_m` are heat capacities in J/°C, `G` is the conductance
between the two lumps, and `H` is the conductance from the measured lump to
the room. Each term has units of W. The left side is a rate of thermal-energy
change. The right side is the sum of heat flows into and out of each lump.

Do this before class:

1. Identify which term transfers heat from the TEC side to the measured
   thermistor/block side.
2. Identify which term describes heat loss from the measured block to room air.
3. Explain why `Tm` can lag behind `T`.
4. Explain why a controller that uses `Tm` may react too late.
5. Starting from the two coupled first-order equations, reproduce the
   elimination that gives the second-order equation for $T_m$. In particular,
   show how the measured-lump equation gives
   $G\theta_T=C_m\dot\theta_m+(G+H)\theta_m$, and use it to eliminate
   $\theta_T$.
6. Divide the measured-lump equation by $C_m$ and compare it term by term with
   the rate-constant form
   $dT_m/dt=k_{21}(T-T_m)-k_m(T_m-T_{\mathrm{amb}})$. Identify
   $k_{21}=G/C_m$ and $k_m=H/C_m$, give their units, and explain how increasing
   each one changes the equilibration between the lumps or the relaxation
   toward room temperature.

#### Later In The Course: Differential Equations In Space

The two-lump model is a crude spatial approximation. It replaces an extended
apparatus with two internally uniform regions connected by a thermal
conductance. It distinguishes a region near the TEC from a region near the
thermistor, but it contains no continuous distance, temperature gradient, or
spatial coordinate.

The long-rod experiment cannot be described by a single temperature. It will
need a temperature field. In its simplest form as a long, thin rod,
temperature depends only on longitudinal position and is independent of
radius.

\[
T = T(x,t)
\]

For the rod we will move toward diffusion equations of the form:

\[
\frac{\partial T}{\partial t}
=
\alpha \frac{\partial^2 T}{\partial x^2}
\]

and, for a rod exchanging heat with the room from its sides, a term that pulls the rod toward room
temperature:

\[
\frac{\partial T}{\partial t}
=
\alpha \frac{\partial^2 T}{\partial x^2}
-
\beta\left(T - T_{\mathrm{room}}\right)
\]

In these equations, `alpha` is the thermal diffusivity in m²/s and `beta` is a
side-loss rate constant in 1/s.

You do not need to solve these equations in Module 6. For now, your job is to
understand how conservation of energy produces the simple lumped equations. The
spatial differential equations come later, when we measure temperature along the
long metal cylinder.

## Pre-Class Assignment

### How To Run The Python GUI

Clicking the Python source-code link opens or downloads the `.py` file. It does
not run the simulation. To run the model, download the file and run it from a
folder on your own computer.

First make a working folder and put the Python file there:

```bash
mkdir -p ~/phys39-lab7
cd ~/phys39-lab7
```

Download this file into that folder:
[Lab_6_7_modeling_tec.py](../../downloads/Lab_6_7_modeling_tec.py).

Set up Python the first time you use this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install matplotlib
```

Run the non-interactive demo:

```bash
python Lab_6_7_modeling_tec.py --demo --output Lab_6_7_modeling_tec_demo.png
```

This saves a plot in the same folder:

```text
Lab_6_7_modeling_tec_demo.png
```

Then run the desktop GUI:

```bash
python Lab_6_7_modeling_tec.py
```

After the first setup, start from this folder and run:

```bash
cd ~/phys39-lab7
source .venv/bin/activate
python Lab_6_7_modeling_tec.py
```

### Before Class

1. Read [Lienhard](../../references/lienhard-heat-transfer-textbook-v6.pdf),
   **Chapter 1: Introduction**. Focus on the parts that connect directly to
   this module: conservation of energy, heat flux, conduction, thermal resistance,
   heat capacity, and lumped thermal models. Read through p. 28. Skip most of the last section on radiation.

2. Prepare to work selected Chapter 1 problems at the board. You may be randomly
   selected to present one of these:

   - **Problem 1.3**: heat flux through a slab. This reinforces Fourier's law,
     units, and the meaning of a temperature gradient.
   - **Problem 1.8**: cooling of a copper sphere in an air stream. This is the
     cleanest Chapter 1 example of a one-lump first-order temperature model.

   For each problem, be ready to identify the physical system, write the heat
   balance or heat-flow law, check units, and explain what approximation makes
   the problem solvable.

3. Pay special attention to these Chapter 1 examples:

   - **Example 1.1**: conduction through a slab. This is the cleanest worked
     example of Fourier's law and heat flux.
   - **Example 1.2**: a copper slab protected by stainless steel. This is useful
     because the same steady heat flow passes through multiple layers, like
     thermal resistances in series.
   - **Example 1.5**: a thermocouple affected by convection and radiation. This
     is a good reminder that a temperature sensor does not always read the
     temperature you think it reads.

4. Follow [How To Run The Python GUI](#how-to-run-the-python-gui) to download
   and open the prepared simulation:

   ```text
   Lab_6_7_modeling_tec.py
   ```

5. Run the non-interactive demo:

   ```bash
   python Lab_6_7_modeling_tec.py --demo --output Lab_6_7_modeling_tec_demo.png
   ```

6. Look at the generated plot:

   ```text
   Lab_6_7_modeling_tec_demo.png
   ```

   The bottom of the PNG and the terminal output list the model parameters used
   to make the plot. Record those values so the plot is reproducible.

7. Run the [Python GUI](#how-to-run-the-python-gui):

   ```bash
   python Lab_6_7_modeling_tec.py
   ```

8. In your notebook, copy the two-lump model equations and label the meaning of
   each variable.
9. Begin the [Two-Lump Theory Assignment](#two-lump-theory-assignment).

### Pre-Class Questions

Write short answers before class.

1. In open-loop mode, what happens if the signed PWM command is zero?
2. In proportional control, why does the PWM become small when the measured
   temperature gets close to the setpoint?
3. Why must proportional-only control leave a steady-state error?
4. In the two-lump thermal-mass model, why might `T` and `Tm` be different?
5. Which parameter in the model most directly changes the amount of thermal
   lag?

## In-Class Assignment

### What You Will Do

You will:

- run the [Python simulation GUI](#how-to-run-the-python-gui),
- interpret the matched physical P and PI responses completed in Part I,
- identify the physical meaning of each control,
- reproduce droop in proportional control,
- produce overshoot or oscillation by increasing gain or lag,
- compare the one-temperature model to the two-temperature model,
- trace one controlled parameter through the equations and numerical algorithm,
- explain what this model teaches you about the real TEC experiment.

### Part 1: One-Lump Open-Loop Model

Set the physical model to `one_lump` and the controller to `open_loop`.

1. Set the signed PWM command to zero. Run the model and confirm that the
   temperature relaxes toward room temperature.
2. Enter a positive signed PWM command and try several values.
3. Enter a negative signed PWM command and try several values.
4. Record what changes in the temperature plot and the PWM plot.

Answer:

- What term in the equation represents heat exchange with the room?
- What term represents the TEC actuator?
- Why is this not feedback control?

### Part 2: One-Temperature Proportional Model

Set the physical model to `one_lump` and the controller to **P**.

1. Set `T_set` above room temperature.
2. Set a small `Kp`.
3. Run until the trace settles.
4. Record the final temperature, setpoint, error, and approximate PWM.
5. Increase `Kp` and repeat.

Make a table:

| Trial | `T_set` | `Kp` | final `T` | final error | final PWM | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |

Answer:

- Does increasing `Kp` reduce droop?
- Does increasing `Kp` eliminate droop completely?
- What happens when PWM saturates?

### Part 3: Reproduce The Goldilocks P And PI Trends

**The purpose of this exercise is to build an explicit match between experiment
and theory.** A successful comparison does more than produce similar-looking
curves: it identifies which terms and parameters in the model control the
features measured in the experiment, including rise time, droop, overshoot,
and the number and decay of oscillations.

Set the physical model to `two_lump`. Enter your measured values of
$T_{\mathrm{amb}}$, $\chi_c$, $\chi_h$, and $\tau$, and use the same
setpoints, PWM limit, and starting conditions as in your six physical runs.
Your numerical gains may differ from those used by other teams.

The measurements determine the one-lump behavior but do not uniquely determine
the internal two-lump parameters $G$ and $C_T/C$. Use the simulation to find
**one shared set** of these physical parameters that qualitatively reproduces
your experimental progression. Do not choose different physical parameters
for each gain.

1. Set $K_i=0$. Run your experimental low, medium, and high $K_p$ values,
   resetting the simulation before each run. Look for the same progression as
   in your P-only Goldilocks plots: slow response and larger droop, a useful
   compromise, and clear overshoot or ringing.
2. If the progression does not resemble your measurements, vary only $G$ or
   $C_T/C$, predict the effect, and repeat all three P runs. Continue until one
   set of physical parameters gives a reasonable qualitative comparison.
3. Keep those physical parameters fixed. Select `pi`, hold $K_p$ at the value
   used for your three experimental PI runs, and simulate your low, medium,
   and high $K_i$ values. Reset the integral before each run.
4. Look for the PI progression in your Goldilocks plots: slow removal of
   steady-state error, a useful compromise, and excessive overshoot, ringing,
   or saturation.
5. Starting from your shared model, vary one parameter at a time. Determine
   which parameters most strongly change rise time, P-control droop,
   overshoot, and the number and decay of oscillations. Return each parameter
   to the shared value before testing the next one. Test $K_p$, $K_i$, $G$,
   and $C_T/C$ explicitly. You may also perturb $\tau$ or $\chi$ to understand
   sensitivity, but restore their measured values for the final comparison.
6. Save all six simulated responses using the same organization and labels as
   your six experimental plots.

Record the single physical parameter set used for all six simulations:

| $\chi_c$ | $\chi_h$ | $\tau$ | $G$ | $C_T/C$ | Setpoints | PWM limit |
| ---: | ---: | ---: | ---: | ---: | --- | ---: |
|  |  |  |  |  |  |  |

Then compare the six conditions:

| Condition | Controller | $K_p$ | $K_i$ | Experimental behavior | Simulated behavior | Agreement or mismatch |
| --- | --- | ---: | ---: | --- | --- | --- |
| P low | P |  | 0 |  |  |  |
| P medium | P |  | 0 |  |  |  |
| P high | P |  | 0 |  |  |  |
| PI low | PI |  |  |  |  |  |
| PI medium | PI |  |  |  |  |  |
| PI high | PI |  |  |  |  |  |

Summarize the parameter-to-behavior correspondence:

| Observed behavior | Parameter varied | Predicted change | Simulated change | Experimental evidence |
| --- | --- | --- | --- | --- |
| Rise time |  |  |  |  |
| P-control droop |  |  |  |  |
| Overshoot |  |  |  |  |
| Number and decay of oscillations |  |  |  |  |

Answer:

- Which parameters most strongly controlled rise time, P-control droop,
  overshoot, and the number and decay of oscillations? Explain each connection
  using the model equations.
- How did changing $G$ or $C_T/C$ affect lag, overshoot, and ringing?
- Which temperature does the controller use to calculate error, and why does
  that delayed measurement make high gain dangerous?
- Which trends in the six experimental plots did one shared two-lump model
  reproduce successfully?
- What important disagreement remains between simulation and experiment?
- Why would changing the physical model parameters separately for every gain
  weaken the comparison?

### Part 4: Connect The Model To PI Feedback

The same feedback structure can be written in compact mathematical form:

```text
error = setpoint - measured temperature
controller output = proportional part + integral part
process turns controller output into a new temperature
```

For proportional-only control:

```text
output = Kp * error
```

For PI control:

```text
integral = integral + error*dt
output = Kp*error + Ki*integral
```

In your notebook:

1. Draw the feedback loop: setpoint, error, controller, process, measured
   temperature.
2. Identify where the Python model calculates each part.
3. Explain why the integral term should reduce droop.
4. Explain why integral control can overshoot if the actuator saturates.

### Part 5: Complete The Two-Lump Theory Assignment

Finish the [Two-Lump Theory Assignment](#two-lump-theory-assignment). Then
answer:

1. Which model variable is closest to what the thermistor measures?
2. Which model variable is closest to where the TEC applies heat?
3. If the thermistor is moved farther from the TEC, which model parameter should
   change?
4. Why is this still a lumped model rather than a full heat-equation model?

### Part 6: Trace One Parameter Through The Algorithm

Choose one parameter: $C_T$, $C_m$, $G$, $H$, $K_p$, or $K_i$.

1. Identify every model or controller equation containing that parameter.
2. Predict how increasing it will affect the temperature trace, command, error,
   or lag.
3. Pause the simulation, change only that parameter, and resume.
4. Compare the observed change with your prediction.
5. Explain where the parameter enters the Euler-update sequence described
   above.

The goal is to understand how the prepared algorithm represents the physics
and controller, not to modify its source code.

### Part 7: Bridge To The Long Rod

The TEC-only model has no spatial coordinate. The later long-rod experiment
will require a model in which temperature depends on both position and time.

The stationary fin model adds space:

```text
temperature depends on x
heat conducts along the rod
heat leaks from the side of the rod to room air
```

The oscillating fin model adds time-periodic boundary forcing:

```text
base temperature oscillates
amplitude decays with distance
phase lags with distance
```

Answer:

- What is missing from the TEC-only model that the rod model must include?
- Why will the rod experiment need more than one thermistor?
- Why are amplitude and phase more useful than just maximum and minimum
  temperature?

## Post-Class Assignment

### Preserve The Model Evidence

Before leaving S15, save the physical PI tuning table and traces from Part I,
copied equations, completed two-lump theory assignment, parameter tables,
screenshots, algorithm-tracing explanation, and exact run command. Keep the team record in
`docs/module_notes/module_07_process_model.md` and preserve the prepared simulation
program in your repository.

### Oral Review Questions: Process Modeling

Use this modeling question bank to check your understanding and prepare A3:

1. Which physical lag in the apparatus can produce overshoot or oscillation as
   gain increases?
2. Identify one model parameter, give its units, and explain its physical
   effect on the simulated response.

Also prepare the [Module 5 P-control questions](../lab-05/index.md#oral-review-questions-p-control)
and [Module 6 PI-control question](../lab-06/index.md#oral-review-questions-pi-control).

### Model Evidence Record

Keep a short module note containing:

- Your copied and labeled model equations.
- Your one-lump results carried forward from Part I.
- The Two-Lump Theory Assignment.
- Open-loop observations.
- Proportional-control droop table.
- Thermal-mass overshoot/oscillation table.
- Screenshot of the [Python GUI](#how-to-run-the-python-gui).
- Your parameter prediction and algorithm-tracing explanation.
- A paragraph answering:

  ```text
  What did the model explain well, and what would it fail to explain about the
  real TEC hardware?
  ```

## Instructor Notes

- This module is a consolidation point after manual control and P/PI control.
- Keep the emphasis on physical interpretation, not formal control theory.
- Students should leave understanding why delay plus gain causes trouble.
- The long-rod model should be introduced as a preview, not fully derived here
  unless the class is ready.
