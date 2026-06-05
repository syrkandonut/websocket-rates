import random

from enum import StrEnum


class PathParam(StrEnum):
    CURRENCY = 'currency'


FIRST_NAME = ['Cool', 'Lazy', 'Smart', 'Rich', 'Epic', 'Super', 'Kind', 'Elegant']
LAST_NAME = ['Donut', 'Capy', 'Panda', 'Axolotl', 'Fox', 'Spider', 'Wolf', 'Parrot']


def get_random_name():
    return f'{random.choice(FIRST_NAME)} {random.choice(LAST_NAME)}'
