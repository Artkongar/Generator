from scipy.stats import triang
from sympy import *
from sympy.abc import x
import numpy as np

import random
from Generator import ParameterizerImpl


class TestParameterizerImpl3_4(ParameterizerImpl):
    def solveExpression(self):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        t = 1 / 1000 * random.randint(1, 1000 - 1)
        s = 1 + 1 / 1000 * random.randint(1, 1000 - 1)
        z1 = t * b / a
        z2 = s * b / a
        q1 = Rational(b / a).limit_denominator(1550000)
        q1a = b / a
        q3 = lambda x: (a * x) / (2 * b)
        q4 = lambda x: 1 - simplify(b / (2 * a * x))
        q5 = lambda x: Rational(a / (2 * b)).limit_denominator(1550000)
        q6 = lambda x: simplify(b / (2 * a * x ** 2))
        p = (2 * s - 1) / (2 * s) - t / 2

        bindings = {
            "a": latex(a),
            "b": latex(b),
            "z1": latex(z1),
            "z2": latex(z2),
            "q1a": latex(q1a),
            "Q1": latex(q1),
            "Q3": latex(q3(x)),
            "Q4": latex(q4(x)),
            "Q5": latex(q5(x)),
            "Q6": latex(q6(x)),
            "p": latex(p)
        }

        return bindings
