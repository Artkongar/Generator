import scipy.stats as stats

import random

from numpy import sqrt
from sympy import Rational, exp, pi, symbols, latex

from Generator import ParameterizerImpl


class TestParameterizerImpl1_1(ParameterizerImpl):
    def solveExpression(self):
        x, y, a, b, c, d, e = symbols('x y a b c d e')
        sol = [[1, 4, 25], [5, 4, 5], [25, 4, 1], [1, 3, 25], [5, 3, 5], [25, 3, 1], [13, 12, 13], [4, 8, 25],
               [5, 8, 20],
               [10, 8, 10], [20, 8, 5], [25, 8, 4], [25, 24, 25], [4, 6, 25], [5, 6, 20], [10, 6, 10], [20, 6, 5],
               [25, 6, 4],
               [17, 15, 17], [5, 12, 45], [9, 12, 25], [15, 12, 15], [25, 12, 9], [45, 12, 5], [41, 40, 41],
               [26, 24, 26],
               [13, 5, 13], [5, 9, 45], [9, 9, 25], [15, 9, 15], [25, 9, 9], [45, 9, 5], [10, 16, 40], [16, 16, 25],
               [20, 16, 20],
               [25, 16, 16], [40, 16, 10], [37, 35, 37], [17, 8, 17], [25, 20, 25], [39, 36, 39], [10, 12, 40],
               [16, 12, 25],
               [20, 12, 20], [25, 12, 16], [40, 12, 10], [34, 30, 34], [20, 24, 45], [25, 24, 36], [30, 24, 30],
               [36, 24, 25],
               [45, 24, 20], [25, 15, 25], [29, 21, 29], [29, 20, 29], [25, 28, 49], [35, 28, 35], [49, 28, 25],
               [25, 7, 25],
               [26, 10, 26], [20, 18, 45], [25, 18, 36], [30, 18, 30], [36, 18, 25], [45, 18, 20], [40, 32, 40],
               [45, 36, 45],
               [25, 21, 49], [35, 21, 35], [49, 21, 25], [34, 16, 34], [40, 24, 40], [37, 12, 37], [39, 15, 39],
               [45, 27, 45],
               [41, 9, 41]]

        k = random.randint(0, len(sol) - 1)
        a = sol[k][0]
        b = sol[k][1]
        c = sol[k][2]
        d = random.randint(-10, 10)
        e = random.randint(-10, 10)
        q = lambda x, y: sqrt((a * c - b ** 2)) * exp((Rational(
            ((c * d ** 2 - 2 * b * d * e + a * e ** 2) / (b ** 2 - a * c))).limit_denominator(
            1550000) - 2 * d * x - a * x ** 2 - 2 * e * y - 2 * b * x * y - c * y ** 2) / 2) / (2 * pi)
        muX = Rational((c * d - b * e) / (b ** 2 - a * c)).limit_denominator(1550000)
        muY = Rational((a * e - b * d) / (b ** 2 - a * c)).limit_denominator(1550000)
        VarX = Rational(c / (a * c - b ** 2)).limit_denominator(1550000)
        VarY = Rational(a / (a * c - b ** 2)).limit_denominator(1550000)
        CovXY = Rational(-(b / (a * c - b ** 2))).limit_denominator(1550000)
        rho = Rational(-(b / sqrt(a * c))).limit_denominator(1550000)

        bindings = {
            "Q": latex(q(x,y)),
            "EX": latex(muX),
            "EY": latex(muY),
            "VARX": latex(VarX),
            "VARY": latex(VarY),
            "COVXY": latex(CovXY),
            "RHO": latex(rho)
        }
        return bindings
