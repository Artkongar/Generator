from abc import abstractmethod, ABC

from sympy import *

from pylatex import Document, Section, Command, Package
from pylatex.utils import NoEscape

import os
import re
import random


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
        calculatedVariables = self.solveExpression()

        for variable in variables:
            if (variable not in calculatedVariables):
                raise Exception("Not all variables are bound")

        for variable, value in calculatedVariables.items():
            self.__expression = self.__expression.replace(f"<{variable}>", "{" + latex(value) + "}")

        return self.__expression

    @abstractmethod
    def solveExpression(self):
        pass


class Generator:
    __solver = {}

    def __init__(self, solver):
        self.__solver = solver

    def addSolver(self, taskType, solver):
        self.__solver[taskType] = solver

    def getSolver(self):
        return self.__solver

    def selectFiles(self):
        mainPath = os.getcwd()
        taskPath = os.path.join(mainPath, "tex")

        taskTypesPath = [os.path.join(taskPath, i) for i in os.listdir(taskPath) if i != "packages.txt"]
        ticketFiles = []
        for taskType in taskTypesPath:
            files = [os.path.join(taskType, file) for file in os.listdir(taskType)]
            selectedTaskType = random.choice(files)
            ticketFiles.append(selectedTaskType)
        return ticketFiles

    def getProblemSolution(self, ticketFiles):
        problemAndSolution = []
        for file in ticketFiles:
            solver = file.split(os.sep)[-2]
            f = open(file, encoding="utf-8")
            text = f.read()
            f.close()

            solverInstance = self.__solver[solver]()
            solverInstance.setExpression(text)
            parametrizedText = solverInstance.parametrizeExpression()

            problem = re.findall(r"\\begin\{problem\*}([\s\S]*?)\\end\{problem\*}", parametrizedText)
            if (len(problem) != 1):
                raise Exception('Ticket does not contain only 1 problem')
            solution = re.findall(r"\\begin\{solution\*}([\s\S]*?)\\end\{solution\*}", parametrizedText)
            if (len(solution) != 1):
                raise Exception('Ticket does not contain only 1 solution')
            problem, solution = problem[0], solution[0]

            problem = r"\begin{problem*}" + "\n" + str(problem) + "\n" + r"\end{problem*}"
            solution = r"\begin{solution*}" + "\n" + str(solution) + "\n" + r"\end{solution*}"
            problemAndSolution.append([problem, solution])

        return problemAndSolution

    def createTickets(self, n):
        k = 0
        for i in range(n):
            k += 1
            selectedFiles = self.selectFiles()
            problemsAndSolutions = self.getProblemSolution(selectedFiles)

            doc = Document()
            doc.packages.append(Package('fontenc', 'T2A'))
            doc.packages.append(Package('lingmacros'))
            doc.packages.append(Package('amsmath'))
            doc.packages.append(Package('amsthm'))
            doc.packages.append(Package('amssymb'))
            doc.packages.append(NoEscape(r'\newtheorem*{problem*}{Problem}'))
            doc.packages.append(NoEscape(r'\newtheorem*{solution*}{Solution}'))

            doc.preamble.append(Command('title', 'Awesome Title'))
            doc.preamble.append(Command('author', 'Anonymous author'))
            doc.preamble.append(Command('date', NoEscape(r'\today')))
            doc.append(NoEscape(r'\maketitle'))

            for task in problemsAndSolutions:
                problem = task[0]
                solution = task[1]
                with doc.create(Section("Задание ")):
                    doc.append(NoEscape(problem))
                    doc.append(NoEscape(solution))
            texAnswerFileName = 'ticket' + str(k)
            doc.generate_tex(texAnswerFileName)
            os.replace(os.path.join(os.getcwd(), texAnswerFileName + ".tex"), os.path.join(os.getcwd(), "answers", texAnswerFileName + ".tex"))

