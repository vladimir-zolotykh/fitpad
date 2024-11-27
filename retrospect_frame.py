#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict
from datetime import datetime
import re
from sqlalchemy import select
from sqlalchemy.engine.base import Engine
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel  # noqa
import models as md
import database as db
from scrolledtreeview import ScrolledTreeview
# exercise, when, weight, reps
col_config = (('#0', 100, md.rel_names[0]),
              *(zip(md.col_names[1:4], (100, 100, 100))))


class RetrospectView(ScrolledTreeview):
    def __init__(self, parent: tk.Frame, engine: Engine, **kw):
        self.engine = engine
        self.retrospect_frame: RetrospectFrame = parent
        super().__init__(parent, **kw)
        self.refresh_view()
        self.bind('<<TreeviewSelect>>', self.on_select)

    def on_select(self, event: tk.Event):
        def get_schedule_name(str: str) -> str:
            m = re.match(r'^[+-]?-[\d]+d <(?P<name>[\w\s\d]+)>$', str)
            if m:
                return m.group('name')

        iid: tuple[str, ...] = self.selection()
        if iid:
            values = self.item(iid, 'values')
            if values and values[0]:
                schedule_name = get_schedule_name(values[0])
                self.retrospect_frame.schedule_var.set(schedule_name)

    def refresh_view(self):
        self.delete(*self.get_children())
        name_wo: defaultdict[str, list[md.Workout]] = defaultdict(list)
        date_wo: defaultdict[datetime, list[md.Workout]] = defaultdict(list)
        with db.session_scope(self.engine) as session:
            query = select(md.Workout)
            for wo in session.scalars(query):
                name_wo[wo.exercise.name].append(wo)
            for exer_name, workouts in name_wo.items():
                exer_node = self.insert('', 'end', text=exer_name)
                date_wo.clear()
                for wo in workouts:
                    dt = datetime.strptime(wo.date(), '%Y-%m-%d')
                    date_wo[dt].append(wo)
                for date, workouts in date_wo.items():
                    date_node = self.insert(
                        exer_node, 'end', values=(wo.date(True), ))
                    _workouts = sorted(workouts, key=lambda wo: wo.weight,
                                       reverse=True)
                    w0 = _workouts[0]
                    self.insert(date_node, 'end',
                                values=('', w0.weight, w0.reps))


class RetrospectFrame(tk.Frame):
    def __init__(self, parent: ttk.Notebook, engine: Engine):
        super().__init__(parent)
        self.engine = engine
        self.schedule_var = tk.StringVar()
        self.schedule_var.set('')
        toolbar = tk.Frame(self)
        toolbar.grid(column=0, row=0, sticky=tk.NSEW)
        schedule_ent = tk.Entry(toolbar, width=50,
                                textvariable=self.schedule_var)
        schedule_ent.grid(column=0, row=0)
        go_btn = tk.Button(toolbar, text='Go', command=self.go_schedule)
        go_btn.grid(column=1, row=0)
        self.tree = tree = RetrospectView(
            self, engine, columns=(md.col_names[1], *md.col_names[2:4]))
        tree.grid(column=0, row=1, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        for cid_width_text in col_config:
            cid = text = cid_width_text[0]
            width: int = int(cid_width_text[1])
            if 2 < len(cid_width_text):
                text = cid_width_text[2]
            tree.heading(cid, text=str(text))
            tree.column(cid, minwidth=width, width=width)

    def go_schedule(self):
        schedule_name: str = self.schedule_var.get()
        # Go to the schedule tab, expand the tree below the
        # `schedule_name' node.
        print(f'{schedule_name = }')
