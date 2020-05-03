from DBModule import ServiceRepo, ResultRepo
from Models import TaskDTO
import utill
import time


def isOpenTask():
    '''
    Проверят наличие открытых задач для сервиса.
    :return: True - если есть открытые задачи для сервиса.
             False - если открытых задач нету.
    '''

    repo = ServiceRepo()
    return repo.isOpenTask()

def getPageTask():
    '''
    Получает набор открытых задач из БД. Десереализует данные.
    :return: задачи.
    '''

    repo = ServiceRepo()
    data = repo.getTask()

    objects = []
    ids = []
    task_id = data[0][2]
    parcent = data[0][3]
    for item in data:
        ids.append((item[0],))
        objects.append(TaskDTO(item[1]))

    del data

    return objects, ids, task_id, parcent

def getResult(objects):
    resaults = []

    for task in objects:
        resaults.append(task.getResaults())

    return resaults

def main():
    repo = ServiceRepo()
    while True:
        if isOpenTask():
            objects, ids, task_id, parcent = getPageTask()
            for task in objects:
                task.run()

            res = getResult(objects)

            del objects

            result = []
            for item in res:
                line = []
                line.append(utill.format_numbers(item[0][1][0]))
                line.append(utill.format_numbers(item[0][1][1]))
                line.append(utill.format_number(item[0][1][2]))
                line.append(utill.format_number(item[1]))
                line.append(utill.appendOneForNumber(item[2]))
                line.append(utill.appendOneForNumber(item[3]))
                result.append(line)

            repoRes = ResultRepo()
            repoRes.addResults(result, task_id, parcent)

            del res
            del result

            repo.setCompleteTask(ids)
            repo.updateLastActive()
        else:
            time.sleep(10)
            repo.updateLastActive()

if __name__ == "__main__":
    main()