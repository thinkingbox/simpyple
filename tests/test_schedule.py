from collections import namedtuple
from nose.tools import eq_, assert_almost_equal

from simpyple.schedule import Line, Schedule


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


class TestSchedule(object):
    RAMP_QUANTITY = 10
    FULL_LOAD_QUANTITY = 20
    INITIAL_DELAY = 1
    FULL_LOAD_DELAY = 0.5
    TOTAL_QUANTITY = RAMP_QUANTITY * 2 + FULL_LOAD_QUANTITY
    def setup(self):
        self.schedule = Schedule(self.RAMP_QUANTITY, self.FULL_LOAD_QUANTITY, self.INITIAL_DELAY, self.FULL_LOAD_DELAY)
        self.values = [self.schedule.next(index) for index in range(self.TOTAL_QUANTITY)]

    def _ramp_up(self):
        delay_increment = (self.INITIAL_DELAY - self.FULL_LOAD_DELAY) / self.RAMP_QUANTITY
        return sum(self.INITIAL_DELAY - i * delay_increment for i in range(self.RAMP_QUANTITY))

    def test_full_load_after_ramp_up_shows_constant_rate(self):
        assert_almost_equal(self.FULL_LOAD_QUANTITY * self.FULL_LOAD_DELAY, self.schedule.full_load - self.schedule.ramp_up)
        for i in range(self.RAMP_QUANTITY, self.RAMP_QUANTITY + self.FULL_LOAD_QUANTITY):
            assert_almost_equal(self.FULL_LOAD_DELAY, self.values[i] - self.values[i - 1])

    def test_ramp_up_and_ramp_down_are_anti_symmetrical(self):
        assert_almost_equal(self._ramp_up(), self.schedule.ramp_up)
        assert_almost_equal(self.schedule.ramp_up + self.schedule.full_load, self.schedule.ramp_down)
        for i in range(self.RAMP_QUANTITY - 1):
            assert_almost_equal(self.values[self.RAMP_QUANTITY - i - 1] - self.values[self.RAMP_QUANTITY - i - 2], self.values[self.RAMP_QUANTITY + self.FULL_LOAD_QUANTITY + i] - self.values[self.RAMP_QUANTITY + self.FULL_LOAD_QUANTITY + i - 1], msg="index={}".format(i))

    # TODO: show that it increments by 0.05 at each ramp step + show a simpler profile
