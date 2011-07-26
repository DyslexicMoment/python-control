# genswitch_plot.m - run the Collins genetic switch model
# RMM, 24 Jan 07
#
# This file contains an example from FBS of a simple dynamical model
# of a genetic switch.  Plots time traces and a phase portrait using
# the python-control library.

import numpy as np
import matplotlib.pyplot as mpl
from scipy.integrate import odeint
from matplotlib.mlab import frange
from control import PhasePlot, boxgrid

# Simple model of a genetic switch
#
# This function implements the basic model of the genetic switch
# Parameters taken from Gardner, Cantor and Collins, Nature, 2000
def genswitch(y, t, mu=4, n=2):
    return (mu / (1 + y[1]**n) - y[0], mu / (1 + y[0]**n) - y[1])

# Run a simulation from an initial condition
tim1 = np.linspace(0, 10, 100)
sol1 = odeint(genswitch, [1, 5], tim1)

# Extract the equlibirum points
mu = 4; n = 2;			# switch parameters
eqpt = np.empty(3);
eqpt[0] = sol1[0,-1]
eqpt[1] = sol1[1,-1]
eqpt[2] = 0;                    # fzero(@(x) mu/(1+x^2) - x, 2);

# Run another simulation showing switching behavior
tim2 = np.linspace(11, 25, 100);
sol2 = odeint(genswitch, sol1[-1,:] + [2, -2], tim2)

# First plot out the curves that define the equilibria
u = frange(0, 4.5, 0.1)
f = np.divide(mu, (1 + u**n))   # mu / (1 + u^n), elementwise

mpl.figure(1); mpl.clf();
mpl.axis([0, 5, 0, 5]);                 # box on;
mpl.plot(u, f, '-', f, u, '--')         # 'LineWidth', AM_data_linewidth);
mpl.legend('z1, f(z1)', 'z2, f(z2)')    # legend(lgh, 'boxoff');
mpl.plot([0, 3], [0, 3], 'k-')          # 'LineWidth', AM_ref_linewidth);
mpl.plot(eqpt[0], eqpt[1], 'k.', eqpt[1], eqpt[0], 'k.', 
         eqpt[2], eqpt[2], 'k.')        # 'MarkerSize', AM_data_markersize*3);
mpl.xlabel('z1, f(z2)');
mpl.ylabel('z2, f(z1)');

# Time traces
mpl.figure(3); mpl.clf(); # subplot(221);
mpl.plot(tim1, sol1[:,0], 'b-', tim1, sol1[:,1], 'g--');
# set(pl, 'LineWidth', AM_data_linewidth);
mpl.hold(True);
mpl.plot([tim1[-1], tim1[-1]+1], 
         [sol1[-1,0], sol2[0,1]], 'ko:', 
         [tim1[-1], tim1[-1]+1], [sol1[-1,1], sol2[0,0]], 'ko:');
# set(pl, 'LineWidth', AM_data_linewidth, 'MarkerSize', AM_data_markersize);
mpl.plot(tim2, sol2[:,0], 'b-', tim2, sol2[:,1], 'g--');
# set(pl, 'LineWidth', AM_data_linewidth);
mpl.axis([0, 25, 0, 5]);

mpl.xlabel('Time {\itt} [scaled]');
mpl.ylabel('Protein concentrations [scaled]');
mpl.legend('z1 (A)', 'z2 (B)')  # 'Orientation', 'horizontal');
# legend(legh, 'boxoff');

# Phase portrait
mpl.figure(2); mpl.clf(); # subplot(221);
mpl.axis([0, 5, 0, 5]);         # set(gca, 'DataAspectRatio', [1, 1, 1]);
PhasePlot(genswitch, X0 = boxgrid([0, 5, 6], [0, 5, 6]), T = 10, 
          timepts = [0.2, 0.6, 1.2])

# Add the stable equilibrium points
mpl.hold(True);
mpl.plot(eqpt[0], eqpt[1], 'k.', eqpt[1], eqpt[0], 'k.', 
  eqpt[2], eqpt[2], 'k.')       # 'MarkerSize', AM_data_markersize*3);

mpl.xlabel('Protein A [scaled]');
mpl.ylabel('Protein B [scaled]');       # 'Rotation', 90);
