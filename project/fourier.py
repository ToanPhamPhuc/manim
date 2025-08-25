"""
Fourier series is a way to represent a periodic function as a sum of sine and cosine functions 
with different frequencies, amplitudes, and phases.
Fourier series expresses f as: f(t) = a0 + SUM(n=1->inf) {an*cos(2πnt/T) + bnsin(2πnt/T)}
where: 
+a0: The average (or DC component) of the function over one period
+an and bn: Coefficients that determine the amplitude of the cosine and sine terms of each frequency n\T
+n: An integer representing the harmonic (multiples of the fundamental frequency 1/T)
+The cosine and sine function oscillating at frequencies n/T

a0 = 1/T∫(0->T)f(t)dt
an = 2/T∫(0->T)f(t)cos(2πnt/T)
bn = 2/T∫(0->T)f(t)sin(2πnt/T)

Convergence: As you include more terms (higher $ n $), the Fourier series gets closer to the original function, 
though it may not converge perfectly at discontinuities.
"""

from manim import *

"""
Square Wave function: sgn(sin(2πnt/T)) is an example of periodic function, where sgn(), is the signum function, and it is non-continuous, that:
sgn(x) =  1 if x>0
sgn(x) =  0 if x=0
sgn(x) = -1 if x<0 

Its Fourier Series is: 4/π Sum(n odd->inf) {2πnt/T}
"""
class FourierSquareWave(Scene):
    def construct(self):
        # Set up axes
        axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-2, 2, 0.5],
            axis_config={"color": BLUE},
        )
        axes_labels = axes.get_axis_labels(x_label="t", y_label="f(t)")
        self.play(Create(axes), Write(axes_labels))
        
        # Define square wave function
        def square_wave(t):
            return 1 if (t % 2) < 1 else -1
        
        # Plot the true square wave
        square_graph = axes.plot(square_wave, color=YELLOW, discontinuities=[-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        square_label = Tex("Square Wave", color=YELLOW).next_to(axes, UP).to_corner(LEFT)
        self.play(Create(square_graph), Write(square_label))
        self.wait(1)
        
        # Fourier series parameters
        T = 2  # Period of square wave
        max_terms = 50  # Number of sine terms to add
        fourier_terms = []
        
        # Define Fourier series approximation
        def get_fourier_series(n_terms):
            def fourier_approx(t):
                result = 0
                for n in range(1, n_terms * 2, 2):  # Odd harmonics only
                    result += (4 / (np.pi * n)) * np.sin(2 * np.pi * n * t / T)
                return result
            return fourier_approx
        
        # Animate adding Fourier terms
        for n in range(1, max_terms + 1):
            # Get current Fourier approximation
            fourier_func = get_fourier_series(n)
            fourier_graph = axes.plot(fourier_func, color=RED)
            
            # Label for current number of terms
            term_label = Tex(f"Fourier Approx (n={n})", color=RED).next_to(axes, UP).to_corner(RIGHT)
            
            # Show the new term
            self.play(Create(fourier_graph), Write(term_label))
            self.wait(1)
            
            # Remove previous term's graph and label if they exist
            if fourier_terms:
                self.play(FadeOut(fourier_terms[-1]["graph"]), FadeOut(fourier_terms[-1]["label"]))
            
            # Store current graph and label
            fourier_terms.append({"graph": fourier_graph, "label": term_label})
        
        # Keep the final approximation and square wave
        self.play(FadeOut(fourier_terms[-1]["label"]))
        self.wait(2)

"""
Wave Function
"""
class FourierClassicalWave(Scene):
    def construct(self):
        # Set up axes
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-2, 2, 0.5],
            axis_config={"color": BLUE}
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y(x,t)")
        self.play(Create(axes), Write(axes_labels))

        # Wave parameters
        lambda_1 = 4 
        lambda_2 = 2
        omega_1 = 2*np.pi/2
        omega_2 = 2*np.pi/1
        A1, A2 = 1, 0.5

        # Define the classical wave function
        def wave_function(x, t):
            return A1*np.sin(2*np.pi*x/lambda_1 - omega_1*t) + A2*np.sin(2*np.pi*x/lambda_2 - omega_2*t)
        
        # Animate the traveling wave
        t = ValueTracker(0)
        wave_graph = always_redraw(
            lambda: axes.plot(lambda x: wave_function(x, t.get_value()), color=YELLOW)
        )
        wave_label = Tex("Classical Wave", color=YELLOW).next_to(axes, UP).to_edge(LEFT)
        self.play(Create(wave_graph), Write(wave_label))
        self.play(t.animate.set_value(2), run_time=4, rate_func=linear)
        self.wait(1)

        self.play(FadeOut(wave_graph), FadeOut(wave_label))

        # Show individual Fourier components
        def first_component(x, t):
            return A1*np.sin(2*np.pi*x/lambda_1 - omega_1*t)
        
        def second_component(x, t):
            return A2*np.sin(2*np.pi*x/lambda_2 - omega_1*t)
        
        # Plot first component
        t.set_value(0) #reset time
        component_1 = always_redraw(
            lambda: axes.plot(lambda x: first_component(x, t.get_value()), color=RED)
        )
        label_1 = Tex("First Component", color=RED).to_corner(UP+RIGHT)
        self.play(Create(component_1), Write(label_1))
        self.play(t.animate.set_value(2), run_time=4, rate_func=linear)
        self.wait(1)

        # Plot first component
        t.set_value(0) #reset time
        component_2 = always_redraw(
            lambda: axes.plot(lambda x: second_component(x, t.get_value()), color=GREEN)
        )
        self.play(FadeOut(label_1))
        label_2 = Tex("Second Component", color=GREEN).to_corner(UP+RIGHT)
        self.play(Create(component_2), Write(label_2))
        self.play(t.animate.set_value(2), run_time=4, rate_func=linear)
        self.wait(1)

        # Show how components sum to the original wave
        self.play(FadeOut(label_2))
        self.play(FadeOut(component_1), FadeOut(component_2))
        self.play(Create(wave_graph), Create(wave_label))
        self.play(t.animate.set_value(4), run_time=8, rate_func=linear)
        self.wait(5)
        
"""
The Classical Wave Equation, is a second-order linear PDE for the description of waves or standing wave fields such as mechanical waves or electromagnetic waves.
It arises in fields like acoustics, electromagnetism, and fluid dynamics.
d^u/dt^2=c^2(d^2u/dx^2+d^2u/dy^2+d^2u/dz^2)
Where: u(x,y,z,t) is the wave amplitude, c is the wave speed, and the right hand sigh represents the Laplacian (∇^2u) in 3D space.
Our goal is to apply a Fourier transform to this equation, which is  a common technique to solve linear PDEs by decomposing the solution into frequency components
"""

class WaveEquationVisualization(ThreeDScene):
    def construct(self):
        # Set up 2D axes (x, y)
        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            z_range=[-2, 2, 0.5],  # For height of the wave
            axis_config={"color": BLUE},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(axes_labels))

        # Wave parameters
        c = 1.0
        k_x, k_y = 1.0, 1.0  # Wave numbers
        omega = c * np.sqrt(k_x**2 + k_y**2)
        t = ValueTracker(0)

        # Define 2D wave function (z=0 plane for simplicity)
        def wave_function(x, y):
            return np.sin(k_x * x + k_y * y - omega * t.get_value())

        # Create surface plot
        wave_surface = always_redraw(
            lambda: Surface(
                lambda x, y: wave_function(x, y),
                resolution=(20, 20),
                u_range=[-6, 6],
                v_range=[-6, 6],
                color=YELLOW,
            )
        )
        self.play(Create(wave_surface))
        self.play(t.animate.set_value(4), run_time=4, rate_func=linear)
        self.wait(1)