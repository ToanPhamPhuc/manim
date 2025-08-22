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

class FourierSquareWave(Scene):
    def construct(self):
        # Set up axes
        axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": BLUE},
        )
        axes_labels = axes.get_axis_labels(x_label="t", y_label="f(t)")
        self.play(Create(axes), Write(axes_labels))

        # Define square wave function
        def square_wave(t):
            return 1 if (t%2)<1 else -1
        
        # Plot the true square wave
        square_graph = axes.plot(square_wave, color=YELLOW, discontinuities=[-3, -2, -1, 0, 1, 2, 3])
        square_label = Tex("Square Wave", color=YELLOW).next_to(axes, UP).to_edge(LEFT)
        self.play(Create(square_graph), Write(square_label))
        self.wait(5)

        # Fourier series parameters
        T = 2 # Period of square wave
        max_term = 7 # Number of sine terms to add
        fourier_terms = []

        # Define Fourier series approximation
        def get_fourier_series(n_terms):
            def fourier_approx(t):
                result = 0
                for n in range(1, n_terms * 2, 2): #odd harmonic 
                    result += (4/ PI*n)* np.sin(2*PI*n*t/T)
                return result
            return fourier_approx
        
        