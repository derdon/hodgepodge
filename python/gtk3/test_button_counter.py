from button_counter import SimpleApp

import pytest


@pytest.fixture
def window():
    return SimpleApp()


def test_initial_window_attributes(window):
    assert window.counter == 0
    assert window.button.get_label() == '0'


def test_label_change_after_click(window):
    window.button.clicked()
    assert window.counter == 1
    assert window.button.get_label() == '1'
