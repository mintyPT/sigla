from src.sigla.ui import __version__
from src.sigla.ui.location import greet


def test_version():
    assert __version__ == '0.1.0'


def test_greet():
    result = greet("America/New_York")
    assert "New York!" in result