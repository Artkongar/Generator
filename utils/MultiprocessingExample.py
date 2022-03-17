import numpy as np
import time
import multiprocessing


def resolver(task, return_dict):
    value = task.getAnswerLatexText()
    return_dict[multiprocessing.current_process().name] = value


def calculateTaskAnswerSync(taskArray, timeout, attempts):
    notDoneCounter = len(taskArray)

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    processInd = [str(i) for i in range(len(taskArray))]
    for att in range(attempts):
        if (notDoneCounter == 0):
            break
        else:
            processes = []
            for i in range(notDoneCounter):
                p = multiprocessing.Process(target=resolver, args=(taskArray[i], return_dict), name=(processInd[i]))
                print('process_' + str(processInd[i]))
                processes.append(p)
            for process in processes:
                process.start()

            isAliveList = []
            start = time.time()
            while (time.time() - start) <= timeout:
                isAliveList = [process.is_alive() for process in processes]
                print(time.time() - start)
                if np.any(isAliveList):
                    time.sleep(.1)
                else:
                    break

            for j in range(len(processes)):
                if isAliveList[j]:
                    processes[j].terminate()
                else:
                    processInd.remove(processes[j].name)
                    notDoneCounter -= 1
            for proc in processes:
                proc.join()
            print(f'dict_len = {return_dict}')
    return return_dict
