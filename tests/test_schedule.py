from collections import namedtuple
from nose.tools import eq_, assert_almost_equal

from simpyple.schedule import Line, Schedule
from simpyple.tests.asserts import assert_list_pairs_have_same_relative_distance


Point = namedtuple("Point", ["x", "y"])


class TestLine(object):
    def test_known_points(self):
        p0 = Point(1.25, 12)
        p1 = Point(-0.3, 4)
        l = Line(p0.x, p0.y, p1.x, p1.y)
        eq_(p0.y, l.value(p0.x))
        eq_(p1.y, l.value(p1.x))

    def test_float_values_are_insensitive_to_initial_int_points(self):
        l = Line(1, 0, 3, 1)
        eq_(0.5, l.value(2))


RAMP_QUANTITY = 10
FULL_LOAD_QUANTITY = 20
INITIAL_DELAY = 1
FULL_LOAD_DELAY = 0.5
TOTAL_QUANTITY = RAMP_QUANTITY * 2 + FULL_LOAD_QUANTITY

class TestSchedule(object):
    def setup(self):
        self.schedule = Schedule(RAMP_QUANTITY, FULL_LOAD_QUANTITY, INITIAL_DELAY, FULL_LOAD_DELAY)
        self.values = [self.schedule.next(index) for index in range(TOTAL_QUANTITY)]
        self.delay_increment = (INITIAL_DELAY - FULL_LOAD_DELAY) / RAMP_QUANTITY

    def _ramp_up(self):
        return sum(INITIAL_DELAY - i * self.delay_increment for i in range(RAMP_QUANTITY))

    def test_full_load_after_ramp_up_shows_constant_rate(self):
        assert_almost_equal(FULL_LOAD_QUANTITY * FULL_LOAD_DELAY, self.schedule.full_load - self.schedule.ramp_up)
        for i in range(RAMP_QUANTITY, RAMP_QUANTITY + FULL_LOAD_QUANTITY):
            assert_almost_equal(FULL_LOAD_DELAY, self.values[i] - self.values[i - 1])

    def test_ramp_up_and_ramp_down_are_anti_symmetrical(self):
        assert_almost_equal(self._ramp_up(), self.schedule.ramp_up)
        assert_almost_equal(self.schedule.ramp_up + self.schedule.full_load, self.schedule.ramp_down)
        ramp_up_values = self.values[:RAMP_QUANTITY]
        ramp_down_values = self.values[RAMP_QUANTITY + FULL_LOAD_QUANTITY - 1:TOTAL_QUANTITY - 1]
        ramp_down_values.reverse()
        assert_list_pairs_have_same_relative_distance(ramp_up_values, ramp_down_values)

    def test_first_and_last_values_happen_after_initial_delay(self):
        eq_(INITIAL_DELAY, self.values[0])
        eq_(INITIAL_DELAY, self.values[-1] - self.values[-2])

    def test_delays_decrement_linearly_during_ramp_up_until_full_load_delay(self):
        distance = INITIAL_DELAY
        for i in range(1, RAMP_QUANTITY):
            assert_almost_equal(distance - self.delay_increment, self.values[i] - self.values[i - 1])
            distance -= self.delay_increment
