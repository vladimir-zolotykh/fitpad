#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from itertools import groupby
from datetime import datetime
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
        tree = ttk.Treeview(
            self, columns=(col_names[1], rel_names[0], *col_names[2:4]))
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

                def _wo_date(wo):
                    return datetime.strptime(wo.when, '%Y-%m-%d %H:%M:%S')

                for when, wo_group in groupby(
                        sorted(schedule.workouts, key=_wo_date),
                        key=_wo_date):
                    date_node = tree.insert(
                        sch, 'end', text='', values=(when, ))

                    def _wo_exer_name(wo):
                        return wo.exercise.name

                    for exer_name, wo_group in groupby(
                            sorted(wo_group, key=_wo_exer_name),
                            key=_wo_exer_name):
                        exer_node = tree.insert(
                            date_node, 'end', text='',
                            values=('', exer_name))
                        for wo in wo_group:
                            tree.insert(
                                exer_node, 'end', text='',
                                values=('', '', wo.weight, wo.reps))
