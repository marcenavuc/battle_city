import pytest
from pytest_mock import mocker

from battle_city.view import Button


@pytest.fixture(autouse=True)
def mock_get_pos(mocker, mouse_coords):
    mocker.patch("pygame.mouse.get_pos", return_value=mouse_coords)


@pytest.mark.parametrize("btn_size, mouse_coords, result", [
    ((0, 0, 10, 10), (5, 5), True),
    ((0, 0, 10, 10), (11, 11), False),
    ((0, 0, 10, 10), (0, 11), False),
    ((0, 0, 10, 10), (11, 0), False),
])
def test_button_is_moused(set_pygame,  btn_size, mouse_coords, result):
    # mocker.patch("pygame.mouse.get_pos", return_value=mouse_coords)
    button = Button(btn_size)
    assert button.is_moused() is result


@pytest.mark.parametrize("mouse_coords, clicked, result", [
    ((5, 5), [True], True)
])
def test_button_is_clicked(set_pygame, mocker,
                           mouse_coords, clicked, result):
    mocker.patch("pygame.mouse.get_pressed", return_value=clicked)
    button = Button((0, 0, 10, 10))  # Здесь координаты не имеют значения
    assert button.is_clicked() is result
