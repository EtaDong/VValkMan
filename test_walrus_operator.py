from pydemo1 import walrus_operator_demo1
import pytest

def test_walrus_operator_with_data():
    input_list =[10, 20]
    result = walrus_operator_demo1(input_list)
    assert "size: 2" in result

def test_walrus_opeartor_empty():
    assert walrus_operator_demo1([]) == "empty"







