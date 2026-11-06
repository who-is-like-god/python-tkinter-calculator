from types import SimpleNamespace

import pytest

from app import CalculatorApp


@pytest.fixture
def app_with_spies(monkeypatch):
    app = CalculatorApp.__new__(CalculatorApp)

    calls = []

    monkeypatch.setattr(
        app, "show_input",
        lambda value: calls.append(("input", value))
    )
    monkeypatch.setattr(
        app, "expression",
        lambda value: calls.append(("calculate", value))
    )
    monkeypatch.setattr(
        app, "clear_input",
        lambda value: calls.append(("clear", value))
    )
    return app, calls

@pytest.mark.parametrize(
    "character",
    list("0123456789.+-*/%")
)
def test_keyboard_input(app_with_spies, character):
    app, calls = app_with_spies

    event = SimpleNamespace(char=character, keysym=character)

    result = app.handle_keypress(event)

    assert calls == [("input", character)]
    assert result == "break"


@pytest.mark.parametrize(
    "keysym",
    ["Return", "KP_Enter"]
)
def test_enter_key_calculates(app_with_spies, keysym):
    app, calls = app_with_spies

    event = SimpleNamespace(char="\r", keysym=keysym)

    app.handle_keypress(event)

    assert calls == [("calculate", "=")]


def test_equals_key_calculates(app_with_spies):
    app, calls = app_with_spies

    event = SimpleNamespace(char="=", keysym="equal")

    app.handle_keypress(event)

    assert calls == [("calculate", "=")]


def test_backspace_deletes_last_character(app_with_spies):
    app, calls = app_with_spies

    event = SimpleNamespace(char="\b", keysym="BackSpace")

    app.handle_keypress(event)

    assert calls == [("clear", "del")]


def test_escape_clears_calculator(app_with_spies):
    app, calls = app_with_spies

    event = SimpleNamespace(char="\x1b", keysym="Escape")

    app.handle_keypress(event)

    assert calls == [("clear", "AC")]


def test_unsupported_key_is_ignored(app_with_spies):
    app, calls = app_with_spies

    event = SimpleNamespace(char="a", keysym="a")

    result = app.handle_keypress(event)

    assert calls == []
    assert result is None
