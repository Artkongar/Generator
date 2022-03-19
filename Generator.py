from sympy.parsing.latex import *
from sympy import *

from pylatex import Document, Section, Subsection, Command, Package
from pylatex.utils import italic, NoEscape

import random
import os
import re


class Task:
    __taskDescription = None
    __latexTask = None
    __bindings = []
    __valueRangeMin = None
    __valueRangeMax = None

    def setTaskDescription(self, taskDescription):
        self.__taskDescription = taskDescription

    def getTaskDescription(self):
        return self.__taskDescription

    def setLatexTask(self, task):
        self.__latexTask = task

    def getLatexTask(self):
        return self.__latexTask

    def setIntRangeValues(self, valueRangeMin, valueRangeMax):
        self.__valueRangeMin = valueRangeMin
        self.__valueRangeMax = valueRangeMax

    def getIntRangeValues(self):
        return self.__valueRangeMin, self.__valueRangeMax

    def setBindings(self, *values):
        self.__bindings = values

    def getLatexQuery(self):

        if (None not in (self.__latexTask, self.__valueRangeMin, self.__valueRangeMax)):
            template = self.__latexTask
            values = self.__bindings
            valueRangeMin = self.__valueRangeMin
            valueRangeMax = self.__valueRangeMax

            query = ""
            valuesInd = 0
            for char in template:
                if (char == "?"):
                    addingValue = ""
                    if (len(values) == 0):
                        addingValue = random.randint(valueRangeMin, valueRangeMax)
                    else:
                        addingValue = values[valuesInd]
                        valuesInd += 1
                    if (addingValue < 0):
                        addingValue = '{' + str(addingValue) + '}'
                    query += str(addingValue)
                else:
                    query += char
            return query
        else:
            raise Exception("Not all fields are filled")

    def __getExpression(self):
        query = self.getLatexQuery()
        expr = parse_latex(query)
        return expr

    def getAnswerLatexText(self):
        try:
            expr = self.__getExpression()
            return latex(expr.doit())
        except LaTeXParsingError as e:
            print(e)


class Ticket:
    __taskArray = None
    __ticketTitle = None
    __ticketNumber = None

    def setTicketTitle(self, title):
        self.__ticketTitle = title

    def setTicketNumber(self, value):
        self.__ticketNumber = value

    def getTicketNumber(self):
        return self.__ticketNumber

    def getTicketTitle(self):
        return self.__ticketTitle

    def __init__(self):
        self.__taskArray = []

    def addTask(self, task):
        self.__taskArray.append(task)

    def getTasks(self):
        return self.__taskArray

    def clear(self):
        self.__taskArray = []

    def getAnswers(self):
        answers = None
        if (len(self.__taskArray) != 0):
            answers = []
        for task in self.__taskArray:
            taskAnswer = task.getAnswerLatexText()
            answers.append(taskAnswer)
        return answers

    def getTicketLatex(self, fileName):
        tasks = self.getTasks()
        answers = self.getAnswers()

        if (len(tasks) != len(tasks)):
            raise Exception('Tasks and answers amount are not equal')

        doc = Document()
        doc.packages.append(Package('fontenc', 'T2A'))
        doc.packages.append(Package('lingmacros'))
        doc.packages.append(Package('amsmath'))

        doc.preamble.append(Command('title', self.__ticketTitle))
        doc.preamble.append(Command('author', self.__ticketNumber))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(r'\maketitle'))

        for i in range(len(tasks)):
            taskLatexQuery = tasks[i].getLatexQuery()
            answerLatexQuery = answers[i]
            with doc.create(Section(tasks[i].getTaskDescription() + ": ")):
                doc.append(NoEscape("Задание: $ " + taskLatexQuery + " $"))
                doc.append(NoEscape("\\" * 4))
                doc.append(NoEscape("Ответ: $ " + answerLatexQuery + " $"))
        doc.generate_tex(fileName)


