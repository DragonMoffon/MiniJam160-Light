from math import pi, tau, ceil, exp, cos, cosh

from typing import TypeVar, Protocol, Optional


__all__ = (
    'SecondOrderAnimatorBase',
    'ProceduralAnimator',
    'SecondOrderAnimator',
    'SecondOrderAnimatorTCritical',
    'SecondOrderAnimatorKClamped',
    'SecondOrderAnimatorPoleZero',
    'update_default_animator'
)


class Animatable(Protocol):

    def __mul__(self, other):
        ...

    def __add__(self, other):
        ...

    def __sub__(self, other):
        ...


A = TypeVar('A', bound=Animatable)


class SecondOrderAnimatorBase:

    def __init__(self, frequency: float, damping: float, response: float,  x_initial: A, y_initial: A, y_d_initial: A):
        self.xp: Animatable = x_initial
        self.y: Animatable = y_initial
        self.dy: Optional[Animatable] = y_d_initial

        self._freq = frequency
        self._damp = damping
        self._resp = response

        self.k1: float = damping / (pi * frequency)
        self.k2: float = 1.0 / (tau * frequency) ** 2.0
        self.k3: float = (response * damping) / (tau * frequency)

    def update_frequency(self, new_frequency):
        self._freq = new_frequency
        self.calc_k_vals()

    def update_damping(self, new_damping):
        self._damp = new_damping
        self.calc_k_vals()

    def update_response(self, new_response):
        self._resp = new_response
        self.calc_k_vals()

    def update_values(self, new_frequency: Optional[A] = None, new_damping: Optional[A] = None, new_response: Optional[A] = None):
        self._freq = new_frequency or self._freq
        self._damp = new_damping or self._damp
        self._resp = new_response or self._resp

        self.calc_k_vals()

    def calc_k_vals(self):
        self.k1 = self._damp / (pi * self._freq)
        self.k2 = 1.0 / (tau * self._freq)**2.0
        self.k3 = (self._resp * self._damp) / (tau * self._freq)

    def update(self, dt: float, nx: A, dx: Optional[A] = None):
        raise NotImplementedError()


class SecondOrderAnimator(SecondOrderAnimatorBase):
    """
    The most basic implementation of the second order procedural animator.

    Has stability issues that can cause jittering at high frequencies,
    and the sim can explode with lag spikes.
    """

    def update(self, dt: float, nx: A, dx: Optional[A] = None):
        dx = dx or (nx - self.xp) / dt
        self.xp = nx
        self.y = self.y + self.dy * dt
        self.dy = self.dy + (self.xp + dx * self.k3 - self.y - self.dy * self.k1) * dt / self.k2

        return self.y


class SecondOrderAnimatorTCritical(SecondOrderAnimatorBase):
    """
    A slightly more complex implementation which tries to stay physically accurate.

    By adding extra smaller iteration steps when the delta time gets too large,
    the sim won't explode with lag spikes, but it adds extra calc steps.
    """

    def __init__(self, frequency: float, damping: float, response: float, x_initial: A, y_initial: A, y_d_initial: A):
        super().__init__(frequency, damping, response, x_initial, y_initial, y_d_initial)
        self.T_crit = 0.8 * ((4.0 * self.k2 + self.k1 * self.k1)**0.5 - self.k1)

    def calc_k_vals(self):
        super().calc_k_vals()
        self.T_crit = 0.8 * ((4.0 * self.k2 + self.k1 * self.k1)**0.5 - self.k1)

    def update(self, dt: float, nx: A, dx: Optional[A] = None):
        dx = dx or (nx - self.xp) / dt
        self.xp = nx

        # Because we may be doing a bunch of iterations we don't want to use dot notation so much
        x, y, dy, k1, k2, k3 = self.xp, self.y, self.dy, self.k1, self.k2, self.k3

        # If the time step is above the critical time step it will freak out so lets make it happier
        iterations = int(ceil(dt / self.T_crit))
        dt = dt / iterations
        for _ in range(iterations):
            y = y + dy * dt
            dy = dy + (x + dx * k3 - y - dy * k1) * dt / k2

        self.y, self.dy = y, dy
        return y


class SecondOrderAnimatorKClamped(SecondOrderAnimatorBase):
    """
    A version of the sim that prioritises stability over physical accuracy.

    by changing the k2 value based on the delta_time it is possible to eliminate
    both sim explosions with lag spikes, and jittering at high frequencies.
    """

    def update(self, dt: float, nx: A, dx: Optional[A] = None):
        if not dt:
            return self.y

        dx = dx or (nx - self.xp) / dt
        self.xp = nx
        # Clamping k2 it isn't physically correct, but protects against the sim collapsing with lag spikes.
        k2_stable = max(self.k2, dt*dt/2.0 + dt*self.k1/2.0, dt*self.k1)

        self.y = self.y + self.dy * dt
        self.dy = self.dy + (self.xp + dx * self.k3 - self.y - self.dy * self.k1) * dt / k2_stable

        return self.y


class SecondOrderAnimatorPoleZero(SecondOrderAnimatorBase):
    """
    The most complex version of the sim that is more accurate for higher speeds.

    By using a more complex algorithm to calc both k1 and k2 each frame lag
    spikes, jittering, and fast movement can all be improved.

    This adds alot of extra computation each frame, and may not be worth it.
    """

    def __init__(self, frequency: float, damping: float, response: float, x_initial: A, y_initial: A, y_d_initial: A):
        super().__init__(frequency, damping, response, x_initial, y_initial, y_d_initial)
        self._w = tau * frequency
        self._d = self._w * (abs(damping * damping - 1.0))

    def calc_k_vals(self):
        super().calc_k_vals()
        self._w = tau * self._freq
        self._d = self._w * (abs(self._damp * self._damp - 1.0))

    def update(self, dt: float, nx: A, dx: Optional[A] = None):
        dx = dx or (nx - self.xp) / dt
        self.xp = nx
        if self._w * dt < self._damp:
            k1_stable = self.k1
            k2_stable = max(self.k2, dt*dt/2.0 + dt*k1_stable/2.0, dt*k1_stable)
        else:
            t1 = exp(-self._damp * self._w * dt)
            alpha = 2.0 * t1 * (cos(dt * self._d) if self._damp <= 1.0 else cosh(dt * self._d))
            beta = t1 * t1
            t2 = dt / (1 + beta - alpha)
            k1_stable = (1 - beta) * t2
            k2_stable = dt * t2

        self.y = self.y + self.dy * dt
        self.dy = self.dy + (self.xp + dx * self.k3 - self.y - self.dy * k1_stable) * dt / k2_stable

        return self.y


ProceduralAnimator = SecondOrderAnimatorKClamped


def update_default_animator(new_default: type):
    assert issubclass(new_default, SecondOrderAnimatorBase)
    global ProceduralAnimator
    ProceduralAnimator = new_default
