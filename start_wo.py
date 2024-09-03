#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Dict, Any
from functools import partial
from datetime import datetime
import argparse
import argcomplete
import tkinter as tk
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import models as md
import database as db
from exer_dir import ExerDir
# from frame2d_exer import Frame2DExer
from exerframe import ExerFrame


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
        exer_frame = ExerFrame(self)
        exer_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        for name in self.db_exer:
            _add_exer = partial(exer_frame.add_exer, name)
            add_exer_menu.add_command(label=name, command=_add_exer)
        add_exer_menu.add_separator()
        add_exer_menu.add_command(label='Edit', command=exer_frame.edit_exer)
        menubar.add_command(label='Save workout', command=self.save_workout)

    def save_workout(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with db.session_scope(self.engine) as session:
            for exer_name in self.dir:
                exer = session.get_exer(exer_name)
                exertk = self.dir[exer_name]
                for _, weight, reps in exertk.yield_sets():
                    session.add(md.Workout(exercise=exer, when=now,
                                           weight=weight, reps=reps))
            session.commit()


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
    Workout(engine).mainloop()
