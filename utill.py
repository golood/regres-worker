#!/usr/bin/python3
import hashlib


def get_value_checkbox(value):
    """
    Проверяет состояние checkbox и отдает результат в булевом значении.
    :param value: состояние checkbox
    :return: состояние checkbox
    """
    if value == 'on':
        return True

    return False


def format_numbers(values, flag=False):
    """
    Форматирует массив чисел к вещественным числам с двумя знаками после запятой.
    :param values: массив чисел.
    :param flag
    :return: массив вещественных чисел.
    """

    return list(map(lambda x: format_number(float(x), validator=find_min_float, flag=flag), values))


def format_number(value, precision=2, validator=None, flag=False):
    """
    Форматирует число к вещественному числу с точностью до двух знаков.
    :param value: число.
    :param precision: точность окрушления.
    :param validator:
    :param flag
    :return: вещественное число.
    """

    if value == 'Infinity':
        return value

    if validator is not None:
        precision = validator([value], flag=flag)

    return float('{:.{}f}'.format(float(value), precision))


def format_to_int(values):
    """
    Форматирует массив строк к целым числам.
    :param values: массив строк.
    :return: массив целых чисел.
    """

    return list(map(lambda x: int(float(x)), values))


def append_one_for_number(array):
    """
    Прибавляет единицу ко всем элементам массива.

    :param array: массив целых чисел.
    :return: массив чисел.
    """

    return list(map(lambda x: x + 1, array))


def find_min_float(*args, flag=False):
    """
    Поиск минимального вещественного числа.
    :return количество знаков после запятой.
    """

    count = 2
    min_value = min(min(args))

    if min_value == 0:
        return count

    if min_value < 0:
        min_value *= -1

    while min_value < 1 * pow(10, count * -1):
        count += 1

    if flag and min_value >= 1:
        return 10

    if count == 2:
        return count

    return count + 8
