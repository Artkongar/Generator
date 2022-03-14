from sympy.parsing.latex import *
from sympy import *

from pylatex import Document, Section, Subsection, Command, Package
from pylatex.utils import italic, NoEscape

import random


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

    def getTicketLatex(self):
        tasks = self.getTasks()
        answers = self.getAnswers()

        if (len(tasks) != len(tasks)):
            raise Exception('Tasks and answers amount are not equal')

        doc = Document()
        doc.packages.append(Package('fontenc', 'T2A'))
        doc.packages.append(Package('lingmacros'))
        doc.packages.append(Package('amsmath'))

        doc.preamble.append(Command('title', 'Awesome Title'))
        doc.preamble.append(Command('author', 'Anonymous author'))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(r'\maketitle'))

        for i in range(len(tasks)):
            taskLatexQuery = tasks[i].getLatexQuery()
            answerLatexQuery = answers[i]
            with doc.create(Section(tasks[i].getTaskDescription() + ": ")):
                doc.append(NoEscape("Задание: $ " + taskLatexQuery + " $"))
                doc.append(NoEscape("\\" * 4))
                doc.append(NoEscape("Ответ: $ " + answerLatexQuery + " $"))
        doc.generate_tex('ticket')

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

answers = ticket1.getAnswers()
print(answers)
ticket1.getTicketLatex()


'''
class Generator:
    __tasksArray = None

    def __init__(self):
        self.__tasksArray = []

    def addTask(self, task):
        self.__tasksArray.append(task)

    def setTaskArray(self, tasks):
        self.__tasksArray = tasks

    def getTasksAnswers(self):
        taskAnswers = None
        for task in self.__tasksArray:
            taskAnswer = task.getAnswerLatexText()
            if (taskAnswers == None):
                taskAnswers = []
            taskAnswers.append(taskAnswer)
        return taskAnswers
'''