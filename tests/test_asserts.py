from nose.tools import raises, assert_raises_regexp

from asserts import assert_list_pairs_have_same_relative_distance

class TestAsserts(object):
    def test_assert_list_pairs_have_same_relative_distance_verifies_relative_distance_of_pairs_in_same_position(self):
        assert_list_pairs_have_same_relative_distance([1, 3], [5, 7])
        assert_list_pairs_have_same_relative_distance([1, 2, 4, 7, 11], [5, 6, 8, 11, 15])

    def test_assert_list_pairs_have_same_relative_distance_does_not_verifies_anything_for_degenerate_cases(self):
        assert_list_pairs_have_same_relative_distance([], [])
        assert_list_pairs_have_same_relative_distance([1], [None])

    @raises(AssertionError)
    def test_assert_list_pairs_have_same_relative_distance_cannot_work_when_lists_have_different_lengths(self):
        assert_list_pairs_have_same_relative_distance([], [1])

    def test_assert_list_pairs_have_same_relative_distance_check_until_the_end_the_list(self):
        with assert_raises_regexp(AssertionError, '1 != 2.*, index=1'):
            assert_list_pairs_have_same_relative_distance([1, 2, 3], [1, 2, 4])
