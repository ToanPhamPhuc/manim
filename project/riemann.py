from manim import *

class SphereManifold(ThreeDScene):
    def construct(self):
        # Set up 3D axes and camera
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            axis_config={"color": WHITE}
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes)

        # Define the sphere as a parametric surface (u: longitude, v: latitude)
        def sphere_param(u, v):
            return np.array([
                np.cos(u) * np.sin(v),
                np.sin(u) * np.sin(v),
                np.cos(v)
            ])

        # Create the sphere surface
        sphere = Surface(
            lambda u, v: sphere_param(u, v),
            u_range=[0, TAU],
            v_range=[0, PI],
            resolution=(20, 20),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        sphere.set_shade_in_3d(True)

        # Color-code based on Gaussian curvature (constant +1 for unit sphere)
        # Simulate variation for visual effect
        def curvature_color(point):
            z = point[2]
            return color_gradient([RED, YELLOW], (z + 1) / 2)

        sphere.set_fill_by_value(curvature_color, axis=2)  # Color by z-axis for demo

        # Add the sphere
        self.play(Create(sphere), run_time=2)

        # Animate a geodesic (great circle)
        geodesic = ParametricFunction(
            lambda t: sphere_param(t, PI / 2),  # Equatorial circle
            t_range=[0, TAU],
            color=GREEN,
            stroke_width=4
        )
        self.play(Create(geodesic), run_time=2)

        # Rotate the camera to explore the manifold
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        # Fade out
        self.play(FadeOut(sphere), FadeOut(geodesic), FadeOut(axes), run_time=1)

class S3Projection(ThreeDScene):
    def construct(self):
        # Set up 3D axes and camera
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"color": WHITE}
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes)

        # Stereographic projection from S^3 to R^3
        # Map (x, y, z, w) on x^2 + y^2 + z^2 + w^2 = 1 to R^3 from pole (0,0,0,1)
        def stereographic(x, y, z, w):
            denom = 1 - w
            if abs(denom) < 1e-6:  # Avoid division by zero near pole
                denom = 1e-6
            return np.array([x / denom, y / denom, z / denom])

        # Parameterize S^3 using hyperspherical coords (simplified via Hopf fibration)
        # For visualization, show 2D surfaces (tori/spheres) at fixed angles
        def hopf_surface(u, v, chi=PI/4):
            # chi is the Hopf parameter, fixing a 2D slice of S^3
            w = np.cos(chi)
            z = np.sin(chi) * np.cos(v)
            x = np.sin(chi) * np.sin(v) * np.cos(u)
            y = np.sin(chi) * np.sin(v) * np.sin(u)
            return stereographic(x, y, z, w)

        # Create multiple surfaces for different chi values to suggest 3D manifold
        surfaces = []
        chi_values = [PI/6, PI/4, PI/3]  # Different slices
        colors = [BLUE_D, GREEN_D, PURPLE_D]
        for chi, color in zip(chi_values, colors):
            surface = Surface(
                lambda u, v: hopf_surface(u, v, chi),
                u_range=[0, TAU],
                v_range=[0, TAU],
                resolution=(20, 20),
                fill_opacity=0.6,
                checkerboard_colors=[color, color]
            )
            surface.set_shade_in_3d(True)
            surfaces.append(surface)

        # Animate creation of surfaces
        self.play(*[Create(surf) for surf in surfaces], run_time=3)

        # Add a geodesic (great circle in S^3, projected to R^3)
        geodesic = ParametricFunction(
            lambda t: stereographic(np.cos(t), np.sin(t), 0, 0),  # Circle in x,y plane of S^3
            t_range=[0, TAU],
            color=RED,
            stroke_width=4
        )
        self.play(Create(geodesic), run_time=2)

        # Rotate camera to explore the projection
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()

        # Fade out
        self.play(*[FadeOut(surf) for surf in surfaces], FadeOut(geodesic), FadeOut(axes), run_time=1)

