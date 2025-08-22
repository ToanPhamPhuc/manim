from manim import *
from manimlib import *

def complex_to_point(z: complex, plane: ComplexPlane) -> np.ndarray:
    return plane.n2p([z.real, z.imag])

#TAU = 2PI
def param_circle(center=0+0j, R=2.0, t0=0, t1=TAU, orientation=+1):
    """Return function gamma(t) parameterizing a circle."""
    if orientation not in (+1, -1):
        raise ValueError("orientation must be +1 (counterclockwise) or -1 (clockwise)")
    def gamma(t):
        return center + R * np.exp(1j*(t0+(t1-t0)*t)*orientation)
    return gamma

def trapezoid_coutour_integral(f, gamma, N=2000):
    """Numerically approximate ∮ f(z) dz along z = gamma(t), t∈[0,1]."""
    ts = np.linspace(0.0, 1.0, N+1)
    zs = np.array([gamma(t) for t in ts], dtype=complex)
    dzs = np.diff(zs)
    #midpoint samples for f
    mids = (zs[:-1] + zs[1:])/2.0
    vals = np.array([f(z) for z in mids], dtype=complex)
    return np.sum(vals*dzs)

def residue_simple_pole(f, z0, h=1e-6):
    """Numerical residue for simple pole at z0 via limit (z-z0)f(z)."""
    return (f(z0+h)*h+f(z0-h)*(-h))/(2*h) #symmetric