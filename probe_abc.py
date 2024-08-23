#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Tuple
from abc import ABC, abstractmethod
import tkinter as tk


class Frame2D(tk.Frame, ABC):
    def __init__(self, _parent):
        super(Frame2D, self).__init__(_parent)
        super(Frame2D, self).grid()

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
    root = tk.Tk()
    exer = Frame2DExer(root)
    _set = Frame2DSet(root)
    print(exer.arrange())
    print(_set.arrange())
