from nose.tools import *
from plot_chunk import *

def setup(): 
    print "setup!"

def teardown():
    print "TEAR DOWN!"

def test_convert_block():
    block = ['diamond', 1, 3, 2]
    converted_block = convert_block_id_to_scatter_color(block)
    assert_equal([plot_dict['diamond'], 1, 3, 2], converted_block)


def test_get_subset_of_type():
    block_array = [
            ['diamond', 2, 2, 3],
            ['diamond', 2, 2, 8],
            ['stone', 1, 2, 0],
            ['diamond', 0, 2, 3],
            ['bedrock', 5, 5, 5]
            ]
    desired_array = [
            ['diamond', 2, 2, 3],
            ['diamond', 2, 2, 8],
            ['diamond', 0, 2, 3]
            ]

    subset = get_subset_of_type(block_array, 'diamond')
    assert_equal(subset, desired_array)

setup()
test_convert_block()
test_get_subset_of_type()
teardown()
