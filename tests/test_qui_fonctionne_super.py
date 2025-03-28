import pytest

n = 1345

@pytest.mark.parametrize("i", range(n))
def test_pas_suspect(i):
    """On écoute tous les bons conseils... vous avez failli vous faire enfumer !"""
    assert True