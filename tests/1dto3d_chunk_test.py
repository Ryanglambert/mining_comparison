from nose.tools import *
from plot_chunk import *

def setup(): 
    print "setup!"

def teardown():
    print "TEAR DOWN!"

def test_get_subset_of_type():
    block_array = [
            ['diamond', 2, 2, 3],
            ['stone',1,1,1],
            ['diamond', 2, 2, 8],
            ['diamond', 0, 2, 3],
            ['stone',1,1,2]
            ]
    desired_array = [
            ['diamond', 2, 2, 3],
            ['diamond', 2, 2, 8],
            ['diamond', 0, 2, 3]
            ]
    filtered_array = get_subset_of_type(block_array, 'diamond')

    assert_equal(filtered_array, desired_array)

setup()
test_get_subset_of_type()
teardown()
