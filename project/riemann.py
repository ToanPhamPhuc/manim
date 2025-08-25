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

class KleinBottle(ThreeDScene):
    def construct(self):
        # Set up 3D axes
        axes = ThreeDAxes()

        # Define Klein bottle parametric equations
        def klein_bottle(u, v):
            # u, v ∈ [0, 2π]
            u = u * 2 * PI
            v = v * 2 * PI
            x = (2 + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)) * np.cos(u)
            y = (2 + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)) * np.sin(u)
            z = np.sin(u / 2) * np.sin(v) + np.cos(u / 2) * np.sin(2 * v)
            return np.array([x, y, z])

        # Create parametric surface
        surface = Surface(
            lambda u, v: klein_bottle(u, v),
            u_range=[0, 1],
            v_range=[0, 1],
            resolution=(100, 100),
            fill_opacity=0.8,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )

        # Add to scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes)
        self.play(Create(surface))
        self.wait(2)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(8)

if __name__ == "__main__":
    config.quality = "high_quality"
    scene = SphereManifold()
    scene.render()