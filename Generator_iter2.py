import os
import os

from sympy import *
from sympy.abc import x
from sympy.parsing.latex import *

query = r"\int_{1}^{2} \frac{\exp(\frac{1}{x})dx}{x^{2}}"
q = parse_latex(query)


def get1():
    expression = Integral(exp(1 / x) / x ** 2, (x, 1, 2))
    result = expression.doit()
    return result


class Parameterizer:
    __expression = None

    def setExpression(self, expr):
        self.__expression = expr

    def getExpression(self):
        return self.__expression

    def parametrizeExpression(self):
        if (self.__expression == None):
            raise Exception('Expression was not set')

        print(self.__expression)


p = Parameterizer()
p.setExpression(r"\int_{<a>}^{<b>} \frac{\exp(\frac{1}{<c>})dx}{x^{<d>}}")
p.parametrizeExpression()
