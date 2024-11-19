#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from sqlalchemy.engine.base import Engine
import tkinter as tk
from tkinter import ttk
import models as md
from scrolledtreeview import ScrolledTreeview
# exercise, when, weight, reps
col_config = (('#0', 100, md.rel_names[0]),
              *(zip(md.col_names[1:4], (100, 100, 100))))


class RetrospectView(ScrolledTreeview):
    def __init__(self, parent: tk.Frame, engine: Engine, **kw):
        self.engine = engine
        super().__init__(parent, **kw)


class RetrospectFrame(tk.Frame):
    def __init__(self, parent: ttk.Notebook, engine: Engine):
        super().__init__(parent)
        self.engine = engine
        self.tree = tree = RetrospectView(
            self, engine, columns=(md.col_names[1], *md.col_names[2:4]))
        tree.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        for cid_width_text in col_config:
            cid = text = cid_width_text[0]
            width: int = int(cid_width_text[1])
            if 2 < len(cid_width_text):
                text = cid_width_text[2]
            tree.heading(cid, text=str(text))
            tree.column(cid, minwidth=width, width=width)
