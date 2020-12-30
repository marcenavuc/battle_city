import pytest

from battle_city.utils import Vector


@pytest.mark.parametrize("x, y, result", [
    (10, 0, Vector(10, 0)),
    (0, 10.5, Vector(0, 10.5)),
    (-6, 10.5, Vector(-6, 10.5))
])
def test_vector_init(x, y, result):
    vector = Vector(x, y)
    assert vector == result
    assert vector.x == x
    assert vector.y == y


@pytest.mark.parametrize("first, second, result", [
    (Vector(0, 10), 20, Vector(20, 30)),
    (Vector(5.5, 2.5), 0.5, Vector(6, 3)),
    (Vector(5.5, 2.5), Vector(5.5, 2.5), Vector(11, 5))
])
def test_vector_sum(first, second, result):
    assert first + second == result


@pytest.mark.parametrize("first, second, result", [
    (Vector(0, 10), 20, Vector(0, 200)),
    (Vector(5.5, 2.5), 0.5, Vector(2.75, 1.25))
])
def test_vector_mul(first, second, result):
    assert first * second == result
