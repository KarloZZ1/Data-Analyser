from project import load,drop_col,graphs

import pytest
import pandas as pd



#test load function
def test_load():
    #test if load exits program when there is file with other extension than csv
    with pytest.raises(SystemExit):
        load("test.pdf")

    #test if load return dataframe object when corret name is given
    object = load('csv_files/test1.csv')
    assert isinstance(object, pd.DataFrame)
    #test if the shape is correct
    assert object.shape == (891,12)

#test if drop_col return a dataframe object with correct columns
def test_drop_col():

    object = pd.read_csv('csv_files/test2.csv')
    object1 = pd.read_csv('csv_files/test1.csv')

    #create two pd variables
    object = drop_col(object)
    object1 = drop_col(object1)
    #assume the number of columns is correct
    assert object.shape == (614,12)
    assert object1.shape == (891,8)

#test if graphs raises assertion error if the target column isnt binary

def test_graphs():
    object1 = pd.read_csv('csv_files/test1.csv')
    with pytest.raises(AssertionError):
        graphs(object1,"Age")











