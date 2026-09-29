r"""Checks on math_notation: negatives get the short dash, subtraction keeps the minus.

    & '.\.venv\Scripts\python.exe' test_math_notation.py
"""

import sys

from math_notation import HANGING_NEG, NEG, hanging_fraction, negatives


def check_leading_negative():
    assert negatives(['-3y', '<', '2x']) == [NEG + '3y', '<', '2x']


def check_subtraction_keeps_minus():
    # -2x - 3y < 6: the first is a negative, the second subtracts.
    assert negatives(['-2x', '-3y', '<', '6']) == [NEG + '2x', '-3y', '<', '6']
    assert negatives(['y', '>', 'x', '-', '2']) == ['y', '>', 'x', '-', '2']


def check_negative_after_relation_inside_one_part():
    assert negatives(['b = -2']) == ['b = ' + NEG + '2']
    assert negatives(['y', '<', '-8']) == ['y', '<', NEG + '8']


def check_hanging_fraction_puts_negative_on_top():
    assert r'\frac{' + HANGING_NEG + '2}' in hanging_fraction('2', '3')


def main():
    failures = 0
    for check in (check_leading_negative, check_subtraction_keeps_minus,
                  check_negative_after_relation_inside_one_part,
                  check_hanging_fraction_puts_negative_on_top):
        try:
            check()
            print(f'ok    {check.__name__}')
        except AssertionError as problem:
            failures += 1
            print(f'FAIL  {check.__name__}\n    {problem}')
    print('\n' + ('all checks passed' if not failures else f'{failures} check(s) failed'))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
