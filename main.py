from Generator_iter2 import Generator

from P3_1 import TestParameterizer3_1
from P3_2 import TestParameterizer3_2
from P3_3 import TestParameterizer3_3
from P3_4 import TestParameterizer3_4

solvers = {
    "t3_1": TestParameterizer3_1,
    "t3_2": TestParameterizer3_2,
    "t3_3": TestParameterizer3_3,
    "t3_4": TestParameterizer3_4
}
g = Generator(solvers)
g.createTickets(10, True)