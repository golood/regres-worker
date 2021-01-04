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


def format_numbers(values):
    """
    Форматирует массив чисел к вещественным числам с двумя знаками после запятой.
    :param values: массив чисел.
    :return: массив вещественных чисел.
    """
    return list(map(lambda x: float('{:.2f}'.format(float(x))), values))


def format_number(value):
    """
    Форматирует число к вещественному числу с точностью до двух знаков.
    :param value: число.
    :return: вещественное число.
    """

    if value == 'Infinity':
        return value
    return float('{:.2f}'.format(float(value)))


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

    return list(map(lambda x: x+1, array))
