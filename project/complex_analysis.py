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

class CauchyIntegralTheoremScene(Scene):
    def construct(self):
        # Title
        title = Tex("Cauchy's Integral Theorem", font_size=64)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Complex plane
        plane = ComplexPlane(x_range=[-3, 3], y_range=[-3, 3], background_line_style={"stroke_opacity": 0.4})
        labels = plane.get_axis_labels(x_label="Re", y_label="Im")
        self.play(Create(plane), Write(labels))

        # Define path (circle)
        path = Circle(radius=1.5, color=YELLOW).move_to(plane.n2p(0))
        self.play(Create(path))

        # Function f(z) = 1/z
        formula = MathTex(r"f(z) = \frac{1}{z}")
        formula.next_to(title, DOWN)
        self.play(Write(formula))

        # Moving dot along path
        mover = Dot(color=BLUE).move_to(path.point_from_proportion(0))
        self.add(mover)

        def update_mover(mob, alpha):
            point = path.point_from_proportion(alpha)
            mob.move_to(point)

        self.play(UpdateFromAlphaFunc(mover, update_mover), run_time=4, rate_func=linear)

        # State theorem result
        result = MathTex(r"\oint_\gamma \frac{1}{z}\, dz = 0", color=GREEN)
        result.next_to(formula, DOWN)
        self.play(Write(result))

        self.wait(2)
