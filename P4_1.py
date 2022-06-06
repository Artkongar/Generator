import math
import os.path

import scipy.stats as stats

import numpy as np
import pandas as pd

from Generator import ParameterizerImpl


def createDataSet(ticketNumber, dataSet, path):
    if ("datasets" not in os.listdir(os.getcwd())):
        os.mkdir(os.path.join(os.getcwd(), "datasets"))
    var = 1
    dataSetFileName = f"ds{ticketNumber}_{var}.csv"
    while (dataSetFileName in os.listdir(os.path.join(os.getcwd(), path))):
        var += 1
        dataSetFileName = f"ds{ticketNumber}_{var}.csv"
    dataSetPath = os.path.join(path, dataSetFileName)
    dataSet.to_csv(dataSetPath, header=False, index=False, decimal=',', sep=';', encoding='cp1251')
    return dataSetFileName


class TestParameterizerImpl4_1(ParameterizerImpl):
    def solveExpression(self):
        ticketNumber = self.getTicketNumber()

        mean = [0, 0]
        cov = [[1, -0.13], [-0.13, 1]]
        ns = [27, 28, 29, 31, 32, 33, 34, 36, 37]  # ns = возможные объемы выборки
        n = ns[np.random.randint(len(ns))]
        z = np.random.multivariate_normal(mean, cov, n)
        x, y = z.T
        hatrho = np.corrcoef(x, y)[0][1]
        dfz = pd.DataFrame(z)
        dataSetFileName = createDataSet(ticketNumber, dfz, "datasets")
        gamma = (np.random.randint(60, 97)) / 100
        alpha = 1 - gamma
        z_al = stats.norm.isf(alpha / 2)
        z_n = math.atanh(hatrho)
        teta_1 = math.tanh(z_n - 1 / math.sqrt(n - 3) * z_al)
        teta_2 = math.tanh(z_n + 1 / math.sqrt(n - 3) * z_al)

        bindings = {
            "0": dataSetFileName,
            "1": gamma,
            "2": round(hatrho, 3),
            "3": round(teta_1, 3),
            "4": round(teta_2, 3)
        }
        return bindings
