import datetime
import psycopg2
from psycopg2.extras import execute_values

import config


def getConnection():
    '''
    Получает соединения с БД.
    :return: соединение с БД.
    '''

    conn = psycopg2.connect(dbname=config.database,
                            user=config.user,
                            password=config.password,
                            host=config.host,
                            port=config.port)
    return conn


class ServiceRepo:
    '''
    Репозиторий для работы с сервисами решения регерессионных уравнений.
    '''

    def getTask(self):
        '''
        Получает набор открытых задач.
        :return: открытые задачи.
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            select = '''
                     SELECT DISTINCT page FROM queue_task
                     WHERE service_id = %s
                       AND complete is FALSE
                     LIMIT 1
                     '''
            cursor.execute(select, (config.service_id,))
            page = cursor.fetchone()[0]

            select = '''
                     SELECT id, task, task_id, parcent
                     FROM queue_task
                     WHERE service_id = %s
                       AND page = %s
                     '''

            cursor.execute(select, (config.service_id, page))
            rows = cursor.fetchall()
            line = []
            for row in rows:
                line.append(row)

        conn.close()
        return line

    def isOpenTask(self):
        '''
        Проверяет наличие открытых задач.
        :return: True - если есть открытые задачи для сервиса
                 False - если нет открытых задач.
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            select = 'SELECT EXISTS(SELECT 1 FROM queue_task WHERE service_id = %s AND complete = FALSE)'

            cursor.execute(select, (config.service_id,))

            isOpenTask = cursor.fetchone()[0]

        conn.close()
        return isOpenTask

    def setCompleteTask(self, ids):
        '''
        Проставляет статусы готовности для задач.
        :param ids: идентификаторы задач
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            update = 'UPDATE queue_task AS t SET complete = TRUE FROM (VALUES %s) AS e(id) WHERE e.id = t.id'

            execute_values(cur=cursor, sql=update, argslist=ids)
        conn.close()

    def updateLastActive(self):
        '''
        Обновляет время последней активности.
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            update = 'UPDATE service_list SET last_active = %s WHERE id = %s'

            dateTime = datetime.datetime.now()
            value = (dateTime, config.service_id,)
            cursor.execute(update, value)

        conn.close()

