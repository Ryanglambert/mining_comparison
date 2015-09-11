from nose.tools import *
from block_handler import get_subset_of_type

def setup(): 
    print "setup!"

def teardown():
    print "TEAR DOWN!"

def test_get_subset_of_type():
    block_array = {
            (2,2,3):'diamond',
            (1,1,1):'stone',
            (2,2,8):'diamond',
            (0,2,3):'diamond',
            (1,1,2):'stone',
            }
    desired_array = {
            (2,2,3):'diamond',
            (2,2,8):'diamond',
            (0,2,3):'diamond',
            }
    filtered_array = get_subset_of_type(block_array, 'diamond')

    assert_equal(filtered_array, desired_array)

setup()
test_get_subset_of_type()
teardown()
