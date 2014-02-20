"""
Fps counter with averaging.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import time


class FpsCounter:
    def __init__(self):
        self.last_update_time = time.clock()
        self.frame_time_sum = 0.0
        self.frame_time_sum_counter = 0
        self.last_moving_average_calculation_time = 0.0
        self.moving_average_frame_time = 1.0 / 30
        self.previous_moving_average_frame_time = 1.0 / 30
        self.fps_string = "0"

    def tick(self):
        current_time = time.clock()
        frame_time = current_time - self.last_update_time
        self.last_update_time = current_time

        if frame_time > (2 * self.moving_average_frame_time):
            frame_time = 2 * self.moving_average_frame_time

        self.frame_time_sum += frame_time
        self.frame_time_sum_counter += 1

        if (current_time - self.last_moving_average_calculation_time) > (1.0 / 15):
            alpha = 0.25
            self.moving_average_frame_time = alpha * (self.frame_time_sum / self.frame_time_sum_counter) + (1.0 - alpha) * self.previous_moving_average_frame_time

            self.previous_moving_average_frame_time = self.moving_average_frame_time
            self.last_moving_average_calculation_time = current_time

            self.frame_time_sum = 0
            self.frame_time_sum_counter = 0

            self.fps_string = str(int(1.0 / self.moving_average_frame_time))

    def get_fps(self):
        return self.fps_string
