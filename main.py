from Generator_iter2 import GeneratorImpl

from P3_1 import TestParameterizerImpl3_1
from P3_2 import TestParameterizerImpl3_2
from P3_3 import TestParameterizerImpl3_3
from P3_4 import TestParameterizerImpl3_4
from P2_1 import TestParameterizerImpl2_1
from P1_1 import TestParameterizerImpl1_1
from P4_1 import TestParameterizerImpl4_1

solvers = {
    "t3_1": TestParameterizerImpl3_1,
    "t3_2": TestParameterizerImpl3_2,
    "t3_3": TestParameterizerImpl3_3,
    "t3_4": TestParameterizerImpl3_4,
    "t2_1": TestParameterizerImpl2_1,
    "t1_1": TestParameterizerImpl1_1,
    "t4_1": TestParameterizerImpl4_1
}

g = GeneratorImpl(solvers)

g.createTickets(30, html=True, startIndex=10, withTitle=False)
g.createAllTasksTex()
g.createAllTasksHtml()
g.checkAllTasks()