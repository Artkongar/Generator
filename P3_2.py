from sympy import *
from sympy.abc import x

import random
from Generator_iter2 import Parameterizer

class TestParameterizer3_2(Parameterizer):
    def solveExpression(self):
        a = random.randint(-10, 10)
        b = random.randint(a + 1, 20)
        s = 1 / 100 * random.randint(1, 100 - 1)
        t = 1 / 100 * random.randint(1, 100 - 1)
        d = 2 * a * (1 - s) + s * (a + b)
        c = (a + b) * (1 - t) + 2 * b * t
        q0 = 2 * a
        q1 = a + b
        q2 = 2 * b
        q3 = lambda x: (x - 2 * a) ** 2 / (2 * (a - b) ** 2)
        q4 = lambda x: 1 - (x - 2 * b) ** 2 / (2 * (a - b) ** 2)
        q5 = lambda x: simplify((x - 2 * a) / ((a - b) ** 2))
        q6 = lambda x: (2 * b - x) / ((a - b) ** 2)
        p = (1 - (c - 2 * b) ** 2 / (2 * (a - b) ** 2)) - ((d - 2 * a) ** 2 / (2 * (a - b) ** 2))

        bindings = {
            "a": a,
            "b": b,
            "c": c,
            "d": d,
            "Q0": q0,
            "Q1": q1,
            "Q2": q2,
            "Q3": q3(x),
            "Q4": q4(x),
            "Q5": q5(x),
            "Q6": q6(x),
            "P": p
        }

        return bindings