class ResultRepo:
    '''
    Репозитория для работы с данными результов вычислений.
    '''

    def getNewIndex(self):
        '''
        Получает новый идентификатор результов вычислений.
        :return: новый идентификатор.
        '''

        conn = getConnection()

        with conn.cursor() as cursor:
            conn.autocommit = True

            select = "select nextval('result_id_seq')"

            cursor.execute(select)

            id = cursor.fetchone()[0]

        conn.close()
        return id

    def setResult(self, result):
        '''
        Добавляет результаты вычислений.
        :param result: результаты вычислений.
        :return: идентификатор результатов вычислений.
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            insert = 'INSERT INTO result (alfa, epselon, e, bias_estimates, n1, n2) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id'

            values = (str(result[0]),
                      str(result[1]),
                      str(result[2]),
                      str(result[3]),
                      str(result[4]),
                      str(result[5]),)

            cursor.execute(insert, values)

        conn.close()
        return cursor.fetchone()[0]

    def setResults(self, results):
        '''
        Добавляет результаты вычислений.
        :param result: результаты вычислений.
        :return: идентификатор результатов вычислений.
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            insert = 'INSERT INTO result (alfa, epselon, e, bias_estimates, n1, n2) VALUES %s RETURNING id'

            values = []
            for item in results:
                values.append((str(item[0]),
                               str(item[1]),
                               str(item[2]),
                               str(item[3]),
                               str(item[4]),
                               str(item[5]),))

            id_res = execute_values(cur=cursor, sql=insert, argslist=values, fetch=True)

        conn.close()
        return id_res

    def createTask(self, type=None):
        '''
        Создаёт новый идентификатор для задачи.
        :param type: тип задачи.
        :return: новый идентификатор.
        '''

        conn = getConnection()

        with conn.cursor() as cursor:
            conn.autocommit = True

            select = "select nextval('tasks_id_seq')"

            cursor.execute(select)
            id = cursor.fetchone()[0]

            insert = 'INSERT INTO tasks (id) VALUES (%s)'
            cursor.execute(insert, (id,))

        conn.close()
        return id

    def addTasksToResalt(self, id_task, id_res):
        '''
        Добавляет связь задачи к результатам вычислений.
        :param id_task: идентификатор задачи.
        :param id_res: идентификатор результатов вычислений.
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            insert = 'INSERT INTO tasks_to_resalt (id_tasks, id_result) VALUES %s'

            values = []
            for item in id_res:
                values.append((id_task, item,))

            execute_values(cur=cursor, sql=insert, argslist=values)
        conn.close()

    def addResults(self, data, id_task=None, percent=0):
        '''
        Добавляет к задаче новые результаты вычислений.
        :param data: результаты вычислений.
        :param id_task: идентификатор задачи.
        :param percent: величина, на которую продвинулось решение заачи.
        '''

        repoWorker = WorkerRepo()

        if id_task == None:
            id_task = self.createTask()


        id_res = self.setResults(data)
        self.addTasksToResalt(id_task, id_res)
        repoWorker.updateCount(id_task, percent)


    def getTask(self, id):
        '''
        Получает результаты вычислений в задаче.
        :param id: идентификатор задачи.
        :return: массив с результатами вычислений.
        '''

        conn = getConnection()

        with conn.cursor() as cursor:
            conn.autocommit = True

            select = '''SELECT r.alfa, r.epselon, r.e, r.bias_estimates, r.n1, r.n2
                        FROM tasks t
                          JOIN tasks_to_resalt ttr on t.id = ttr.id_tasks
                          JOIN result r on ttr.id_result = r.id
                        WHERE t.id = %s'''
            cursor.execute(select, (id,))

            rows = cursor.fetchall()

            line = []
            for row in rows:
                line.append(row)

        conn.close()
        return line

    def getTaskByBestBiasEstimates(self, id):
        '''
        Получает результаты вычислений в задаче.
        :param id: идентификатор задачи.
        :return: массив с результатами вычислений.
        '''

        conn = getConnection()

        with conn.cursor() as cursor:
            conn.autocommit = True

            select = '''SELECT r.alfa, r.epselon, r.e, r.bias_estimates, r.n1, r.n2
                        FROM tasks t
                          JOIN tasks_to_resalt ttr on t.id = ttr.id_tasks
                          JOIN result r on ttr.id_result = r.id
                        WHERE t.id = %s
                        ORDER BY r.bias_estimates
                        LIMIT 50'''
            cursor.execute(select, (id,))

            rows = cursor.fetchall()

            line = []
            for row in rows:
                line.append(row)

        conn.close()
        return line


class WorkerRepo:
    '''
    Репозитория для работы с данными работника.
    Работник имеет следующие статусы:
        # build - формирование задачи.
        # in_progress - задача в процессе выполнения.
        # done - задача выполнена.
        # wait - задача стоит в очереди на выполнение.
    '''

    def getNewIndex(self):
        '''
        Получает новый идентификатор.
        :return: новый идентификатор.
        '''

        conn = getConnection()

        with conn.cursor() as cursor:
            conn.autocommit = True

            select = "select nextval('worker_id_seq')"

            cursor.execute(select)

            id = cursor.fetchone()[0]

        conn.close()
        return id

    def createNewWorker(self, userId):
        '''
        Создаёт нового работника.
        :param userId: идентификатор пользователя.
        :param name: имя нового работника.
        :return: идентификатор работника.
        '''

        id = self.getNewIndex()

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            insert = 'INSERT INTO worker (id, status, user_id, count) VALUES (%s, %s, %s, %s)'

            values = (id, 'build', userId, 0)

            cursor.execute(insert, values)

        conn.close()
        return id

    def buildWorker(self, id, name, taskId):
        '''
        Строит работника, задаёт имя задачи. Привязывает задачу к работнику.
        :param id: идентификатор работника.
        :param name: имя задачи.
        :param taskId: идентификатор задачи.
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            update = 'UPDATE worker SET name = %s, task_id = %s WHERE id = %s'

            values = (name, taskId, id,)

            cursor.execute(update, values)
        conn.close()

    def runWorker(self, id):
        '''
        Запуск работника. В случае успешного запуска метод возвращает True.
        :param id: идентификатор работника.
        :return: True, если удалось запустить работника.
                 False, если стоит блокировка на запуск работника.
        '''

        repoBloker = BlockerRepo()

        if repoBloker.isAllowedRunNewWorker():
            conn = getConnection()
            with conn.cursor() as cursor:
                conn.autocommit = True

                dateTime = datetime.datetime.now()
                update = "UPDATE worker SET status = 'in_progress', count = 0, time_start = %s WHERE id = %s"

                values = (dateTime, id,)
                cursor.execute(update, values)
                repoBloker.addRunWorker()

            conn.close()
            return True
        else:
            return False

    def updateCount(self, taskId, count):
        '''
        Обновляет прогресс выполнения работника.
        :param taskId: идентификатор задачи.
        :param count: величина, на которую прогресс увеличился.
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            select = 'SELECT count FROM worker WHERE task_id = %s'
            cursor.execute(select, (taskId,))
            count_db = cursor.fetchone()[0]

            update = 'UPDATE worker SET count = %s WHERE task_id = %s'

            values = (count_db + count, taskId)

            cursor.execute(update, values)
        conn.close()

    def complete(self, taskId):
        '''
        Помечает, что работник завершил работу. Снимает блокировку на
        1 работника.
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            select = 'SELECT id FROM worker WHERE task_id = %s'
            cursor.execute(select, (taskId,))
            id = cursor.fetchone()[0]

            dateTime = datetime.datetime.now()
            update = 'UPDATE worker SET count = %s, status = %s, time_end = %s WHERE id = %s'

            values = (100, 'done', dateTime, id,)

            cursor.execute(update, values)

        repo = BlockerRepo()
        repo.delRunWorker()
        conn.close()

    def getTaskInLastWorkerByUser(self, userId):
        '''
        Получает идентификатор задачи для последнего работника пользователя.
        :param userId: идентификатор пользователя.
        :return: идентификатор задачи.
        '''

        id = None
        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            select = "SELECT task_id FROM worker WHERE user_id = %s ORDER BY id DESC LIMIT 1"
            cursor.execute(select, (userId,))
            id = cursor.fetchone()[0]

        conn.close()
        return id

    def isDone(self, taskId):
        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            select = "SELECT status, count FROM worker WHERE task_id = %s"
            cursor.execute(select, (taskId,))
            status, count = cursor.fetchone()

            conn.close()
            return [status, float(count)]

    def isRun(self, workerId):
        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            select = "SELECT status FROM worker WHERE id = %s"
            cursor.execute(select, (workerId,))

            var = cursor.fetchone()[0] in ('in_progress', 'done')
            conn.close()
            return var

