from abc import abstractmethod, ABC

from sympy import *

from pylatex import Document
from pylatex.utils import NoEscape

import os
import shutil
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
    __isTicketGenerated = False
    __withTitle = False

    def __init__(self, solver):
        self.__solver = solver

    def addSolver(self, taskType, solver):
        self.__solver[taskType] = solver

    def getSolver(self):
        return self.__solver

    def __selectFiles(self):
        self.__loadTaskWeights()

        mainPath = os.getcwd()
        taskPath = os.path.join(mainPath, "tex")
        taskTypesPath = [os.path.join(taskPath, i) for i in os.listdir(taskPath) if
                         i != "packages.tex" and i != "taskWeight.json"]
        ticketFiles = []
        for taskType in taskTypesPath:
            files = [os.path.join(taskType, file) for file in os.listdir(taskType)]
            selectedTaskType = random.choice(files)
            ticketFiles.append(selectedTaskType)
        return ticketFiles

    def __loadTaskWeights(self):
        taskWeightFile = os.path.join(os.path.join(os.getcwd(), "tex"), "taskWeight.json")
        try:
            with open(taskWeightFile, "r") as read_file:
                self.__taskWeight = json.load(read_file)
        except:
            raise Exception("'taskWeight.json' was not created")

    def __getProblemSolution(self, ticketFiles):
        problemAndSolution = {}

        for file in ticketFiles:
            solver = file.split(os.sep)[-1].split(".")[0]
            taskType = file.split(os.sep)[-2]
            if (taskType not in self.__taskWeight):
                raise Exception("Not all types set in 'taskWeight.json'")
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

            if (taskType not in problemAndSolution):
                problemAndSolution[taskType] = []
            problemAndSolution[taskType].append([problem, solution])
        return problemAndSolution

    def __wrapContentForHtml(self, content):
        newContent = ""
        isOpen = False
        for word in content:
            if (word == "$"):
                if (isOpen == False):
                    newContent += "\("
                    isOpen = True
                else:
                    newContent += "\)"
                    isOpen = False
            else:
                newContent += word
        return newContent

    def __getProblemSolutionHtml(self, ticketFiles):
        problemsAndSolutions = self.__getProblemSolution(ticketFiles)
        result = {}
        for taskType, problemsAndSolutions_ in problemsAndSolutions.items():
            wrappedProblemAndSolution = []
            for problemAndSolution in problemsAndSolutions_:
                wrappedProblemAndSolution.append([
                    self.__wrapContentForHtml(problemAndSolution[0]),
                    self.__wrapContentForHtml(problemAndSolution[1])
                ])
            result[taskType] = wrappedProblemAndSolution

        return result

    def __getProblemSolutionTex(self, ticketFiles):
        problemsAndSolutions = self.__getProblemSolution(ticketFiles)
        result = {}
        for taskType, problemsAndSolutions_ in problemsAndSolutions.items():
            wrappedProblemAndSolution = []
            for problemAndSolution in problemsAndSolutions_:
                wrappedProblemAndSolution.append([
                    str(problemAndSolution[0]),
                    str(problemAndSolution[1])
                ])
            result[taskType] = wrappedProblemAndSolution
        return result

    def __createDocTitleTex(self, ticketNumber):
        doc = Document()
        doc.packages.clear()

        doc.packages.append(NoEscape(
            r"""\usepackage{amsthm}
            \usepackage{amssymb}%
            \usepackage{thmtools}
            \usepackage{graphicx}
            \usepackage[russian]{babel}
            \graphicspath{ {../../signature/} }
            \declaretheoremstyle[headfont=\bfseries]{normalhead}
            \theoremstyle{normalhead}%
            
            \newtheorem*{solution*}{Ответ}
            \newtheorem{problem}{}
            """))

        packageFile = open(os.path.join(os.getcwd(), "tex", "packages.tex"), encoding="utf-8")
        doc.packages.append(NoEscape(packageFile.read()))
        packageFile.close()

        doc.packages.append(NoEscape(r"""
        \usepackage[T2A]{fontenc}%
        \usepackage{geometry} \geometry{verbose,a4paper,tmargin=1cm,bmargin=1.2cm,lmargin=1cm,rmargin=1cm}
        \usepackage{ragged2e}
        \justifying"""))

        doc = self.__addTexHeader(doc, ticketNumber)
        return doc

    def __addTexHeader(self, doc, counter):
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
            \centerline{\large{\textbf{""" + f"Билет {counter}." + """}}}
                    \end{center}"""
        ))
        return doc

    def __addDocContentTex(self, doc, problemsAndSolutions, withAnswers=False):
        for taskType, content in problemsAndSolutions.items():
            for problemAndSolution in content:
                problem, solution = problemAndSolution
                taskTypeDef = ""
                if (self.__withTitle and withAnswers):
                    taskTypeDef += self.__taskWeight[taskType][0]
                doc.append(NoEscape(r"\begin{problem}" + "\n(" + str(
                    self.__taskWeight[taskType][1]) + ") " + taskTypeDef + "\n" + problem + r"\end{problem}" + "\n"))
                if (withAnswers):
                    doc.append(NoEscape("\n" + r"\begin{solution*}" + solution + r"\end{solution*}" + "\n"))

        if (withAnswers == False):
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

    def __checkAnswersFolder(self):
        answersPath = ['tickets', 'answers', 'html_tickets', 'html_answers', 'all_tickets_tex',
                       'all_tickets_answers_tex',
                       'all_tickets_html', 'all_tickets_answers_html']
        if "answers" not in os.listdir(os.getcwd()):
            os.mkdir(os.path.join(os.getcwd(), 'answers'))
            for i in answersPath:
                os.mkdir(os.path.join(os.getcwd(), 'answers', i))
        else:
            for i in answersPath:
                if (i not in os.listdir(os.path.join(os.getcwd(), 'answers'))):
                    os.mkdir(os.path.join(os.getcwd(), 'answers', i))

    def __createHtmlTicket(self, problemsAndSolutions, counter, ticketPrifix, withAnswers=False):
        htmlTemplatePath = os.path.join(os.getcwd(), "html", "utils")
        htmlTemplateFile = os.path.join(htmlTemplatePath, "html_template.html")

        ticketHtmlFileName = ""
        htmlTicketFile = None
        if (withAnswers):
            ticketHtmlFileName = ticketPrifix + str(counter) + "_answers.html"
            htmlTicketFile = os.path.join(htmlTemplatePath, ticketHtmlFileName)
        else:
            ticketHtmlFileName = ticketPrifix + str(counter) + ".html"
            htmlTicketFile = os.path.join(htmlTemplatePath, ticketHtmlFileName)
        shutil.copyfile(htmlTemplateFile, htmlTicketFile)

        f = open(htmlTicketFile, "a", encoding="utf-8")
        f.write(r"""<h5>Билет """ + str(counter) + r"""</h5><div id="content">""")
        f.write(f"<title>{ticketHtmlFileName}</title>")
        taskCounter = 0
        for taskType, content in problemsAndSolutions.items():
            for problemAndSolution in content:
                newProblem, newSolution = problemAndSolution
                taskCounter += 1
                taskTypeDef = ""
                if (self.__withTitle and withAnswers):
                    taskTypeDef = " <span class=\"task_number\"><b>" + self.__taskWeight[taskType][0] + "</b><br>"
                f.write("<div> <b><span class=\"task_number\">" + str(taskCounter) + ".</span></b> (" + str(
                    self.__taskWeight[taskType][1]) + ")" + taskTypeDef + newProblem + "</div>")
                if (withAnswers):
                    f.write("<div> <b><span>" + "Ответ" + ".</span></b>" + newSolution + "</div>")

        packagesFile = open(os.path.join(os.getcwd(), "tex", "packages.tex"), "r", encoding="utf-8")
        packages = packagesFile.read()
        packagesFile.close()
        f.write(
            r"""
            </div>
            <table style='width:80%;margin-top:20px;border-width:0;margin-right:40px'>
                <tr>
                    <td align='left'> &nbsp; Профессор, д.ф.-м.н.</td>
                    <td align='center'><img src='../../signature/signature.png' width='90' height='50'/></td>
                    <td align='right'>П.Е. Рябов</td>
                </tr>
            </table>
            </BODY>
            <script>
            document.getElementById("packages").textContent = `\\(""" + packages.replace("\\", "\\\\") + """\\\\)`
            ;</script>
            </html>
            """)
        f.close()
        self.__checkAnswersFolder()

        if (withAnswers == False):
            htmlAnswersPath = os.path.join(os.getcwd(), "answers", "html_tickets")
            os.replace(htmlTicketFile, os.path.join(htmlAnswersPath, ticketPrifix + str(counter) + ".html"))
        else:
            htmlAnswersPath = os.path.join(os.getcwd(), "answers", "html_answers")
            os.replace(htmlTicketFile, os.path.join(htmlAnswersPath, ticketPrifix + str(counter) + "_answers.html"))

    def __createTexTicket(self, problemsAndSolutions, counter, withAnswers=False):
        doc = self.__addDocContentTex(self.__createDocTitleTex(counter), problemsAndSolutions)

        texFileAnsPostfix = "_answers"
        texFileName = 'ticket' + str(counter)

        doc.generate_tex(texFileName)
        os.replace(
            os.path.join(os.getcwd(), texFileName + ".tex"),
            os.path.join(os.getcwd(), "answers", "tickets", texFileName + ".tex")
        )

        if (withAnswers):
            docWithAnswers = self.__addDocContentTex(self.__createDocTitleTex(counter), problemsAndSolutions, True)
            docWithAnswers.generate_tex(texFileName + texFileAnsPostfix)
            os.replace(
                os.path.join(os.getcwd(), texFileName + texFileAnsPostfix + ".tex"),
                os.path.join(os.getcwd(), "answers", "answers", texFileName + texFileAnsPostfix + ".tex")
            )

    def createTickets(self, n, html=False, startIndex=1, withTitle=False):
        self.__withTitle = withTitle
        self.__checkAnswersFolder()
        k = startIndex
        for i in range(n):
            selectedFiles = self.__selectFiles()

            problemSolutionTex = self.__getProblemSolutionTex(selectedFiles)
            self.__createTexTicket(problemSolutionTex, k, True)

            if (html):
                problemSolutionHtml = self.__getProblemSolutionHtml(selectedFiles)
                self.__createHtmlTicket(problemSolutionHtml, k, "ticket", True)
                self.__createHtmlTicket(problemSolutionHtml, k, "ticket")

            k += 1
        self.__isTicketGenerated = True

    def __writeAllTasksInOneTexFile(self, fromPath, toPath):
        if (self.__isTicketGenerated == False):
            raise Exception("Tickets were not generated")

        self.__loadTaskWeights()
        self.__checkAnswersFolder()

        ticketFiles = [os.path.join(fromPath, i) for i in sorted(os.listdir(fromPath)) if i.split(".")[-1] == "tex"]

        title = None
        resultFileName = "all.tex"
        resultFile = open(os.path.join(toPath, resultFileName), "w", encoding="utf-8")
        for file in ticketFiles:
            f = open(file, "r", encoding="utf-8")
            fileContent = f.read()
            if (title == None):
                title = re.findall(r"\\documentclass\{article}([\s\S]*?)\\begin\{document}", fileContent)[0]
                resultFile.write(r"\documentclass{article}")
                resultFile.write(title)
                resultFile.write(r"\begin{document}")
            documentContent = re.findall(r"\\begin\{document}([\s\S]*?)\\end\{document}", fileContent)[0]
            resultFile.write(documentContent)
            resultFile.write(r"\newpage")
            f.close()

        resultFile.write("\end{document}")
        resultFile.close()

    def createAllTasksTex(self):
        mainPath = os.getcwd()
        self.__writeAllTasksInOneTexFile(
            os.path.join(mainPath, "answers", "answers"),
            os.path.join(mainPath, "answers", "all_tickets_answers_tex")
        )
        self.__writeAllTasksInOneTexFile(
            os.path.join(mainPath, "answers", "tickets"),
            os.path.join(mainPath, "answers", "all_tickets_tex")
        )

    def __writeAllTasksInOneHTMLFile(self, fromPath, toPath):
        if (self.__isTicketGenerated == False):
            raise Exception("Tickets were not generated")
        self.__loadTaskWeights()
        self.__checkAnswersFolder()

        ticketFiles = [os.path.join(fromPath, i) for i in sorted(os.listdir(fromPath))]
        resultFileName = "all.html"
        resultFile = open(os.path.join(toPath, resultFileName), "w", encoding="utf-8")
        for file in ticketFiles:
            f = open(file, "r", encoding="utf-8")
            fileContent = f.read()
            resultFile.write(fileContent)
            f.close()
            resultFile.write("<hr/>" + "<br>" * 2)
        resultFile.close()

    def createAllTasksHtml(self):
        self.__loadTaskWeights()
        self.__checkAnswersFolder()

        mainPath = os.getcwd()
        self.__writeAllTasksInOneHTMLFile(
            os.path.join(mainPath, "answers", "html_answers"),
            os.path.join(mainPath, "answers", "all_tickets_answers_html")
        )
        self.__writeAllTasksInOneHTMLFile(
            os.path.join(mainPath, "answers", "html_tickets"),
            os.path.join(mainPath, "answers", "all_tickets_html")
        )
