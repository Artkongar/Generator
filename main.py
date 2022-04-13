from Generator_iter2 import Generator

from P3_1 import TestParameterizer3_1
from P3_2 import TestParameterizer3_2
from P3_3 import TestParameterizer3_3
from P3_4 import TestParameterizer3_4
from P2_1 import TestParameterizer2_1
from P1_1 import TestParameterizer1_1

solvers = {
    "t3_1": TestParameterizer3_1,
    "t3_2": TestParameterizer3_2,
    "t3_3": TestParameterizer3_3,
    "t3_4": TestParameterizer3_4,
    "t2_1": TestParameterizer2_1,
    "t1_1": TestParameterizer1_1
}

g = Generator(solvers)

g.createTickets(5, html=True, startIndex=10, withTitle=True)
g.createAllTasksTex()
g.createAllTasksHtml()