#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Dict, Any, Tuple
from functools import partial
from operator import itemgetter
from datetime import datetime
import argparse
import argcomplete
import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine.base import Engine
import models as md
import database as db
# from frame2d_exer import Frame2DExer
from exerframe import ExerFrame
from setframe import SetFrame


class Workout(tk.Tk):
    def __init__(self, engine, *args, **kwargs):
        super(Workout, self).__init__(*args, **kwargs)
        self.engine = engine
        self.title('Workout')
        self.geometry('500x200+400+300')
        menubar = tk.Menu(self, tearoff=0)
        self['menu'] = menubar
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Quit', command=self.quit)
        menubar.add_cascade(label='File', menu=file_menu)
        add_exer_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Add exercise', menu=add_exer_menu)
        self.db_exer: Dict[str, Any] = {}
        with Session(engine) as session:
            for exer in session.scalars(select(md.Exercise)):
                self.db_exer[exer.name] = None
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.exer_frame = ExerFrame(self.notebook)
        self.exer_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.notebook.add(self.exer_frame, text='Workout')
        self.log_frame = tk.Frame(self.notebook)
        self.log_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.notebook.add(self.log_frame, text='Log')
        self.repertoire_frame = tk.Frame(self.notebook)
        self.repertoire_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.notebook.add(self.repertoire_frame, text='Repertoire')
        self.show_repertoire()
        for name in self.db_exer:
            _add_exer = partial(self.exer_frame.add_exer, name)
            add_exer_menu.add_command(label=name, command=_add_exer)
        add_exer_menu.add_separator()
        add_exer_menu.add_command(label='Edit',
                                  command=self.exer_frame.edit_exer)
        menubar.add_command(label='Save workout', command=self.save_workout)

    def show_repertoire(self):
        columns = (('exercise', 150), )
        table = ttk.Treeview(self.repertoire_frame, show='headings',
                             columns=[itemgetter(0)(t) for t in columns])
        for n, w in columns:
            table.heading(n, text=n)
            table.column(n, width=w)
        for exer_name in self.db_exer:
            table.insert('', tk.END, values=(exer_name, ))
        table.grid(column=0, row=0, sticky=tk.NSEW)
        self.repertoire_frame.columnconfigure(0, weight=1)
        self.repertoire_frame.rowconfigure(0, weight=1)

    def show_log(self):
        """Show completed workout"""

        columns = (('exercise', 150), ('when', 150),
                   ('weight', 100), ('reps', 100))
        table = ttk.Treeview(
            self.log_frame, show="headings",
            columns=[itemgetter(0)(t) for t in columns])
        for n, w in columns:
            table.heading(n, text=n)
            table.column(n, width=w)
        with db.session_scope(self.engine) as session:
            for wo in session.scalars(select(md.Workout)):
                table.insert("", tk.END, values=(wo.exercise.name, wo.when,
                                                 wo.weight, wo.reps))
        table.grid(column=0, row=0, sticky=tk.NSEW)
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)

    def save_workout(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with db.session_scope(self.engine) as session:
            exer_no: str
            set_frame: SetFrame
            for exer_no, set_frame in self.exer_frame:
                exer = session.get_exer(set_frame.exer_name)
                for _, weight, reps in set_frame:
                    wo = md.Workout(exercise=exer, when=now, weight=weight,
                                    reps=reps)
                    session.add(wo)
            session.commit()
        self.show_log()


def create_exercises(engine: Engine):
    """Create exercises once"""

    try:
        with db.session_scope(engine) as session:
            for exer_name in ['front squat', 'squat', 'bench press',
                              'deadlift']:
                exer = md.Exercise(name=exer_name)
                session.add(exer)
                session.commit()
    except IntegrityError:
        # Exercises already exist
        session.rollback()


parser = argparse.ArgumentParser(
    prog='start_wo.py',
    description='Start workout',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--echo', action='store_true', help='Print emitted SQL commands')
parser.add_argument('--db', default='fitpad.db', help='Database file (.db)')


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    engine = create_engine(f'sqlite:///{args.db}', echo=args.echo)
    db.initialize(engine)
    create_exercises(engine)
    Workout(engine).mainloop()
