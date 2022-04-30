from scipy.stats import triang
from sympy import *
from sympy.abc import x
import numpy as np

import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

import random
from Generator_iter2 import ParameterizerImpl

def figure(k,A,B,C):
    a1=-(B-A)
    b1=(B-A)
    c1=0
    a2=np.abs(a1)
    mode = (c1 - a1) / (b1-a1)
    loc = a1
    scale = b1-a1
    T=triang(mode,loc,scale)
    fig,ax =plt.subplots(figsize=(10, 5))
    plt.tick_params(labelsize = 20)
    ax.set_xlim(xmin=a1, xmax=b1)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(8))
    ax.xaxis.set_minor_locator(ticker.MaxNLocator(40))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(6))
    plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
    plt.ylim(0.,2.0/(b1-a1)+0.01)
    plt.xlim(a1-2,b1+2)
    x1 = np.linspace(a1-2, b1+2, 1000)
    y1 = T.pdf(x1)
    plt.plot(x1, y1, 'k-',lw=5)
    y0=0
    plt.fill_between(x1,y1,y0, color='orange', alpha=0.2)
    font0 = FontProperties()
    font = font0.copy()
    font.set_style('italic')
    font.set_weight('bold')
    fig.savefig('pictures/' + "t3_3_1_" + str(k) + '.png', bbox_inches='tight')


class TestParameterizerImpl3_3(ParameterizerImpl):
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
        figure(self.getTicketNumber(), a, b, c)

        bindings = {
            "a": latex(a),
            "b": latex(b),
            "c": latex(c),
            "q": latex(q),
            "Q0": latex(q0),
            "Q1": latex(q1),
            "Q2": latex(q2),
            "Q3": latex(q3(x)),
            "Q4": latex(q4(x)),
            "Q5": latex(q5(x)),
            "Q6": latex(q6(x)),
            "Q7": latex(q7),
            "qq": (q + 1) / 2,
            "Image": "t3_3_1_" + str(self.getTicketNumber())
        }
        return bindings
