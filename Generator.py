from sympy.parsing.latex import *
from sympy import *

from pylatex import Document, Section, Subsection, Command, Package
from pylatex.utils import italic, NoEscape

import random

from utils.MultiprocessingExample import calculateTaskAnswerSync

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

    __calculateTimeout = 30
    __calculateAttempts = 3

    def __init__(self):
        self.__taskArray = []

    def setCalculateTimeout(self, value):
        self.__calculateTimeout = value

    def setCalculateAttempts(self, value):
        self.__calculateAttempts = value

    def getCalculateTimeout(self):
        return self.__calculateTimeout

    def getCalculateAttempts(self):
        return self.__calculateAttempts

    def addTask(self, task):
        self.__taskArray.append(task)

    def getTasks(self):
        return self.__taskArray

    def clear(self):
        self.__taskArray = []

    def getAnswers(self):
        answers = None
        if (len(self.__taskArray) != 0):
            answers = calculateTaskAnswerSync(self.__taskArray, self.__calculateTimeout, self.__calculateAttempts)

        return answers

    def getTicketLatex(self):
        tasks = self.getTasks()
        answers = self.getAnswers()

        print(len(tasks),  len(answers))
        #if (len(tasks) != len(answers)):
        #    raise Exception('Tasks and answers amount are not equal')

        doc = Document()
        doc.packages.append(Package('fontenc', 'T2A'))
        doc.packages.append(Package('lingmacros'))
        doc.packages.append(Package('amsmath'))

        doc.preamble.append(Command('title', 'Awesome Title'))
        doc.preamble.append(Command('author', 'Anonymous author'))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(r'\maketitle'))


        #for i in range(len(tasks)):
        #    taskLatexQuery = tasks[i].getLatexQuery()
        #    answerLatexQuery = answers[str(i)]
        #    print(answerLatexQuery)
        #    with doc.create(Section(tasks[i].getTaskDescription() + ": ")):
        #        doc.append(NoEscape("Задание: $ " + taskLatexQuery + " $"))
        #        doc.append(NoEscape("\\" * 4))
        #        doc.append(NoEscape("Ответ: $ " + answerLatexQuery + " $"))
        #doc.generate_tex('ticket')
