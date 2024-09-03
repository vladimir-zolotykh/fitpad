#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
import frame2d_exer as f2e
from setframe import SetFrame
from entry_var import EntryVar


class ExerFrame(f2e.Frame2DExer):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, *kwargs)
        self.parent = parent
        self.grid_row = 0

    @property
    def exer_order(self):
        return self.grid_row + 1

    def add_exer(self, exer_name: str):
        var = tk.StringVar()
        var.set(str(self.exer_order))  # refactor EntryVar.set()
        exer_no: EntryVar = EntryVar(self, textvariable=var, width=2)
        exer_no.grid(column=0, row=self.grid_row)
        set_frame = SetFrame(self, exer_name)
        set_frame.grid(column=1, row=self.grid_row, sticky=tk.EW)
        self.columnconfigure(1, weight=1)
        self.grid_row += 1

    def edit_exer(self):
        self.arrange()
