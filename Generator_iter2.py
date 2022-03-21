from abc import abstractmethod, ABC

from sympy import *
from sympy.abc import x
from sympy.parsing.latex import *

import os
import re
import random

query = r"\int_{1}^{2} \frac{\exp(\frac{1}{x})dx}{x^{2}}"
q = parse_latex(query)


def get1():
    expression = Integral(exp(1 / x) / x ** 2, (x, 1, 2))
    result = expression.doit()
    return result


class Parameterizer(ABC):
    __expression = None

    def setExpression(self, expr):
        self.__expression = expr

    def getExpression(self):
        return self.__expression

    def parametrizeExpression(self):
        if (self.__expression == None):
            raise Exception('Expression was not set')

        variables = re.findall(r'<([\s\S]*?)>', self.__expression)
        calculatedVariables, answer = self.solveExpression()

        for variable in variables:
            if (variable not in calculatedVariables):
                raise Exception("Not all variables are bound")

        for variable, value in calculatedVariables.items():
            self.__expression = self.__expression.replace(f"<{variable}>", str(value))

        return self.__expression, answer

    @abstractmethod
    def solveExpression(self):
        pass


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

p = TestParameterizer1()
p.setExpression(r"\int_{<a>}^{<b>} \frac{\exp(\frac{<c>}{x})dx}{x^{<d>}}")
result = p.parametrizeExpression()
print(result)




