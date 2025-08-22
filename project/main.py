from manimlib import *
from manim import *

# #region: Example Scenes
# class BraceAnnotation(Scene):
#     def construct(self):
#         dot = Dot([-2, -1, 0])
#         dot2 = Dot([2, 1, 0])
#         line = Line(dot.get_center(), dot2.get_center()).set_color(ORANGE)
#         b1 = Brace(line)
#         b1text = b1.get_text("Horizontal distance")
#         b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
#         b2text = b2.get_tex("x-x_1")
#         self.add(line, dot, dot2, b1, b2, b1text, b2text)

# class VectorArrow(Scene):
#     def construct(self):
#         dot = Dot(ORIGIN)
#         arrow = Arrow(ORIGIN, [2, 2, 0], buff=0)
#         numberplane = NumberPlane()
#         origin_text = Text('(0, 0)').next_to(dot, DOWN)
#         tip_text = Text('(2, 2)').next_to(arrow.get_end(), RIGHT)
#         self.add(numberplane, dot, arrow, origin_text, tip_text)
#         self.wait(5)
#         self.embed()

# class GradientImageFromArray(Scene):
#     def construct(self):
#         n = 256
#         imageArray = np.uint8(
#             [[i * 256 / n for i in range(0, n)] for _ in range(0, n)]
#         )
#         image = ImageMobject(imageArray).scale(2)
#         image.background_rectangle = SurroundingRectangle(image, color=GREEN)
#         self.add(image, image.background_rectangle)

# class BooleanOperations(Scene):
#     def construct(self):
#         ellipse1 = Ellipse(
#             width=4.0, height=5.0, fill_opacity=0.5, color=BLUE, stroke_width=10
#         ).move_to(LEFT)
#         ellipse2 = ellipse1.copy().set_color(color=RED).move_to(RIGHT)
#         bool_ops_text = MarkupText("<u>Boolean Operation</u>").next_to(ellipse1, UP * 3)
#         ellipse_group = Group(bool_ops_text, ellipse1, ellipse2).move_to(LEFT * 3)
#         self.play(FadeIn(ellipse_group))

#         i = Intersection(ellipse1, ellipse2, color=GREEN, fill_opacity=0.5)
#         self.play(i.animate.scale(0.25).move_to(RIGHT * 5 + UP * 2.5))
#         intersection_text = Text("Intersection", font_size=23).next_to(i, UP)
#         self.play(FadeIn(intersection_text))

#         u = Union(ellipse1, ellipse2, color=ORANGE, fill_opacity=0.5)
#         union_text = Text("Union", font_size=23)
#         self.play(u.animate.scale(0.3).next_to(i, DOWN, buff=union_text.height * 3))
#         union_text.next_to(u, UP)
#         self.play(FadeIn(union_text))

#         e = Exclusion(ellipse1, ellipse2, color=YELLOW, fill_opacity=0.5)
#         exclusion_text = Text("Exclusion", font_size=23)
#         self.play(e.animate.scale(0.3).next_to(u, DOWN, buff=exclusion_text.height * 3.5))
#         exclusion_text.next_to(e, UP)
#         self.play(FadeIn(exclusion_text))

#         d = Difference(ellipse1, ellipse2, color=PINK, fill_opacity=0.5)
#         difference_text = Text("Difference", font_size=23)
#         self.play(d.animate.scale(0.3).next_to(u, LEFT, buff=difference_text.height * 3.5))
#         difference_text.next_to(d, UP)
#         self.play(FadeIn(difference_text))

# class PointMovingOnShapes(Scene):
#     def construct(self):
#         circle = Circle(radius=1, color=BLUE)
#         dot = Dot()
#         dot2 = dot.copy().shift(RIGHT)
#         self.add(dot)

#         line = Line([3, 0, 0], [5, 0, 0])
#         self.add(line)

#         self.play(GrowFromCenter(circle))
#         self.play(Transform(dot, dot2))
#         self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
#         self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
#         self.wait()

# class MovingAround(Scene):
#     def construct(self):
#         square = Square(color=BLUE, fill_opacity=1)

#         self.play(square.animate.shift(LEFT))
#         self.play(square.animate.set_fill(ORANGE))
#         self.play(square.animate.scale(0.3))
#         self.play(square.animate.rotate(0.4))

# class MovingDots(Scene):
#     def construct(self):
#         d1,d2=Dot(color=BLUE),Dot(color=GREEN)
#         dg=VGroup(d1,d2).arrange(RIGHT,buff=1)
#         l1=Line(d1.get_center(),d2.get_center()).set_color(RED)
#         x=ValueTracker(0)
#         y=ValueTracker(0)
#         d1.add_updater(lambda z: z.set_x(x.get_value()))
#         d2.add_updater(lambda z: z.set_y(y.get_value()))
#         l1.add_updater(lambda z: z.become(Line(d1.get_center(),d2.get_center())))
#         self.add(d1,d2,l1)
#         self.play(x.animate.set_value(5))
#         self.play(y.animate.set_value(4))
#         self.wait()
        
