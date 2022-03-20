from utils import all_valid

def test_all_valid():
    
    assert all_valid(True, True, 0)
    assert all_valid(0, True, 0)

    assert not all_valid(True, True, None)
    assert not all_valid(None, True, None)


if __name__ == "__main__":
    test_all_valid()
