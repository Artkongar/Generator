from scipy.stats import triang
from sympy import *
from sympy.abc import x
import numpy as np

import random
from Generator_iter2 import Parameterizer

class TestParameterizer3_4(Parameterizer):
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
            "a": a,
            "b": b,
            "z1": z1,
            "z2": z2,
            "q1a": q1a,
            "Q1": q1,
            "Q3": q3(x),
            "Q4": q4(x),
            "Q5": q5(x),
            "Q6": q6(x),
            "p": p
        }

        return bindings
