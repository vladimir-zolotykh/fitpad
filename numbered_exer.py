#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from entry_var import EntryVar
from frame2d import Frame2DExer
from exertk import ExerTk


class NumberedExer(list):
    """class to `unpack' the grid structure

    The grid structure represents has two widgets: tk.Entry
    (`exer_no') and Frame2D(ExerTk) and is made in
    NumberedFrame. NumberedExer.__getattr__ is used to
    grid_forget/[re-]grid_pack
    """

    def __init__(self, frame: Frame2DExer):
        num_cols, num_rows = frame.grid_size()
        assert num_rows == 1
        self.frame = frame      # '.workout_frame.exer_wrap_frame00'
        super().__init__(frame[0, col] for col in range(num_cols))

    def __getattr__(self, name):
        return getattr(self.frame, name)

    def exer_name(self) -> str:
        frame2d: Frame2DExer = self[1]
        exertk_frame: ExerTk = frame2d[0, 0]
        label: tk.Label = exertk_frame[0, 0]
        return label.cget('text')

    def exer_no(self) -> int:
        if isinstance(self[0], EntryVar):
            return int(self[0].get())
        else:
            raise TypeError(f'Expected EntryVar, got {type(self[0])}')

    def print_size(self):
        # num_cols = 2, num_rows = 1
        num_cols, num_rows = self.grid_size()
        print(f'NumberedExer.print_size {num_cols = }, {num_rows = }')
