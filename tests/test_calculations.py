import pytest
from calculations import calculate


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("10+5*2", 20),
        ("20/5*2", 8),
        ("10+20/5*2-3", 15),
        ("100-20-30", 50),
        ("2+3*4", 14),
        ("100%30+5", 15),
    ]
)
def test_calculate(expression, expected):
    result = calculate(expression)

    assert result == expected


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate("10/0")


def test_empty_expression():
    with pytest.raises(ValueError):
        calculate("")


# def test_multiplication_before_addition():
#     result = calculate("10+5*2")
#
#     assert result == 20


@pytest.mark.parametrize(
    "expression",
    [
        "",
        "10+",
        "+10",
        "5++2",
        "abc",
        "10/",
    ]
)
def test_invalid_expression(expression):
    with pytest.raises(ValueError):
        calculate(expression)


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("0.1+0.2", 0.3),
        ("10/3", 10/3),
        ("2.5*1.5", 3.75),
        ("10/4", 2.5),
    ]
)
def test_floating_point_calculations(expression, expected):
    assert calculate(expression) == pytest.approx(expected)


def test_decimal_calculation():
    result = calculate("5.25+5.25")

    assert result == pytest.approx(10.6, abs=0.1)
