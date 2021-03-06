import utill
from Models import TaskDTO


def get_result(objects):
    results = []

    for task in objects:
        results.append(task.get_results())

    return results


def start_solution(data):
    tasks = []

    for item in data['list_h']:
        tasks.append(TaskDTO(
            {
                'x': data['x'],
                'y': data['y'],
                'h1': item['h1'],
                'h2': item['h2'],
                'freeChlen': data['freeChlen']
            }))
    del data

    for task in tasks:
        task.run()

    res = get_result(tasks)

    del tasks

    result = []
    for item in res:
        result.append([
            utill.format_numbers(item[0][1][0]),
            utill.format_numbers(item[0][1][1]),
            utill.format_number(item[0][1][2], precision=5),
            utill.format_number(item[1], precision=5),
            utill.append_one_for_number(item[2]),
            utill.append_one_for_number(item[3])
        ])

    del res

    return result
