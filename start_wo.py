#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Dict, Any
from functools import partial
import argparse
import argcomplete
import tkinter as tk
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Exercise
import database as db
from exertk import ExerDir


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
        self.exer_dir: Dict[str, Any] = {}
        with Session(engine) as session:
            for exer in session.scalars(select(Exercise)):
                self.exer_dir[exer.name] = None
        frame = tk.Frame(self)
        frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        self.dir = dir = ExerDir(frame)
        for name in self.exer_dir:
            _add_exer = partial(dir.add_exer, name)
            add_exer_menu.add_command(label=name, command=_add_exer)
        menubar.add_command(label='Save workout', command=self.save_workout)

    def save_workout(self):
        # for exer_name in self.dir.yield_exer_names():
        #     print(f'{exer_name = }')
        for name in self.dir:
            print(f'{name = }')
            exertk = self.dir[name]
            for set_no, weight, reps in exertk.yield_sets():
                print(f'{set_no = }, {weight = }, {reps = }')


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
