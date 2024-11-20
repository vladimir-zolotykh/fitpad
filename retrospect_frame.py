#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict
from sqlalchemy import select
from sqlalchemy.engine.base import Engine
import tkinter as tk
from tkinter import ttk
import models as md
import database as db
from scrolledtreeview import ScrolledTreeview
# exercise, when, weight, reps
col_config = (('#0', 100, md.rel_names[0]),
              *(zip(md.col_names[1:4], (100, 100, 100))))


class RetrospectView(ScrolledTreeview):
    def __init__(self, parent: tk.Frame, engine: Engine, **kw):
        self.engine = engine
        super().__init__(parent, **kw)
        self.refresh_view()

    def refresh_view(self):
        self.delete(*self.get_children())
        exer_date: defaultdict[str, md.Workout] = defaultdict(list)
        with db.session_scope(self.engine) as session:
            query = select(md.Workout)
            for wo in session.scalars(query):
                exer_date[wo.exercise.name].append(wo)
            for exer_name, workouts in exer_date.items():
                exer_node = self.insert('', 'end', text=exer_name)
                for wo in workouts:
                    self.insert(exer_node, 'end',
                                values=(wo.when, wo.weight, wo.reps))


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
