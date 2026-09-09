"""Ellipse definition: two changing distances, one fixed sum."""
import numpy as np
from manim import (
    Scene, Text, MathTex, Axes, Dot, Line, VGroup, Rectangle, DecimalNumber,
    ValueTracker, always_redraw, ParametricFunction, TracedPath, FadeIn,
    FadeOut, Create, Write, TransformFromCopy, linear, config,
)

config.background_color = '#101C30'
INK, GOLD, BLUE, MUTED = '#F2F5FA', '#FFC66D', '#86C8FF', '#B2C0D4'


class EllipseDefinition(Scene):
    def construct(self):
        def text(words, size=25, color=MUTED):
            return Text(words, font='Segoe UI', font_size=size, color=color)

        title = text('WHAT MAKES AN ELLIPSE?', 28).move_to([0, 3.45, 0])
        equation = MathTex(r'\frac{x^2}{25}+\frac{y^2}{9}=1',
                           font_size=49, color=INK).move_to([0, 2.65, 0])
        self.add(title, equation)
        axes = Axes(x_range=[-6, 6, 1], y_range=[-4, 4, 1],
                    x_length=6.6, y_length=4.4,
                    axis_config={'color': '#53647E', 'include_tip': False,
                                 'include_ticks': True, 'tick_size': .04})
        axes.move_to([-3.25, -.2, 0])
        origin = text('(0, 0)', 18).move_to(axes.c2p(0, -.5))
        curve = ParametricFunction(lambda t: axes.c2p(5*np.cos(t), 3*np.sin(t)),
                                   t_range=[0, 2*np.pi], color=INK, stroke_width=3)
        verts = VGroup(*[MathTex(s, font_size=25, color=MUTED).move_to(axes.c2p(x,y))
                        for s,x,y in [('5',5,-.5),('-5',-5,-.5),('3',.45,3.3),('-3',.5,-3.4)]])
        note = text('Start with an ellipse centered at the origin.', 27).move_to([0,-3.3,0])
        self.play(Create(axes), FadeIn(origin), FadeIn(note), run_time=1)
        self.play(Create(curve), FadeIn(verts), run_time=2)
        self.wait(1.5)

        def say(words):
            nonlocal note
            self.play(FadeOut(note), run_time=.2)
            note = text(words, 26).move_to([0,-3.3,0])
            self.play(FadeIn(note), run_time=.3)

        f1, f2 = axes.c2p(-4,0), axes.c2p(4,0)
        focus1, focus2 = Dot(f1, color=GOLD), Dot(f2,color=BLUE)
        labels = VGroup(MathTex(r'F_1\ (-4,0)',font_size=25,color=GOLD).move_to(axes.c2p(-4,-.85)),
                        MathTex(r'F_2\ (4,0)',font_size=25,color=BLUE).move_to(axes.c2p(4,-.85)))
        setup = MathTex(r'a=5,\quad b=3',r'\quad c=\sqrt{25-9}=4',
                        font_size=29,color=MUTED).move_to([3.25,1.75,0])
        self.play(FadeIn(focus1),FadeIn(focus2),FadeIn(labels),Write(setup),run_time=1.3)
        say('These two fixed points are the foci. They stay put.')
        self.wait(2)

        theta, radius = ValueTracker(np.pi/2), ValueTracker(1)
        def coords():
            t,r=theta.get_value(),radius.get_value()
            return np.array([5*r*np.cos(t),3*r*np.sin(t)])
        def position():
            return axes.c2p(*coords())
        def distances():
            p=coords()
            return np.linalg.norm(p-[-4,0]), np.linalg.norm(p-[4,0])
        point = always_redraw(lambda: Dot(position(),radius=.085,color=INK))
        p_label = always_redraw(lambda: MathTex('P',font_size=27,color=INK).move_to(position()+[-.25,.28,0]))
        seg1 = always_redraw(lambda: Line(f1,position(),color=GOLD,stroke_width=5))
        seg2 = always_redraw(lambda: Line(f2,position(),color=BLUE,stroke_width=5))
        self.play(Create(seg1),Create(seg2),FadeIn(point),FadeIn(p_label),run_time=1)
        self.add(seg1,seg2,point,p_label)

        # The meter is scaled in graph units, so its moving boundary represents d1.
        meter_x, meter_y, unit = 1.0, .45, .4
        legend = MathTex(r'PF_1', '+', r'PF_2', font_size=40,color=INK).move_to([3,1.05,0])
        legend[0].set_color(GOLD);legend[2].set_color(BLUE)
        meter1 = always_redraw(lambda: Rectangle(width=unit*distances()[0],height=.28,
            fill_color=GOLD,fill_opacity=1,stroke_width=0).move_to([meter_x+unit*distances()[0]/2,meter_y,0]))
        meter2 = always_redraw(lambda: Rectangle(width=unit*distances()[1],height=.28,
            fill_color=BLUE,fill_opacity=1,stroke_width=0).move_to([meter_x+unit*(distances()[0]+distances()[1]/2),meter_y,0]))
        ticks=VGroup(*[Line([meter_x+unit*v,.18,0],[meter_x+unit*v,.08,0],color=MUTED)
                      for v in range(11)])
        fixed_end=Line([5,.05,0],[5,.85,0],color=INK,stroke_width=2)
        ten=text('10',22,INK).move_to([5,-.18,0])
        zero=text('0',22).move_to([1,-.18,0])
        n1=DecimalNumber(5,num_decimal_places=2,font_size=36,color=GOLD).move_to([1.7,-.85,0])
        n2=DecimalNumber(5,num_decimal_places=2,font_size=36,color=BLUE).move_to([3.25,-.85,0])
        total=DecimalNumber(10,num_decimal_places=2,font_size=36,color=INK).move_to([5,-.85,0])
        n1.add_updater(lambda m:m.set_value(distances()[0]))
        n2.add_updater(lambda m:m.set_value(distances()[1]))
        # Add the displayed rounded measurements so the visible arithmetic agrees.
        total.add_updater(lambda m:m.set_value(sum(round(d,2) for d in distances())))
        signs=VGroup(MathTex('+',font_size=32).move_to([2.5,-.85,0]),
                     MathTex('=',font_size=32).move_to([4.1,-.85,0]))
        self.play(FadeIn(legend),FadeIn(ticks),FadeIn(fixed_end),FadeIn(ten),FadeIn(zero),
                  FadeIn(signs),FadeIn(n1),FadeIn(n2),FadeIn(total),run_time=.8)
        self.play(TransformFromCopy(seg1,meter1),TransformFromCopy(seg2,meter2),run_time=1.5)
        self.add(meter1,meter2)
        say('At the top, the distances are 5 and 5. Together: 10.')
        self.wait(2)
        say('As P moves, one distance grows while the other shrinks.')
        self.play(theta.animate.set_value(0),run_time=4,rate_func=linear)
        self.wait(1)
        say('At the right end: 9 + 1 = 10. The total has not changed.')
        self.wait(2)
        say('Keep moving: the two lengths trade off, but still total 10.')
        self.play(theta.animate.set_value(-np.pi),run_time=6,rate_func=linear)
        say('At the left end: 1 + 9 = 10. Different lengths, same sum.')
        self.wait(2)
        say('Return to the top, where both distances are 5.')
        self.play(theta.animate.set_value(-3*np.pi/2),run_time=3,rate_func=linear)

        say('Inside the ellipse, the two distances add to less than 10.')
        self.play(radius.animate.set_value(.45),run_time=2)
        self.wait(2)
        say('Outside the ellipse, they add to more than 10.')
        self.play(radius.animate.set_value(1.22),run_time=2.5)
        self.wait(2)
        say('Exactly 10 puts P back on the ellipse.')
        self.play(radius.animate.set_value(1),run_time=2)
        self.wait(1)

        self.play(FadeOut(curve),run_time=.6)
        say('Imagine a taut 10-unit string: focus to P to focus.')
        self.wait(2)
        trace=TracedPath(position,stroke_color=INK,stroke_width=3)
        self.add(trace)
        say('Keeping that total fixed traces the ellipse itself.')
        self.play(theta.animate.set_value(theta.get_value()+2*np.pi),run_time=10,rate_func=linear)
        definition=text('An ellipse is every point P\nwhose distances to two fixed foci\nhave the same sum.',23,INK)
        definition.move_to([3.2,-1.9,0])
        self.play(FadeIn(definition),run_time=.8)
        say('The equation and the fixed-distance rule describe the same curve.')
        self.wait(4)
