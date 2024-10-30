#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter import ttk
from sqlalchemy import select
from sqlalchemy.engine.base import Engine
import models as md
import database as db
# col_names = ['id', 'when', 'weight', 'reps']
col_names: list[str] = [col.name for col in md.Workout.__table__.columns]
# rel_names = ['exercise', 'schedule']
rel_names: list[str] = [rel.key for rel in md.Workout.__mapper__.relationships]
col_config = (('#0', 100, rel_names[1]), (rel_names[0], 150),
              *(zip(col_names[1:4], (100, 100, 100))))


class ScheduleFrame(tk.Frame):
    def __init__(self, parent, engine: Engine):
        super().__init__(parent)
        self.engine = engine
        tree = ttk.Treeview(self, columns=(rel_names[0], *col_names[1:4]))
        tree.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        for cid_width_text in col_config:
            cid = text = cid_width_text[0]
            width = cid_width_text[1]
            if 2 < len(cid_width_text):
                text = cid_width_text[2]
            tree.heading(cid, text=text)
            tree.column(cid, width=width)
        with db.session_scope(self.engine) as session:
            schedule: md.Schedule
            for schedule in session.scalars(select(md.Schedule)):
                sch = tree.insert('', 'end', text=schedule.name)
                for wo in schedule.workouts:
                    tree.insert(
                        sch, 'end', text='',
                        values=(wo.exercise.name, wo.when, wo.weight, wo.reps))
