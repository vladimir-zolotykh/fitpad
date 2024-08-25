#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Tuple
from abc import ABC, abstractmethod
import tkinter as tk
from frame2d_exer import Frame2DExer
from frame2d_set import Frame2DSet


class Frame2D(tk.Frame, ABC):
    def __init__(self, _parent):
        super(Frame2D, self).__init__(_parent)
        super(Frame2D, self).grid()

    @abstractmethod
    def arrange(self) -> Tuple[int, int]:
        return (0, 0)


if __name__ == '__main__':
    root = tk.Tk()
    exer = Frame2DExer(root)
    _set = Frame2DSet(root)
    print(exer.arrange())
    print(_set.arrange())
