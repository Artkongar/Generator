from abc import abstractmethod, ABC


class Generator(ABC):

    @abstractmethod
    def createAllTasksTex(self):
        pass

    @abstractmethod
    def createTickets(self, n, html=False, startIndex=1, withTitle=False):
        pass

    @abstractmethod
    def createAllTasksHtml(self):
        pass

    @abstractmethod
    def checkAllTasks(self):
        pass


class Parameterizer(ABC):

    @abstractmethod
    def setTicketNumber(self):
        pass

    @abstractmethod
    def getTicketNumber(self):
        pass

    @abstractmethod
    def setFileName(self):
        pass

    @abstractmethod
    def getFileName(self):
        pass

    @abstractmethod
    def setExpression(self):
        pass

    @abstractmethod
    def getExpression(self):
        pass

    @abstractmethod
    def parametrizeExpression(self):
        pass

    @abstractmethod
    def solveExpression(self):
        pass
