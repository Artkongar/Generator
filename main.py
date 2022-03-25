from sympy import *
from sympy.abc import x

import random
from Generator_iter2 import Parameterizer, Generator


class TestParameterizer1(Parameterizer):

    def solveExpression(self):
        v_a = 1  # random.randint(1, 10)
        v_b = 2  # random.randint(1, 10)
        v_c = 1  # random.randint(1, 10)
        v_d = 2  # random.randint(1, 10)

        v1 = exp(v_c / x)
        v2 = x ** v_d
        v3 = Integral(v1 / v2, (x, v_a, v_b)).doit()

        variableBinding = {
            "a": v_a,
            "b": v_b,
            "c": v_c,
            "d": v_d,
            "r_a": v3
        }

        return variableBinding


class TestParameterizer2(Parameterizer):
    'Limit((x**2 + x - 2)/(sqrt(x + 6) - 1*2), x, -2)'

    def solveExpression(self):
        # q1 = 2
        # q2 = 1
        # q3 = -2
        q1 = random.randint(-10, 10)
        q2 = random.randint(-10, 10)
        q3 = random.randint(-10, 10)
        v1 = x ** q1 + q2 * x + q3

        # q4 = 6
        # q5 = -2
        q4 = random.randint(-10, 10)
        q5 = random.randint(-10, 10)
        v2 = sqrt(x + q4) + q5

        # q6 = -2
        q6 = random.randint(-10, 10)
        result = Limit(v1 / v2, x, q6)

        bindings = {
            "a": q6,
            "b": q1,
            "c": q2,
            "d": q3,
            "e": q4,
            "f": q5,
            "r_a": result.doit()
        }

        return bindings


class TestParameterizer3(Parameterizer):
    def solveExpression(self):
        a = random.randint(-10, 10)
        b = random.randint(a + 1, 20)
        t = 1 / 100 * random.randint(1, 100 - 1)
        c = (a + b) * (1 - t) + 2 * b * t
        q0 = 2 * a
        q1 = a + b
        q2 = 2 * b
        q3 = lambda x: (x - 2 * a) ** 2 / (2 * (a - b) ** 2)
        q4 = lambda x: 1 - (x - 2 * b) ** 2 / (2 * (a - b) ** 2)
        q5 = lambda x: simplify((x - 2 * a) / ((a - b) ** 2))
        q6 = lambda x: (2 * b - x) / ((a - b) ** 2)
        qc = 1 - (c - 2 * b) ** 2 / (2 * (a - b) ** 2)

        bindings = {
            "a": a,
            "b": b,
            "c": c,
            "Q0": q0,
            "Q1": q1,
            "Q2": q2,
            "Q3": q3(x),
            "Q4": q4(x),
            "Q5": q5(x),
            "Q6": q6(x),
            "G": 1,
            "QC": qc,
        }
        return bindings

solvers = {"Q1": TestParameterizer1, "Q2": TestParameterizer2, "Q3": TestParameterizer3}
g = Generator(solvers)
g.createTickets(10)
