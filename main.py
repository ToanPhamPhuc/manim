from manimlib import *

class STC(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        z1 = complex(0, 1)

        def func(z):
            return (2*z1*z**2+3*z)/(z-3-2*z1)

        def euler(z):
            return (np.exp(np.pi*z1))

        self.play(ShowCreation(square))
        self.wait()
        self.play(ReplacementTransform(square, circle))
        self.wait()

        self.embed()

        