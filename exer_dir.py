#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Dict
import tkinter as tk
from exertk import ExerTk
from frame2d import Frame2D
from numbered_frame import NumberedFrame
from wo_tools import Wo, NumberedExer


class ExerDir(Dict[str, ExerTk]):
    """A dict of Workout exercises

    Dict[str, ExerTk]
    """

    def __init__(self, frame: Frame2D):
        super().__init__()
        self.frame: Frame2D = frame
        self.row: int = 0

    def del_exer(self, name: str):
        del self[name]
        self.row -= 1

    def edit_exer(self):
        wo: Wo = Wo(self.frame)
        exer: NumberedExer
        for exer in wo:
            # exer.print_size()
            if 0 < exer.exer_no():
                exer.grid_forget()
        row: int = 0
        for exer in wo:
            if exer.exer_no() == 0:
                self.del_exer(exer.exer_name())
                exer.destroy()
            else:
                exer.grid(column=0, row=row, sticky=tk.EW)
                row += 1

    def add_exer(self, name: str):
        numbered_frame = NumberedFrame(self.frame, self.row)
        self[name] = ExerTk(numbered_frame.exer_box, name, 0)
        self.row += 1
