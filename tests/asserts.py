from nose.tools import eq_, assert_almost_equal

def assert_list_pairs_have_same_relative_distance(list1, list2):
    eq_(len(list1), len(list2))
    assert_almost_equal.im_class.longMessage = True         #TODO: does this work in Python3?
    for i in range(len(list1) - 1):
        assert_almost_equal(abs(list1[i + 1] - list1[i]), abs(list2[i + 1] - list2[i]), msg=', index={}'.format(i))
