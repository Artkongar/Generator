from abc import abstractmethod, ABC

from sympy import *

from pylatex import Document
from pylatex.utils import NoEscape

import os
import re
import random
import json


class Parameterizer(ABC):
    __expression = None
    __fileName = None

    def setFileName(self, name):
        self.__fileName = name

    def getFileName(self):
        return self.__fileName

    def setExpression(self, expr):
        self.__expression = expr

    def getExpression(self):
        return self.__expression

    def parametrizeExpression(self):
        if (self.__expression == None):
            raise Exception('Expression was not set')

        variables = re.findall(r'<([\w]*?)>', self.__expression)
        calculatedVariables = self.solveExpression()

        for variable in variables:
            if (variable not in calculatedVariables):
                raise Exception(
                    f"Not all variables are bound\nThis variables must be bound: {variables}\nNo '{variable}' in {[i for i in calculatedVariables]}\nFile name = '{self.__fileName}'")

        for variable, value in calculatedVariables.items():
            self.__expression = self.__expression.replace(f"<{variable}>", "{" + latex(value) + "}")

        return self.__expression

    @abstractmethod
    def solveExpression(self):
        pass


class Generator:
    __solver = {}
    __taskWeight = {}

    def __init__(self, solver):
        self.__solver = solver

    def addSolver(self, taskType, solver):
        self.__solver[taskType] = solver

    def getSolver(self):
        return self.__solver

    def selectFiles(self):
        mainPath = os.getcwd()
        taskPath = os.path.join(mainPath, "tex")

        taskWeightFile = os.path.join(taskPath, "taskWeight.json")
        try:
            with open(taskWeightFile, "r") as read_file:
                self.__taskWeight = json.load(read_file)
        except:
            raise Exception("'taskWeight.json' was not created")
        taskTypesPath = [os.path.join(taskPath, i) for i in os.listdir(taskPath) if
                         i != "packages.tex" and i != "taskWeight.json"]

        ticketFiles = []
        for taskType in taskTypesPath:
            files = [os.path.join(taskType, file) for file in os.listdir(taskType)]
            selectedTaskType = random.choice(files)
            ticketFiles.append(selectedTaskType)
        return ticketFiles

    def getProblemSolution(self, ticketFiles):
        print([i.split("\\")[-1] for i in ticketFiles])
        problemAndSolution = []
        for file in ticketFiles:
            solver = file.split(os.sep)[-1].split(".")[0]
            taskType = file.split(os.sep)[-2]
            f = open(file, encoding="utf-8")
            text = f.read()
            f.close()

            if (solver not in self.__solver):
                raise Exception(f"Add Parametrizator for '{solver}' file")
            solverInstance = self.__solver[solver]()
            solverInstance.setFileName(solver)
            solverInstance.setExpression(text)
            parametrizedText = solverInstance.parametrizeExpression()

            problem = re.findall(r"\\begin\{problem}([\s\S]*?)\\end\{problem}", parametrizedText)
            if (len(problem) != 1):
                raise Exception('Ticket does not contain only 1 problem')
            solution = re.findall(r"\\begin\{solution\*}([\s\S]*?)\\end\{solution\*}", parametrizedText)
            if (len(solution) != 1):
                raise Exception('Ticket does not contain only 1 solution')
            problem, solution = problem[0], solution[0]
            if (taskType not in self.__taskWeight):
                raise Exception("Not all types set in 'taskWeight.json'")
            problem = r"\begin{problem}[" + str(self.__taskWeight[taskType]) + " баллов]\n" + str(problem) + "\n" + r"\end{problem}"
            solution = r"\begin{solution*}" + "\n" + str(solution) + "\n" + r"\end{solution*}"
            problemAndSolution.append([problem, solution])

        return problemAndSolution

    def __createDocTitle(self, ticketNumber):
        doc = Document()
        doc.packages.clear()

        doc.packages.append(NoEscape(
            r"""\usepackage{amsthm}
            \usepackage{amssymb}%
            \usepackage{thmtools}
            \usepackage{graphicx}
            \graphicspath{ {../../signature/} }
            \declaretheoremstyle[headfont=\bfseries]{normalhead}
            \theoremstyle{normalhead}%
            
            \newtheorem*{solution*}{Ответ}
            \newtheorem{problem}{Задание}
            """))

        packageFile = open(os.path.join(os.getcwd(), "tex", "packages.tex"), encoding="utf-8")
        doc.packages.append(NoEscape(packageFile.read()))
        packageFile.close()

        doc.packages.append(NoEscape(r"\usepackage[T2A]{fontenc}%"))
        doc.packages.append(NoEscape(
            r"\usepackage{geometry} \geometry{verbose,a4paper,tmargin=1cm,bmargin=1.2cm,lmargin=1cm,rmargin=1cm}"))

        doc.append(NoEscape(
            r"""\begin{center}
            \centerline{\footnotesize{ФЕДЕРАЛЬНОЕ\,\, ГОСУДАРСТВЕННОЕ\,\, ОБРАЗОВАТЕЛЬНОЕ\,\, БЮДЖЕТНОЕ}}
            \centerline{\footnotesize{УЧРЕЖДЕНИЕ\,\, ВЫСШЕГО\,\, ОБРАЗОВАНИЯ}}
            
            \centerline{\small{\textbf{<<ФИНАНСВЫЙ\,\,УНИВЕРСИТЕТ\,\,ПРИ\,\,ПРАВИТЕЛЬСТВЕ}}}
            \centerline{\small{\textbf{РОССИЙСКОЙ\,\,ФЕДЕРАЦИИ>>}}}
            \centerline{\small{\textbf{(ФИНАНСОВЫЙ УНИВЕРСИТЕТ)}}}
            
            \hfill \break
            \normalsize{Департамент анализа данных и машинного обучения}\\
            
            \hfill \break
            \centerline{\normalsize{{\textit{\textbf{Дисциплина: <<Теория вероятностей и математическая статистика>>}}}}}
            \centerline{\small{\textit{Направление подготовки: 01.03.02 <<Прикладная математика и информатика>>}}}
            \centerline{\small{\textit{Профиль: <<Анализ данных и принятие решений в экономике и финансах>>}}}
            \centerline{\small{\textit{Факультет информационных технологий и анализа больших данных}}}
            \centerline{\small{\textit{Форма обучения очная}}}
            \centerline{\small{\textit{Учебный 2021/2022 год, 3 семестр}}}
            
            \hfill \break
            \centerline{\large{\textbf{""" + f"Билет {ticketNumber}." + """}}}
            \end{center}"""
        ))
        return doc

    def __addDocContent(self, doc, problemsAndSolutions, withAnswers=False):
        taskAndAnswerIndex = 0
        for task in problemsAndSolutions:
            problem = task[0]
            solution = task[1]

            doc.append(NoEscape(problem))
            if (withAnswers):
                doc.append(NoEscape(solution))

        doc.append(NoEscape(
            r"""$\\$
            \begin{minipage}{0.3\textwidth}
              Профессор, д.ф.-м.н.
            \end{minipage}
            \hfill
            \begin{minipage}{0.3\textwidth}
              \includegraphics[width=20mm,scale=0.5]{signature}
            \end{minipage}
            \begin{minipage}{0.3\textwidth}
              П. Е. Рябов
            \end{minipage}"""
        ))
        return doc

    def createTickets(self, n):
        if "answers" not in os.listdir(os.getcwd()):
            os.mkdir(os.path.join(os.getcwd(), 'answers'))
            os.mkdir(os.path.join(os.getcwd(), 'answers', 'tasks'))
            os.mkdir(os.path.join(os.getcwd(), 'answers', 'answers'))
        else:
            if ("tasks" not in os.listdir(os.path.join(os.getcwd(), 'answers'))):
                os.mkdir(os.path.join(os.getcwd(), 'answers', 'tasks'))
            if ("answers" not in os.listdir(os.path.join(os.getcwd(), 'answers'))):
                os.mkdir(os.path.join(os.getcwd(), 'answers', 'answers'))

        k = 0
        for i in range(n):
            k += 1
            selectedFiles = self.selectFiles()
            problemsAndSolutions = self.getProblemSolution(selectedFiles)

            docWithAnswers, = self.__addDocContent(self.__createDocTitle(k), problemsAndSolutions, True),
            doc = self.__addDocContent(self.__createDocTitle(k), problemsAndSolutions)

            texFileAnsPostfix = "_answers"
            texFileName = 'ticket' + str(k)

            docWithAnswers.generate_tex(texFileName + texFileAnsPostfix)
            doc.generate_tex(texFileName)

            os.replace(
                os.path.join(os.getcwd(), texFileName + texFileAnsPostfix + ".tex"),
                os.path.join(os.getcwd(), "answers", "answers", texFileName + texFileAnsPostfix + ".tex")
            )
            os.replace(
                os.path.join(os.getcwd(), texFileName + ".tex"),
                os.path.join(os.getcwd(), "answers", "tasks", texFileName + ".tex")
            )