class Generator:

    def parseTickets(self, n):
        filePath = os.path.join(os.getcwd(), 'tex')
        files = os.listdir(filePath)

        selectedFiles = []
        for j in range(n):
            oneTicketFiles = []
            for path in [path for path in files if path != "packages.txt"]:
                taskFilePath = os.path.join(filePath, path)
                taskFiles = os.listdir(taskFilePath)

                selectedTaskFileName = os.path.join(taskFilePath, random.choice(taskFiles))
                oneTicketFiles.append(selectedTaskFileName)
            selectedFiles.append(oneTicketFiles)

        fileNameIndex = 0
        for oneTicketFiles in selectedFiles:
            t = Ticket()
            t.setTicketTitle("Экзамен по математике")
            t.setTicketNumber("Билет № " + str(fileNameIndex + 1))
            for i in oneTicketFiles:
                f = open(i, encoding="utf-8")
                ticketData = f.read()
                f.close()

                task = Task()

                description = re.findall('<begin description>([\s\S]*?)<end description>', ticketData)[0].replace("\n",
                                                                                                                  "")
                problem = re.findall(r'<begin problem>([\s\S]*?)<end problem>', ticketData)[0].replace("\n", "")
                formuls = re.findall(r'<begin formula>([\s\S]*?)<end formula', problem)

                task.setTaskDescription(description)
                task.setIntRangeValues(-10, 10)
                task.setLatexTask(formuls[0])

                t.addTask(task)
            fileNameIndex += 1
            texFileName = "ticket_" + str(fileNameIndex)
            t.getTicketLatex(texFileName)

            answersPath = os.path.join(os.getcwd(), 'answers', texFileName + ".tex")
            createdFilePath = os.path.join(os.getcwd(), texFileName + ".tex")
            os.replace(createdFilePath, answersPath)


g = Generator()
g.parseTickets(3)

'''
ticket1 = Ticket()

task1 = Task()
task1.setTaskDescription("Решите интеграл")
task1.setIntRangeValues(-10, 10)
task1.setLatexTask(r"\int_{{?}}^{{?}} \frac{\exp(\frac{?}{x})dx}{x^{?}}")
task1.setBindings(1, 2, 1, 2)

task2 = Task()
task2.setTaskDescription("Решите предел")
task2.setIntRangeValues(-15, 15)
task2.setLatexTask(r"""\lim_{x \to ?} \frac{?x^{?}+?x+?}{\sqrt{?x + ?} +?}""")
task2.setBindings(-2, 1, 2, 1, -2, 1, 6, -2)

ticket1.addTask(task1)
ticket1.addTask(task2)

# answers = ticket1.getAnswers()
# print(answers)
ticket1.getTicketLatex()
'''


class Generator:

    def parseTickets(self):
        filePath = os.path.join(os.getcwd(), 'tex')
        files = os.listdir(filePath)
        selectedFiles = []
        for path in [path for path in files if path != "packages.txt"]:
            taskFilePath = os.path.join(filePath, path)
            taskFiles = os.listdir(taskFilePath)

            selectedTaskFileName = os.path.join(taskFilePath, random.choice(taskFiles))
            selectedFiles.append(selectedTaskFileName)

        t = Ticket()
        for i in selectedFiles:
            f = open(i, encoding="utf-8")
            ticketData = f.read()
            f.close()

            task = Task()

            description = re.findall('<begin description>([\s\S]*?)<end description>', ticketData)[0].replace("\n", "")
            problem = re.findall(r'<begin problem>([\s\S]*?)<end problem>', ticketData)[0].replace("\n", "")
            formuls = re.findall(r'<begin formula>([\s\S]*?)<end formula', problem)

            task.setTaskDescription(description)
            task.setIntRangeValues(-10, 10)
            task.setLatexTask(formuls)

        t.getTicketLatex("ticket_" + str(0))


g = Generator()
g.parseTickets()

'''
ticket1 = Ticket()

task1 = Task()
task1.setTaskDescription("Решите интеграл")
task1.setIntRangeValues(-10, 10)
task1.setLatexTask(r"\int_{{?}}^{{?}} \frac{\exp(\frac{?}{x})dx}{x^{?}}")
task1.setBindings(1, 2, 1, 2)

task2 = Task()
task2.setTaskDescription("Решите предел")
task2.setIntRangeValues(-15, 15)
task2.setLatexTask(r"""\lim_{x \to ?} \frac{?x^{?}+?x+?}{\sqrt{?x + ?} +?}""")
task2.setBindings(-2, 1, 2, 1, -2, 1, 6, -2)

ticket1.addTask(task1)
ticket1.addTask(task2)

# answers = ticket1.getAnswers()
# print(answers)
ticket1.getTicketLatex()
'''
