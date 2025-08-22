from manim import *
import numpy as np

#constants
pi = np.pi

class SphereManinold(ThreeDScene):
    def construct(self):
        #set up 3D axes and camera
        axes = ThreeDScene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes)

        #define sphere as a parametric surface
        def sphere_param(u, v):
            return np.array([
                np.cos(u) * np.sin(v),
                np.sin(u) * np.sin (v),
                np.cos(v)
            ])
        
        #create the sphere surface
        sphere = Surface(
            lambda u, v: sphere_param(u, v),
            u_range=[0, TAU],
            v_range=[0, PI],
            resolution=(20, 20),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        sphere.set_shade_in_3d(True)

        #color-code based on Gaussian curvature (constant +1 for unit sphere)
        #and for illustration, vary color intensity (in reality, it's uniform)
        def curvature_color(point):
            #K = 1/r^2 =1 (Gaussian Curvature) = 1 for unit sphere; simulate variation for demo
            z = point[2]
            return color_gradient([RED, YELLOW], (z+1)/2)
        
        sphere.set_color_by_gradient(curvature_color) #approximate curvation visualization

        #add the sphere
        self.play(Create(sphere), run_time=2)

        #animate a geodesic (great circle)
        geodesic = ParametricFunction(
            lambda t: sphere_param(t, pi/2), #equatorial circle
            t_range=[0, TAU],
            color=GREEN,
            stroke_width=4
        )
        self.play(Create(geodesic), run_time=2)

        #rotate the camera to explore the manifold
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.embed()
        #self.stop_ambient_camera_rotation

        #fade out
        #self.play(FadeOut(sphere), FadeOut(geodesic), FadeOut(axes))