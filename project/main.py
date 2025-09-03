from manim import *

class SpaceGrid(ThreeDScene):
    def construct(self):
        # Set up axes (hidden, used for orientation)
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-3, 3, 1],
            axis_config={"include_numbers": False, "stroke_width": 1},
        )
        
        # Create the grid surface (flat, no mass yet)
        grid = Surface(
            lambda u, v: np.array([u, v, 0]), # flat sheet z=0
            u_range=[-5, 5],
            v_range=[-5, 5],
            resolution=(20, 20),
            fill_opacity=0,
            stroke_color=WHITE,
        )
        
        # Camera setup
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        
        self.add(axes, grid)
        self.wait()

class WarpedSpaceWithEarth(ThreeDScene):
    def construct(self):
        # Warp function for the grid
        def warp(u, v):
            r = np.sqrt(u**2 + v**2) + 1e-6
            z = -1 / (r + 0.5)
            return np.array([u, v, z])

        # Warped grid surface
        grid = Surface(
            warp,
            u_range=[-5, 5],
            v_range=[-5, 5],
            resolution=(30, 30),
            fill_opacity=0,
            stroke_color=WHITE,
        )

        # Simple parametric sphere
        sphere = Surface(
            lambda u, v: np.array([
                0.6 * np.cos(u) * np.sin(v),
                0.6 * np.sin(u) * np.sin(v),
                0.6 * np.cos(v),
            ]),
            u_range=[0, TAU],
            v_range=[0, PI],
            resolution=(32, 64),
            fill_opacity=1,
            checkerboard_colors=[BLUE_D, BLUE_E],  # just to give shading
        )

        # Camera orientation
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)

        self.add(grid, sphere)
        self.wait()
