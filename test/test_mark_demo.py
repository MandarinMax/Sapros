import pytest

@pytest.mark.skip
@pytest.mark.smoke
def test_one():
    pass


def test_two():
    pass

@pytest.mark.smoke
def test_three_smok():
    pass

@pytest.mark.regression
def test_regression():
    pass

@pytest.mark.integration
def test_integration():
    pass

@pytest.mark.critical
def test_critical():
    pass

@pytest.mark.critical
@pytest.mark.regression
def test_critical_and_regression():
    assert 1 == 2



    # smoke
    # regression
    # integration
    # critical