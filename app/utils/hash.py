#!/usr/bin/env python3
# File: app/util/hash.py
# Author: Oluwatobiloba Light
"""Hash utility"""

import uuid


def get_rand_hash(length=16):
    """"""
    return uuid.uuid4().hex[:length]