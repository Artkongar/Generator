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
            "d": v_d
        }

        return [variableBinding, v3]


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
            "f": q5
        }
        return (bindings, result.doit())


solvers = {"Q1": TestParameterizer1, "Q2": TestParameterizer2}
g = Generator(solvers)
g.createTickets(10)