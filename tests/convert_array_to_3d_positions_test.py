from nose.tools import *
from block_plotter import *

def setup(): 



def teardown():
    print "TEAR DOWN!"

def test_convert_array_to_3d_positions():
    one_dimensional_array = [1,2,3,4,5,6,7,8]
    desired_three_dimensional = [
            [
                [1,2],### Bottom
                [3,4]
                ],
            [
                [5,6],### Top
                [7,8]
                ]
            ]
    assert_equal(converted_one_dimensional, desired_three_dimensional)

def test_reproduce_properly():
    activeDrugs = []
    popDensity = .001
    child_virus = virus.reproduce(popDensity, activeDrugs)

    assert_equal(child_virus.mutProb, global_mutProb)


#setup()
#test_return_values_properly()
#test_reproduce_properly()
#teardown()
