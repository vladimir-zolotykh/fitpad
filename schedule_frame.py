#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from itertools import groupby
from operator import itemgetter
import tkinter as tk
from tkinter import ttk
from sqlalchemy import select
from sqlalchemy.engine.base import Engine
import models as md
import database as db

data = (
    {"date": "2024-09-01", "exercise": "Squat", "weight": 100, "reps": 5},
    {"date": "2024-09-02", "exercise": "Bench Press", "weight": 80, "reps": 8},
    {"date": "2024-09-03", "exercise": "Deadlift", "weight": 120, "reps": 4},
    {"date": "2024-09-03", "exercise": "Deadlift", "weight": 110, "reps": 5}
)


class ScheduleFrame(tk.Frame):
    def __init__(self, parent, engine: Engine):
        super().__init__(parent)
        self.engine = engine
        tree = ttk.Treeview(self, columns=('exercise', 'weight', 'reps'))
        tree.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        tree.heading("#0", text="Date")
        tree.heading("exercise", text="exercise")
        tree.heading("weight", text="Weight (kg)")
        tree.heading("reps", text="Reps")
        tree.column("#0", width=100)
        tree.column("exercise", width=150)
        tree.column("weight", width=100)
        tree.column("reps", width=100)

        with db.session_scope(self.engine) as session:
            schedule: md.Schedule
            for schedule in session.scalars(select(md.Schedule)):
                sch = tree.insert('', 'end', text=schedule.name)
                for wo in schedule.workouts:
                    tree.insert(
                        sch, 'end', text='',
                        values=(wo.exercise.name, wo.weight, wo.reps))


        #         schedule_names.append(schedule.name)
        
        # for date, exercises in groupby(data, key=itemgetter('date')):
        #     parent = tree.insert("", "end", text=date)
        #     for exer in exercises:
        #         tree.insert(
        #             parent, 'end', text='',
        #             values=(itemgetter('exercise', 'weight', 'reps')(exer)))
