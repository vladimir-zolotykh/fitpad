#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict
from datetime import datetime
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
        name_wo: defaultdict[str, list[md.Workout]] = defaultdict(list)
        with db.session_scope(self.engine) as session:
            query = select(md.Workout)
            for wo in session.scalars(query):
                name_wo[wo.exercise.name].append(wo)
            for exer_name, workouts in name_wo.items():
                exer_node = self.insert('', 'end', text=exer_name)
                date_wo: defaultdict[datetime, list[md.Workout]]
                date_wo = defaultdict(list)
                for wo in workouts:
                    dt = datetime.strptime(wo.date(), '%Y-%m-%d')
                    date_wo[dt].append(wo)
                for date, workouts in date_wo.items():
                    date_node = self.insert(exer_node, 'end',
                                            values=(wo.date(True)))
                    _workouts = sorted(workouts, key=lambda wo: wo.weight,
                                       reverse=True)
                    for wo in _workouts:
                        self.insert(date_node, 'end',
                                    values=('', wo.weight, wo.reps))
                        break


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
