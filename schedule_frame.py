#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from datetime import datetime
from collections import defaultdict
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
            tree.heading(cid, text=str(text))
            tree.column(cid, width=int(width))
        with db.session_scope(self.engine) as session:
            self.make_view(tree, session.scalars(select(md.Schedule)))

    def make_view(
            self,
            tree: ttk.Treeview,
            schedules: list[md.Schedule]
    ) -> None:
        """
        Make collapsible/expandable ttk.Treeview
        """
        schedule: md.Schedule
        for schedule in schedules:
            sch_node = tree.insert('', 'end', text=schedule.name)
            when_dict = defaultdict(list)  # workouts by date
            for wo in schedule.workouts:
                when = datetime.strptime(wo.when, '%Y-%m-%d %H:%M:%S')
                when_dict[when].append(wo)
            exer_dict = defaultdict(list)  # workouts by exer. name
            for when in when_dict:
                for wo in when_dict[when]:
                    exer_dict[wo.exercise.name].append(wo)
                when_node = tree.insert(sch_node, 'end', text='',
                                        values=(when, ))
                for exer_name in exer_dict:
                    exer_node = tree.insert(
                        when_node, 'end', text='', values=('', exer_name))
                    for wo in exer_dict[exer_name]:
                        tree.insert(exer_node, 'end', text='',
                                    values=('', '', wo.weight, wo.reps))
