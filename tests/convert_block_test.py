from nose.tools import *
from plot_chunk import *

hold_plot_dict = plot_dict
def setup(): 
    global plot_dict
    plot_dict = {
            'diamond':('b', 'o')
            }
    print "setup!"

def teardown():
    plot_dict = hold_plot_dict
    print "TEAR DOWN!"

def test_convert_block():
    block = ['diamond', 1, 3, 2]
    converted_block = convert_block_id_to_scatter_color(block)
    assert_equal([plot_dict['diamond'], 1, 3, 2], converted_block)

def test_convert_block_array():
    block_array = [
            ['diamond', 2, 2, 3],
            ['diamond', 1, 2, 0],
            ['diamond', 5, 5, 5]
            ]
    converted_array = convert_block_id_array_to_scatter_color_array(block_array)
    desired_array = [
            [plot_dict['diamond'], 2, 2, 3],
            [plot_dict['diamond'], 1, 2, 0],
            [plot_dict['diamond'], 5, 5, 5]
            ]

setup()
test_convert_block()
test_convert_block_array()
teardown()
