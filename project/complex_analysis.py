from manim import *

#region: def
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

def trapezoid_contour_integral(f, gamma, N=2000):
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
#endregion

class TitleBanner(VGroup):
    def __init__(self, title:str, subtitle: str = "", **kwargs):
        super().__init__(**kwargs)
        t = Tex(title).scale(1.0)
        s = Tex(subtitle).scale(0.7).set_opacity(0.8) if subtitle else VGroup()
        self.add(t, s.arrange(DOWN, buff=0.2) if subtitle else t)

class BasedComplexScene(Scene):
    def setup_plane(self, x_range=(-4,4,1), y_range=(-3,3,1)):
        plane = ComplexPlane(x_range=x_range, y_range=y_range).add_coordinates()
        self.add(plane)
        return plane
    
    def show_integral_box(self, tex, pos=ORIGIN, color=YELLOW):
        box = SurroundingRectangle(tex, color=color, buff=0.25)
        self.play(FadeIn(tex), Create(box))
        return VGroup(tex, box).move_to(pos)
    
    def construct(self):
        tex = Tex()
        self.show_integral_box(tex)
        
# ==========================
# 1) Cauchy Integral Theorem (CIT)
# ==========================

class CauchyIntegralTheoremScene(BasedComplexScene):
    def construct(self):
        plane = self.setup_plane()
        title = TitleBanner(r"Cauchy Integral Theorem", r"If $f$ analytic on and inside $\gamma$ then $\oint_\gamma f(z)\,dz=0$")
        title.to_edge(UP)
        self.play(FadeIn(title))


        # Example function analytic everywhere: f(z) = z^2
        def f(z):
            return z**2


        # Square contour (piecewise smooth) around origin
        R = 2.0
        pts = [R+R*1j, -R+R*1j, -R-R*1j, R-R*1j, R+R*1j]
        poly = VMobject().set_stroke(BLUE, 3)
        poly.set_points_as_corners([plane.n2p([p.real, p.imag]) for p in pts])
        self.play(Create(poly))


        # Animate a dot going around
        mover = Dot(color=BLUE).move_to(plane.n2p([pts[0].real, pts[0].imag]))
        self.add(mover)
        self.play(MoveAlongPath(mover, poly), run_time=3, rate_func=linear)


        # Numerical integral ~ 0
        gamma_segments = [
            lambda t: R + R*1j + t*(-2*R), # top: (R+iR) -> (-R+iR)
            lambda t: -R + R*1j + t*(-2j*R), # left: (-R+iR) -> (-R-iR)
            lambda t: -R - R*1j + t*(2*R), # bottom: (-R-iR) -> (R-iR)
            lambda t: R - R*1j + t*(2j*R), # right: (R-iR) -> (R+iR)
        ]
        def gamma(u):
            # concatenate segments
            u = np.clip(u, 0, 1)
            k = int(u * 4)
            if k == 4: k = 3
            t = u*4 - k
            return gamma_segments[k](t)

        approx = trapezoid_contour_integral(f, gamma, N=1600)
        tex = MathTex(r"\oint_\gamma z^2\,dz \approx ", f"{approx.real:.2e}+{approx.imag:.2e}i", r"\approx 0")
        tex.to_edge(DOWN)
        self.play(Write(tex))
        self.wait(0.5)


        # Catch 1: Not simply-connected / a singularity inside -> CIT doesn't apply
        catch = Tex(r"Catch: CIT needs analyticity on \\ and *inside* $\gamma$. A pole inside breaks it.")
        catch.next_to(tex, UP)
        self.play(FadeIn(catch))


        # Replace f with 1/(z - 0.5) (simple pole at 0.5)
        def g(z):
            return 1.0 / (z - 0.5)
        approx_g = trapezoid_contour_integral(g, gamma, N=2000)
        tex2 = MathTex(r"\oint_\gamma \frac{dz}{z-0.5} = 2\pi i \neq 0\ (analytically)", color=YELLOW)
        tex2.next_to(catch, UP)
        self.play(Write(tex2))
        self.wait(1)