class KleinConstruction(ThreeDScene):
    def construct(self):
        # camera + axes
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES, zoom=0.9)
        axes = ThreeDAxes()
        self.add(axes)

        # ---------- Step 1: square with arrows ----------
        step1_title = Text("1) Start with a square — identify opposite edges",
                           font_size=34).to_edge(UP)
        self.add_fixed_in_frame_mobjects(step1_title)

        s = 4
        square = Square(side_length=s).set_stroke(WHITE, 2)

        # arrows (red = left/right edges, blue = top/bottom edges)
        left_arrow   = Arrow(square.get_corner(UL), square.get_corner(DL),
                             buff=0, color=RED, stroke_width=6)
        right_arrow  = Arrow(square.get_corner(UR), square.get_corner(DR),
                             buff=0, color=RED, stroke_width=6)
        top_arrow    = Arrow(square.get_corner(UR), square.get_corner(UL),
                             buff=0, color=BLUE, stroke_width=6)
        bottom_arrow = Arrow(square.get_corner(DL), square.get_corner(DR),
                             buff=0, color=BLUE, stroke_width=6)
        arrows2d = VGroup(left_arrow, right_arrow, top_arrow, bottom_arrow)

        self.play(Create(square), LaggedStartMap(Create, arrows2d, lag_ratio=0.15),
                  Write(step1_title))
        self.wait(1)

        # ---------- Step 2: glue left/right → cylinder ----------
        step2_title = Text("2) Glue left & right edges → a cylinder",
                           font_size=34).to_edge(UP)
        self.add_fixed_in_frame_mobjects(step2_title)

        cyl = self.make_cylinder(radius=1.5, height=4.0)
        cyl_marks = self.cylinder_rim_arrows(radius=1.5, height=4.0)

        self.play(FadeTransform(VGroup(square, arrows2d), VGroup(cyl, cyl_marks)),
                  Transform(step1_title, step2_title))
        self.wait(1)

        # ---------- Step 3: pass one end through the side ----------
        step3_title = Text("3) Pass one end through the side, then glue the ends",
                           font_size=34).to_edge(UP)
        self.add_fixed_in_frame_mobjects(step3_title)

        # a copy of the cylinder to illustrate the motion
        mover = VGroup(cyl.copy(), cyl_marks.copy())
        self.add(mover)

        self.play(Transform(step1_title, step3_title))
        # tilt and swing the copy to "thread" it through
        self.play(mover.animate.rotate(PI/2, axis=RIGHT).shift(LEFT * 2.8))
        self.play(mover.animate.shift(RIGHT * 2.8))
        self.wait(1)

        # ---------- Step 4: Klein bottle (figure-8 immersion) ----------
        step4_title = Text("4) Resulting surface: Klein bottle (figure-8 immersion)",
                           font_size=34).to_edge(UP)
        self.add_fixed_in_frame_mobjects(step4_title)

        klein = self.klein_figure8_surface(r=2.2).set_opacity(0.9)
        self.play(Transform(step1_title, step4_title))
        self.play(ReplacementTransform(VGroup(cyl, cyl_marks, mover), klein))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)

    # ---------- helpers ----------

    def make_cylinder(self, radius=1.5, height=4.0):
        """Closed cylinder surface (for visuals)."""
        return Surface(
            lambda u, v: np.array([
                radius * np.cos(TAU * u),
                radius * np.sin(TAU * u),
                (v - 0.5) * height
            ]),
            u_range=[0, 1], v_range=[0, 1], resolution=(64, 20),
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_color=BLACK, stroke_width=0.5, fill_opacity=0.85
        )

    def cylinder_rim_arrows(self, radius=1.5, height=4.0):
        """Rim circles + tangent arrows indicating how ends should be glued."""
        def rim(z, color, direction=+1):
            circ = Circle(radius=radius, color=color, stroke_width=4).shift(OUT * (z))
            # tangent arrow on the rim (tangent at angle 0)
            p = np.array([radius, 0, z])
            t = np.array([0, 1, 0]) * direction  # tangent direction
            arr = Arrow(p - 0.7 * t, p + 0.7 * t, buff=0, stroke_width=6, color=color)
            return VGroup(circ, arr)

        top = rim(+height/2, BLUE, direction=+1)
        bot = rim(-height/2, BLUE, direction=+1)  # same orientation to “match” when glued
        seam = DashedLine(
            np.array([radius, 0, -height/2]),
            np.array([radius, 0, +height/2]),
            color=RED, dash_length=0.15
        )
        return VGroup(top, bot, seam)

    def klein_figure8_surface(self, r=2.2):
        """Figure-8 immersion from Wikipedia (theta,v in [0,2π))."""
        def f(u, v):
            th = TAU * u
            w = TAU * v
            x = (r + np.cos(th/2) * np.sin(w) - np.sin(th/2) * np.sin(2*w)) * np.cos(th)
            y = (r + np.cos(th/2) * np.sin(w) - np.sin(th/2) * np.sin(2*w)) * np.sin(th)
            z =  np.sin(th/2) * np.sin(w) + np.cos(th/2) * np.sin(2*w)
            return np.array([x, y, z])

        return Surface(
            f, u_range=[0, 1], v_range=[0, 1], resolution=(100, 100),
            checkerboard_colors=[PURPLE_D, ORANGE],
            stroke_color=BLACK, stroke_width=0.5, fill_opacity=0.9
        )
