from numpy import hstack, ones
import scipy as sp
from sympy import symbols, Dummy, lambdify
from numpy import array, hstack, zeros, linspace, pi, ones, ceil
from numpy.linalg import solve
import sympy.physics.mechanics as mech
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class SecondOrderWithLinearForcing(object):
    """Docstring for Pendulum. """

    def __init__(self, M_func, F_func, parameter_vals, x0, dt=1e-3):

        self._Mfunc = M_func
        self._Ffunc = F_func
        self._dt = dt
        self._parvals = parameter_vals
        self._t = 0.
        self._x = x0
        """A simple pendulum simulator (following EE220C)

        :m: The mass of the pendulum
        :l: the length of the pendulum
        :I: The moment of inertia
        :b: Damper coefficient

        """
        self._state_history = ()


    def __step__(self, u):
        """@todo: Docstring for step.
        :returns: @todo

        """

        def derivative(x, t):
            arguments = hstack((x, u, self._parvals))
            dx = array(solve(self._Mfunc(*arguments),
                self._Ffunc(*arguments))).T[0]

            return dx

        ## The [1] is for getting the value at dt
        self._x = odeint(derivative, self._x, [0, self._dt])[1]
        self._t += self._dt

        #self._x += self._dt * (self._A.dot(self._x) + self._B.dot(u))
        #self._t += self._dt

        self._state_history += ((self._t, self._x, u),)

        return self._x # changed to return whole state - KY
       # return self._x[0]


    def __copy__(self):
        """Copy the object to a new one
        :returns: @todo

        """
        return SecondOrderWithLinearForcing(
                self._A, self._B,
                self._x, self._t, self._dt)


    def __call__(self, u):
        """@todo: Docstring for __call__.
        :returns: @todo

        """
        return self.__step__(u)


def pendulumFactory():

    ## Number of pendulums
    n = 1

    q = mech.dynamicsymbols('q:' + str(n + 1)) ## Generalized coords
    u = mech.dynamicsymbols('u:' + str(n + 1)) ## Generalized speeds
    f = mech.dynamicsymbols('f') ## Force applied to the cart

    m = symbols('m:' + str(n + 1)) ## Mass of each bob
    l = symbols('l:' + str(n + 1)) ## Length of each link
    g, t = symbols('g t') ## Gravity and time

    ## Setup inertial reference frame and define the origin O.
    I = mech.ReferenceFrame('I')
    O = mech.Point('O')
    O.set_vel(I, 0) ## Origin's velocity is zero.

    ## Setup the cart as the first point.
    P0 = mech.Point('P0') ## Hinge point of top link.
    P0.set_pos(O, q[0] * I.x) ## Set the position of P0.
    P0.set_vel(I, u[0] * I.x) ## Set the velocity of P0.
    Pa0 = mech.Particle('Pa0', P0, m[0]) ## Define a particle at P0.

    ## Define the frames, particles, forces, and kinematic equations. This
    ## allows for general n pendulum linkages.
    frames = [I]
    points = [P0]
    particles = [Pa0]
    forces = [(P0, f * I.x - m[0] * g * I.y)]
    kindiffs = [q[0].diff(t) - u[0]]

    for i in range(n):
        ## Setup and add frame.
        Bi = I.orientnew('B' + str(i), 'Axis', [q[i + 1], I.z])
        Bi.set_ang_vel(I, u[i + 1] * I.z)
        frames.append(Bi)

        ## Setup and add point for hinge.
        Pi = points[-1].locatenew('P' + str(i + 1), l[i] * Bi.x)
        Pi.v2pt_theory(points[-1], I, Bi)
        points.append(Pi)

        ## Inertial properties of each link.
        Pai = mech.Particle('Pa' + str(i + 1), Pi, m[i + 1])
        particles.append(Pai)

        ## Define force applied per point and the kinematic ODE:
        ## dq_i / dt - u_i = 0
        forces.append((Pi, -m[i + 1] * g * I.y))
        kindiffs.append(q[i + 1].diff(t) - u[i + 1])

    ## Use KanesMethod class to derive the equations of motion.
    kane = mech.KanesMethod(I, q_ind=q, u_ind=u, kd_eqs=kindiffs)
    fr, frstar = kane.kanes_equations(forces, particles)

    ## Setup simulation.
    arm_length = 1. / n
    bob_mass = 0.01 / n
    parameters = [g, m[0]]
    parameter_vals = [9.81, 0.01 / n]
    for i in range(n):
        parameters += [l[i], m[i + 1]]
        parameter_vals += [arm_length, bob_mass]

    dynamic = q + u
    dynamic.append(f)
    dummy_symbols = [Dummy() for i in dynamic]
    dummy_dict = dict(zip(dynamic, dummy_symbols))
    kindiff_dict = kane.kindiffdict()
    M = kane.mass_matrix_full.subs(kindiff_dict).subs(dummy_dict)
    F = kane.forcing_full.subs(kindiff_dict).subs(dummy_dict)
    M_func = lambdify(dummy_symbols + parameters, M)
    F_func = lambdify(dummy_symbols + parameters, F)

    ## Set dt
    dt = 0.01

    ## Set up initial conditions.
    ## [position of cart, angle of pendulum, velocity of cart, angular
    ##  velocity]
    x0 = hstack((0, pi / 2 * ones(n) + pi / 4,
        1e-3 * ones((n + 1))))

    return SecondOrderWithLinearForcing(M_func, F_func, parameter_vals, x0,
           dt=dt)

if __name__ == '__main__':
    myPend = pendulumFactory()
    us = zeros(1000)

    for u in us:
        myPend(u)

    xs = [x for _, x, _ in myPend._state_history]
    us = [u for _, _, u in myPend._state_history]

    plt.plot([p for p, a, _, _ in xs])
    plt.figure()
    plt.plot([a for p, a, _, _ in xs])
    plt.figure()
    plt.plot(us)
    plt.show()
