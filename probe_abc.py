#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Tuple
from abc import ABC, abstractmethod


class Frame2D(ABC):
    @abstractmethod
    def arrange(self) -> Tuple[int, int]:
        return (0, 0)


class Frame2DExer(Frame2D):
    def arrange(self) -> Tuple[int, int]:
        return (1, 2)


class Frame2DSet(Frame2D):
    def arrange(self) -> Tuple[int, int]:
        return (3, 4)


if __name__ == '__main__':
    exer = Frame2DExer()
    _set = Frame2DSet()
    print(exer.arrange())
    print(_set.arrange())