# class MovingGroupToDestination(Scene):
#     def construct(self):
#         group = VGroup(Dot(LEFT), Dot(ORIGIN), Dot(RIGHT, color=RED), Dot(2 * RIGHT)).scale(1.4)
#         dest = Dot([4, 3, 0], color=YELLOW)
#         self.add(group, dest)
#         self.play(group.animate.shift(dest.get_center() - group[2].get_center()))
#         self.wait(0.5)

# class RotationUpdater(Scene):
#     def construct(self):
#         def updater_forth(mobj, dt):
#             mobj.rotate_about_origin(dt)
#         def updater_back(mobj, dt):
#             mobj.rotate_about_origin(-dt)
#         line_reference = Line(ORIGIN, LEFT).set_color(WHITE)
#         line_moving = Line(ORIGIN, LEFT).set_color(YELLOW)
#         line_moving.add_updater(updater_forth)
#         self.add(line_reference, line_moving)
#         self.wait(2)
#         line_moving.remove_updater(updater_forth)
#         line_moving.add_updater(updater_back)
#         self.wait(2)
#         line_moving.remove_updater(updater_back)
#         self.wait(0.5)

# class SinAndCosFunctionPlot(Scene):
#     def construct(self):
#         axes = Axes(
#             x_range=[-10, 10.3, 1],
#             y_range=[-1.5, 1.5, 1],
#             x_length=10,
#             axis_config={"color": GREEN},
#             x_axis_config={
#                 "numbers_to_include": np.arange(-10, 10.01, 2),
#                 "numbers_with_elongated_ticks": np.arange(-10, 10.01, 2),
#             },
#             tips=False,
#         )
#         axes_labels = axes.get_axis_labels()
#         sin_graph = axes.plot(lambda x: np.sin(x), color=BLUE)
#         cos_graph = axes.plot(lambda x: np.cos(x), color=RED)

#         sin_label = axes.get_graph_label(
#             sin_graph, "\\sin(x)", x_val=-10, direction=UP / 2
#         )
#         cos_label = axes.get_graph_label(cos_graph, label="\\cos(x)")

#         vert_line = axes.get_vertical_line(
#             axes.i2gp(TAU, cos_graph), color=YELLOW, line_func=Line
#         )
#         line_label = axes.get_graph_label(
#             cos_graph, r"x=2\pi", x_val=TAU, direction=UR, color=WHITE
#         )

#         plot = VGroup(axes, sin_graph, cos_graph, vert_line)
#         labels = VGroup(axes_labels, sin_label, cos_label, line_label)
#         self.add(plot, labels)

# class ArgMinExample(Scene):
#     def construct(self):
#         ax = Axes(
#             x_range=[0, 10], y_range=[0, 100, 10], axis_config={"include_tip": False}
#         )
#         labels = ax.get_axis_labels(x_label="x", y_label="f(x)")

#         t = ValueTracker(0)

#         def func(x):
#             return 2 * (x - 5) ** 2
#         graph = ax.plot(func, color=MAROON)

#         initial_point = [ax.coords_to_point(t.get_value(), func(t.get_value()))]
#         dot = Dot(point=initial_point)

#         dot.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), func(t.get_value()))))
#         x_space = np.linspace(*ax.x_range[:2],200)
#         minimum_index = func(x_space).argmin()

#         self.add(ax, labels, graph, dot)
#         self.play(t.animate.set_value(x_space[minimum_index]))
#         self.wait()

# #endregion

# class myClass(Scene):
#     def construct(self):
#         #region: transform and positioning
#         myObj = Line()
#         myObj.set_fill(BLUE, opacity=0.5)
#         myObj.set_stroke(BLUE_E, width=4)

#         square = Square()
#         square.set_fill(RED, opacity=0.7)
#         square.set_stroke(RED_A, width=4)

#         triangle = Triangle()
#         triangle.set_fill(GREEN, opacity=0.7)
#         triangle.set_stroke(GREEN_A, width=4)

#         circle = Circle()
#         circle.set_fill(GREEN, opacity=0.7)
#         circle.set_stroke(GREEN_A, width=4)

#         self.play(ShowCreation(myObj))
#         self.wait()
#         self.play(Transform(myObj, square))
#         self.wait()
#         self.play(Transform(myObj, triangle))
#         self.wait()
#         self.play(Transform(myObj, circle))
#         self.wait()
#         square_ = Square()
#         square_.set_fill(YELLOW, opacity=0.5) 
#         square_.next_to(myObj, RIGHT, buff=0.5)
#         self.play(ShowCreation(square_))
#         self.wait()
#         self.play(FadeOut(square_), FadeOut(myObj))
#         self.wait()
#         #endregion

#         #region: animating
#         square = Square()
#         circle = Circle()

#         self.play(ShowCreation(square))
#         self.wait(0.5)
#         self.play(square.animate.rotate(PI/4))
#         self.wait()
#         self.play(Transform(square, circle))
#         self.wait()
#         self.play(square.animate.set_fill(RED, opacity=0.9))
#         self.wait()
#         #endregion
#         self.embed()

