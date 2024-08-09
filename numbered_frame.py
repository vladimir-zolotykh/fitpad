#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
# from typing import Dict, List, Optional, cast
from entry_var import EntryVar


class NumberedFrame(tk.Frame):
    def __init__(self, parent: tk.Frame, row: int):
        super().__init__(parent, name=f'exer_wrap_frame{row:02d}')
        assert not (hasattr(self, 'parent') or hasattr(self, 'row'))
        self.parent = parent
        self.row = row
        self.grid(column=0, row=row, sticky=tk.NSEW)
        self.columnconfigure(1, weight=1)
        # exer_no
        var = tk.StringVar()
        var.set(str(self.row + 1))
        exer_no = EntryVar(self, width=2)
        exer_no.configure(textvariable=var)
        exer_no.grid(column=0, row=0)
        # self._exer_box
        self._exer_box = tk.Frame(self, name=f'exer_box_frame{row:02d}')
        self._exer_box.columnconfigure(0, weight=1)
        self._exer_box.grid(column=1, row=0, sticky=tk.EW)

    @property
    def exer_box(self):
        return self._exer_box
