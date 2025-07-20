from manim import *
import numpy as np
from scipy import signal

class FieldSequence(Scene):
    """Dynamically plots the external magnetic field sequence for transport experminents."""

    def construct(self):
        """Manim entry point."""
        
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 3, 1],
            tips=True,
            axis_config={
                "include_numbers": False,
                "tick_size": 0.05,
                "tip_width": 0.1,
                "tip_height": 0.2,
                "stroke_width": 4,
                "include_ticks": True,
            },
        )
        axes.set_color(BLACK)

        labels = axes.get_axis_labels(
            Tex(r"$t$").scale(1), 
            Tex(r"$H_\text{ext}$").scale(1)
        )
        labels.set_color(BLACK)

        self.add(axes, labels)

        def square_wave(t, period, amplitude):
            signal = np.sin(2 * np.pi * t / period) 
            return signal

            return np.where(signal > 0, amplitude * np.ones(np.shape(t)), -amplitude * np.ones(np.shape(t)))

        def trapzoid_signal(t, width=2., slope=1., amp=1., offs=0):
            a = slope*width*signal.sawtooth(2*np.pi*t/width, width=0.5)/4.
            if a > amp:
                a = amp
            if a < -amp:
                a = -amp
            return a + offs

        Hx = axes.plot(lambda t: 4 * trapzoid_signal(t+2, width=8, slope=1.5, amp=0.5), 
                       color=BLACK,
                       stroke_width=5,
                       x_range=[0, 10])
        Hz = axes.plot(lambda t: 2 * trapzoid_signal(t, width=8, slope=1.5, amp=0.5) if t > 2 else 0, 
                       color=BLACK,
                       stroke_width=5,
                       x_range=[2, 10])
        Hx_label = Tex(r"$H_z$", color=BLACK).scale(1)
        Hz_label = Tex(r"$H_x$", color=BLACK).scale(1)
        Hx_label.move_to([-5.1, 2.2, 0])
        Hz_label.move_to([-2.7, 1, 0])

        self.play(
            Create(Hx, run_time=5), 
            Succession(
                Wait(1.0),
                Create(Hz, run_time=3.5), 
            ),
            Succession(
                Wait(1),
                FadeIn(Hx_label, run_time=0.5),
                Wait(0.5),
                FadeIn(Hz_label, run_time=0.5),
            ),
        )

