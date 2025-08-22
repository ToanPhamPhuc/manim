from manim import *
import cmath
import numpy as np
from scipy.special import factorial

#region: def
def complex_to_point(z: complex, plane: ComplexPlane) -> np.ndarray:
    return plane.n2p(z)

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

# ==========================
# 2) Cauchy Integral Formula (CIF)
# ==========================
class CauchyIntegralFormulaScene(BasedComplexScene):
    def construct(self):
        plane = self.setup_plane()
        title = TitleBanner(r"Cauchy's Integral Formula", r"$f(z_0)=\frac{1}{2\pi i}\oint_{|z-z_0|=R}\frac{f(z)}{z-z_0}\,dz$")
        title.to_edge(UP)
        self.play(FadeIn(title))

        z0 = 0.8 + 0.4j
        dot0 = Dot(color=YELLOW).move_to(complex_to_point(z0, plane))
        self.play(FadeIn(dot0))
        label0 = MathTex("z_0").next_to(dot0, UR, buff=0.1)
        self.add(label0)

        R = 1.5
        circle = Circle(radius=R, color=BLUE).move_to(complex_to_point(z0, plane))
        self.play(Create(circle))

        # f analytic: e^z
        def f(z):
            return cmath.exp(z)
        # gamma(t) circle around z0, CCW
        gamma = param_circle(center=z0, R=R, orientation=+1)

        approx = trapezoid_contour_integral(lambda z: f(z)/(z - z0), gamma, N=2400)
        est = approx / (2j*np.pi)

        box = MathTex(r"\frac{1}{2\pi i}\oint \frac{e^z}{z-z_0}\,dz \approx e^{z_0}")
        box.to_edge(DOWN)
        self.show_integral_box(box)

        shown = VGroup(
        MathTex(r"\text{LHS }\approx ", f"{est.real:.5f}+{est.imag:.5f}i"),
        MathTex(r"\text{RHS }= e^{z_0} = ", f"{f(z0).real:.5f}+{f(z0).imag:.5f}i"),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(box, UP)
        self.play(Write(shown))

        # Catch: clockwise orientation gives a minus sign
        catch = Tex(r"Catch: Clockwise orientation $\Rightarrow$ a minus sign.")
        catch.next_to(shown, UP)
        self.play(FadeIn(catch))

        cw_circle = circle.copy().set_color(RED)
        self.play(TransformFromCopy(circle, cw_circle, run_time=1))
        gamma_cw = param_circle(center=z0, R=R, orientation=-1)
        approx_cw = trapezoid_contour_integral(lambda z: f(z)/(z - z0), gamma_cw, N=2400)
        est_cw = approx_cw / (2j*np.pi)
        minus_text = MathTex(r"\frac{1}{2\pi i}\oint_{\text{CW}} = -\,e^{z_0}", color=RED).next_to(catch, UP)
        self.play(Write(minus_text))
        self.wait(1)

# ==========================
# 3) Generalized Cauchy Integral Formula (nth derivative)
# ==========================
class GeneralIntegralFormulaScene(BasedComplexScene):
    def construct(self):
        plane = self.setup_plane()
        title = TitleBanner(r"Generalized CIF", r"$f^{(n)}(z_0)=\frac{n!}{2\pi i}\oint\frac{f(z)}{(z-z_0)^{n+1}}dz$")
        title.to_edge(UP)
        self.play(FadeIn(title))

        z0 = -0.7 + .5j
        dot0 = Dot(color=YELLOW).move_to(complex_to_point(z0, plane))
        self.add(dot0, MathTex("z_0").next_to(dot0, UR, buff=0.1))

        R = 1.2
        circle = Circle(radius=R, color=BLUE).move_to(complex_to_point(z0, plane))
        self.play(Create(circle))

        #choose and f
        n = 2
        def f(z):
            return cmath.cos(z)
        
        #true val cos''(z) = -cos(z)

        true_val = -cmath.cos(z0)
        gamma = param_circle(center=z0, R=R, orientation=+1)
        approx = trapezoid_contour_integral(lambda z: f(z) / (z-z0)**(n+1), gamma, N=2600)
        est = (factorial(n)/(2j*np.pi)) * approx

        panel = VGroup(
            MathTex(r"n=2,\ f(z)=\cos z"),
            MathTex(r"\frac{2!}{2\pi i}\oint \frac{\cos z}{(z-z_0)^3}\,dz \stackrel{?}{=} \cos''(z_0) = -\cos z_0"),
            MathTex(r"\text{LHS }\approx ", f"{est.real:.5f}+{est.imag:.5f}i"),
            MathTex(r"\text{RHS }= ", f"{true_val.real:.5f}+{true_val.imag:.5f}i"),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN)

        self.play(Write(panel))

        # Catch: z0 must be inside; crossing boundary invalidates; singularities of f inside are forbidden
        catch = Tex(r"Catches: $z_0$ must be inside; $f$ analytic on/inside; no extra poles in disk.")
        catch.next_to(panel, UP)
        self.play(FadeIn(catch))
        self.wait(1)

# ==========================
# 4) Residue Theorem
# ==========================
class ResidueTheoremScene(BasedComplexScene):
    def construct(self):
        plane = self.setup_plane()
        title = TitleBanner(r"Residue Theorem", r"$\oint_\gamma f(z)dz=2\pi i\sum \text{Res}(f; z_k)$ for poles $z_k$ inside $\gamma$")        
        title.to_edge(UP)
        self.play(FadeIn(title))

        # example: f(z) = z/[(z-1)(z+2)]
        def f(z):
            return z / ((z-1)*(z+2))
        
        #circle centered at 0 of radius 1.5 (contains z=1 but not z=-2)
        R = 1.5
        circle = Circle(radius=R, color=BLUE).move_to(complex_to_point(0j, plane))
        self.play(Create(circle))

        # Poles
        poles = [1+0j, -2+0j]
        colors = [YELLOW, GRAY]
        for p, c in zip(poles, colors):
            dot = Dot(color=c).move_to(complex_to_point(p, plane))
            label = MathTex(f"{p.real:.0f}").next_to(dot, DOWN, buff=0.05)
            self.add(dot, label)

        gamma = param_circle(center=0+0j, R=R, orientation=+1)
        approx = trapezoid_contour_integral(f, gamma, N=2600)


        # Residues (analytic)
        # Res at z=1: lim (z-1) f = z/((z+2)) |_{z=1} = 1/3
        # Res at z=-2 is outside, so skip
        res_sum = 1/3
        lhs = MathTex(r"\oint f(z)dz \approx ", f"{approx.real:.5f}+{approx.imag:.5f}i")
        rhs = MathTex(r"2\pi i\,\sum \text{Res} = 2\pi i\cdot \tfrac{1}{3} = \tfrac{2\pi i}{3}")
        panel = VGroup(lhs, rhs).arrange(DOWN).to_edge(DOWN)
        self.play(Write(panel))


        # Catch: Only poles inside count; holes in domain / branch cuts break homotopy arguments
        catch = Tex(r"Catches: only interior poles; branch cuts/essential singularities need care; \\ contour must avoid singularities and be oriented.")
        catch.next_to(panel, UP)
        self.play(FadeIn(catch))
        self.wait(1)

# ==========================
# 5) Branch Cut / Non-analytic Catch
# ==========================
class BranchCutCatchScene(BasedComplexScene):
    def construct(self):
        plane = self.setup_plane()
        title = TitleBanner(
            r"Branch Cuts \& Non-analytic Integrands", 
            r"CIT fails if $f$ not analytic; multivalued logs need branches"
        )

        title.to_edge(UP)
        self.play(FadeIn(title))

        # Example 1: f(z)=conj(z) is nowhere-analytic -> integral generally ≠ 0
        def f1(z):
            return np.conjugate(z)
            
        zc = 0+0j
        R = 1.8
        circle = Circle(radius=R, color=RED).move_to(complex_to_point(zc, plane))
        self.play(Create(circle))
        gamma = param_circle(center=zc, R=R, orientation=+1)
        approx = trapezoid_contour_integral(f1, gamma, N=2400)

        t1 = VGroup(
            Tex(r"Example: $f(z)=\overline{z}$ (not analytic anywhere)"),
            MathTex(r"\oint f(z)\,dz \not\equiv 0\ (CIT\ doesn't\ apply)").set_color(RED),
            MathTex(r"\text{Numerical }\approx ", f"{approx.real:.4f}+{approx.imag:.4f}i"),
        ).arrange(DOWN).to_edge(DOWN)
        self.play(Write(t1))
        self.wait(0.5)

        # Example 2: log z with branch cut on negative real axis; circle that crosses the cut
        self.play(*[FadeOut(mob) for mob in [circle, *t1]])
        base = Tex(r"Example: $\log z$ with principal branch cut on $(-\infty,0]$.")
        base.to_edge(DOWN)
        self.play(Write(base))

        def flog(z):
        # principal log via Python's cmath.log (branch cut on negative real axis)
            return cmath.log(z) 
        
        # Keyhole-like path that crosses the negative real axis -> jump in argument
        R1, R2 = 2.2, 1.2
        # Outer CCW
        outer = ParametricFunction(lambda t: complex_to_point(R1*np.exp(1j*t), plane), t_range=[-PI+0.3, PI-0.3], color=BLUE)
        # Inner CW
        inner = ParametricFunction(lambda t: complex_to_point(R2*np.exp(1j*t), plane), t_range=[PI-0.3, -PI+0.3], color=BLUE)
        bridge_top = Line(complex_to_point(R2*np.exp(1j*(PI-0.3)), plane), complex_to_point(R1*np.exp(1j*(PI-0.3)), plane), color=BLUE)
        bridge_bot = Line(complex_to_point(R1*np.exp(1j*(-PI+0.3)), plane), complex_to_point(R2*np.exp(1j*(-PI+0.3)), plane), color=BLUE)
        path_group = VGroup(outer, bridge_top, inner, bridge_bot)
        self.play(Create(path_group))

        # Define a parameterization that traverses the keyhole once
        pieces = []
        pieces.append(lambda s: R1 * np.exp(1j*(-PI+0.3 + (PI-0.3 - (-PI+0.3)) * s))) # outer CCW
        pieces.append(lambda s: R2 * np.exp(1j*(PI-0.3))) # top bridge start (stationary -> will be replaced)
        pieces.append(lambda s: R2 * np.exp(1j*(PI-0.3 + (-PI+0.3 - (PI-0.3)) * s))) # inner CW
        pieces.append(lambda s: R1 * np.exp(1j*(-PI+0.3))) # bottom bridge end

        # We'll just integrate the two circular arcs; bridge segments are negligible here (or could be added as straight lines)
        def gamma_keyhole(u):
        # map u in [0,1] to concatenated arcs + straight segments with small weight
            u = np.clip(u, 0, 1)
            if u < 0.5:
                s = u / 0.5
                return pieces[0](s)
            else:
                s = (u-0.5)/0.5
                return pieces[2](s)
        
        approx2 = trapezoid_contour_integral(flog, gamma_keyhole, N=2800)
        info = VGroup(
            Tex(r"Crossing the branch cut changes $\arg z$ by $2\pi$, causing a jump in $\log z$."),
            MathTex(r"\oint_{\text{keyhole}} \log z\,dz\ \text{reflects the branch jump}").set_color(YELLOW),
            MathTex(r"\text{Numerical }\approx ", f"{approx2.real:.4f}+{approx2.imag:.4f}i"),
        ).arrange(DOWN).next_to(base, UP)
        self.play(Write(info))
        self.wait(1)
