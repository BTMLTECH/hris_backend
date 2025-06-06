#!/usr/bin/env python3
# File: app/util/class_object.py
# Author: Oluwatobiloba Light
"""Class Object"""


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance
