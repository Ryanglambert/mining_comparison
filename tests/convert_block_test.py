from nose.tools import *
from plot_chunk import *

def setup(): 
    global plot_dict
    plot_dict = {
            'diamond':('b', 'o')
            }
    print "setup!"

def teardown():
    #del plot_dict
    print "TEAR DOWN!"

def test_convert_block():
    block = ['diamond', 1, 3, 2]
    converted_block = convert_block_id_to_scatter_color(block)
    assert_equal(
            [('b', 'o'), 1, 3, 2], converted_block)

setup()
test_convert_block()
teardown()
