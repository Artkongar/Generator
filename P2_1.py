import scipy.stats as stats

import random

from sympy import latex

from Generator_iter2 import Parameterizer


class TestParameterizer2_1(Parameterizer):
    def solveExpression(self):
        A0 = random.randint(13, 27)  # число степеней свободы
        A1 = random.randint(5, 37) + random.random()
        A2 = stats.chi2.sf(A1, A0)
        A3 = random.randint(73, 97)
        A4 = A3 / 100
        A5 = random.randint(3, 11)  # число степеней свободы
        A6 = stats.chi2.isf(A4, A5)
        dig = 5

        bindings = {
            "0": latex(A0),
            "1": latex(A1),
            "2": latex(A3),
            "4": latex(A2),
            "3": latex(A4),
            "5": latex(A5),
            "6": latex(A6)
        }
        return bindings
