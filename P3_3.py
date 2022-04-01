from scipy.stats import triang
from sympy import *
from sympy.abc import x
import numpy as np

import random
from Generator_iter2 import Parameterizer

class TestParameterizer3_3(Parameterizer):
    def solveExpression(self):
        a = random.randint(-10, 10)
        b = random.randint(a + 1, 20)
        q = 1 / 1000 * random.randint(1, 1000 - 1)
        a1 = -(b - a)
        b1 = (b - a)
        c1 = 0
        a2 = np.abs(a1)
        mode = (c1 - a1) / (b1 - a1)
        loc = a1
        scale = b1 - a1
        T = triang(mode, loc, scale)
        c = T.ppf((q + 1) / 2)
        q0 = -(b - a)
        q1 = 0
        q2 = (b - a)
        q3 = lambda x: (x + b - a) ** 2 / (2 * (b - a) ** 2)
        q4 = lambda x: Rational(1 / 2) + x * (2 * (b - a) - x) / (2 * (b - a) ** 2)
        q5 = lambda x: simplify((x + b - a) / ((b - a) ** 2))
        q6 = lambda x: (b - a - x) / ((b - a) ** 2)
        q7 = simplify(b - a)

        bindings = {
            "a": a,
            "b": b,
            "c": c,
            "q": q,
            "Q0": q0,
            "Q1": q1,
            "Q2": q2,
            "Q3": q3(x),
            "Q4": q4(x),
            "Q5": q5(x),
            "Q6": q6(x),
            "Q7": q7,
            "qq":(q+1)/2
        }

        return bindings