class BlockerRepo:
    '''
    Репозиторий для работы с блокировщиком фоновых задач.
    '''

    def isAllowedRunNewWorker(self):
        '''
        Проверяет возможность запустить работника.
        :return: True, если можно запустить,
                 False, если нельзя.
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            select = 'SELECT 1 FROM blocker WHERE id = 0 AND limit_worker > run_worker'

            cursor.execute(select)
            answer = cursor.fetchone()
            conn.close()

            if answer:
                return True
            else:
                return False

    def addRunWorker(self):
        '''
        Добавляет запущенного работника.
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            select = 'SELECT run_worker FROM blocker WHERE id = 0'
            cursor.execute(select)
            run_worker = cursor.fetchone()[0]

            update = 'UPDATE  blocker SET run_worker = %s WHERE id = 0'

            value = (run_worker + 1,)
            cursor.execute(update, value)
            conn.close()

    def delRunWorker(self):
        '''
        Удаляет запущенного рабоника.
        '''

        conn = getConnection()
        with conn.cursor() as cursor:
            conn.autocommit = True

            select = 'SELECT run_worker FROM blocker WHERE id = 0'
            cursor.execute(select)
            run_worker = cursor.fetchone()[0]

            update = 'UPDATE  blocker SET run_worker = %s WHERE id = 0'

            value = (run_worker - 1,)
            cursor.execute(update, value)
            conn.close()
