import scipy.stats as stats
import random

from sympy import latex

from Generator import ParameterizerImpl


class TestParameterizerImpl2_1(ParameterizerImpl):
    def solveExpression(self):
        A0 = random.randint(13, 27)  # число степеней свободы
        A1 = random.randint(5, 37) + random.random()
        A2 = stats.chi2.sf(A1, A0)
        A3 = random.randint(73, 97)
        A4 = A3 / 100
        A5 = random.randint(3, 11)  # число степеней свободы
        A6 = stats.chi2.isf(A4, A5)
        dig = 2

        bindings = {
            "0": latex(A0),
            "1": latex(round(A1, dig)),
            "2": latex(A3),
            "4": latex(round(A2, dig)),
            "3": latex(A4),
            "5": latex(A5),
            "6": latex(round(A6, dig))
        }
        return bindings
