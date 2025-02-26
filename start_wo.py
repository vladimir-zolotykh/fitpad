#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Optional
from functools import partial
from operator import itemgetter
import argparse
import argcomplete
import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine.base import Engine
import models as md
import database as db
from exerframe import ExerFrame
from schedule_frame import ScheduleFrame
# from repertoire_frame import RepertoireFrame
from repertoire_frame import RepertoireFrame
from retrospect_frame import RetrospectFrame


class Workout(tk.Tk):
    def __init__(self, engine, *args, **kwargs):
        super(Workout, self).__init__(*args, **kwargs)
        self.engine: Engine = engine
        self.title('Workout')
        self.geometry('500x200+400+300')
        self.menubar = menubar = tk.Menu(self, tearoff=0)
        self['menu'] = menubar
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Quit', command=self.quit)
        menubar.add_cascade(label='File', menu=file_menu)
        self.workout_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Workout', menu=self.workout_menu)
        self.notebook = ttk.Notebook(self)
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)
        self.notebook.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.exer_frame = ExerFrame(self.notebook, self.engine)
        self.exer_frame.grid(column=0, row=0, sticky=tk.NSEW)
        # <<< Workout >>>
        self.notebook.add(self.exer_frame, text='Workout')
        # <<< Schedule >>>
        self.schedule_frame = ScheduleFrame(self.notebook, self.engine)
        self.notebook.add(self.schedule_frame, text='Schedule')
        # self.schedule_menu = schedule_menu = tk.Menu(
        #     self.workout_menu, tearoff=False)
        menubar.add_cascade(
            label='Schedule',
            menu=self.schedule_frame.modify_menu(
                tk.Menu(self.workout_menu, tearoff=False)))
        # menubar.add_cascade(label='Schedule', menu=self.schedule_menu)
        # <<< Retrospect >>>
        self.retrospect_frame = RetrospectFrame(self.notebook, self.engine)
        self.notebook.add(self.retrospect_frame, text='Retrospect')
        # <<< Log >>>
        self.log_frame = tk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text='Log')
        self.repertoire_table: Optional[ttk.Treeview] = None
        # <<< Repertoire >>>
        self.repertoire_frame = RepertoireFrame(
            self.notebook, self.engine, self.update_workout_menu)
        self.notebook.add(self.repertoire_frame, text='Repertoire')
        self.workout_menu.add_command(
            label='Edit', command=self.exer_frame.edit_exer)
        self.workout_menu.add_separator()
        self.workout_menu.add_command(
            label='Clear', command=self.clear_workout_tab)
        self.workout_menu.add_command(
            label='Save schedule', command=self.schedule_frame.save_schedule)
        self.workout_menu.add_command(
            label='Load schedule', command=self.schedule_frame.load_schedule)
        self.update_workout_menu(self.workout_menu)
        repertoire_menu = tk.Menu(menubar, tearoff=0)
        # Experimental

        def let(cmd, obj):
            cmd(label='Add', command=obj.add_exercise_name)
            # cmd(label='Rename', command=obj.rename_exercise)
            cmd(label='Rename', command=obj.tree.rename_item)
            cmd(label='Update', command=obj.update_exercise_list_gui)
            # cmd(label='Delete', command=obj.delete_exercise)
            cmd(label='Delete', command=obj.tree.delete_item)
        let(repertoire_menu.add_command, self.repertoire_frame)
        menubar.add_cascade(label='Repertoire', menu=repertoire_menu)

    def clear_workout_tab(self):
        if self.exer_frame:
            self.exer_frame.delete_grids()

    def update_workout_menu(self, menu: Optional[tk.Menu] = None) -> None:
        """Update `Add exercise' submenu of `Workout' menu

        the menu is build anew from md.Exercise table each time
        `update_workout_menu' is called
        """

        def delete_old_submenu(menu: tk.Menu) -> None:
            """Delete `Add exercise` submenu if exists"""

            index_end: Optional[int] = menu.index(tk.END)
            if isinstance(index_end, int):
                for i in range(index_end + 1):
                    try:
                        t: str = menu.entrycget(i, "label")
                    except tk.TclError:
                        continue  # separator has no label
                    if t == 'Add exercise':
                        menu.delete(i)

        if menu is None:
            menu = self.workout_menu
        delete_old_submenu(menu)
        exer_list_menu = tk.Menu(self.workout_menu, tearoff=0)
        self.workout_menu.add_cascade(
            label='Add exercise', menu=exer_list_menu)
        # for exer_name in self.db_exer:
        for exer_name in self.repertoire_frame.db_exer:
            _add_exer = partial(self.exer_frame.add_exer, exer_name)
            exer_list_menu.add_command(label=exer_name, command=_add_exer)

    def on_tab_change(self, event):
        """
        Synchronize menus and notebook tabs

        Handles the synchronization between the 'Workout' and
        'Repertoire' menus and their corresponding notebook tabs.

        Only one menu is active at a time:
        - The 'Workout' menu is active when the 'Workout' tab is
          selected.
        - The 'Repertoire' menu is active when the 'Repertoire' tab is
          selected.
        """

        # Assuming nb tabs and menu labels named the same, e.g.,
        # 'Workout', 'Schedule', 'Repertoire'
        NB_TABS: list[str] = ['Workout', 'Schedule', 'Repertoire']
        win_to_tab: dict[str, str] = {}  # window name -> tab name
        for index, t in enumerate(self.notebook.tabs()):
            tab_name = self.notebook.tab(index, 'text')
            # e.g. win_to_tab['.!notebook.!frame'] = 'Log'
            win_to_tab[t] = tab_name
        selected_tab_text = win_to_tab[self.notebook.select()]
        label_to_index: dict[str, int] = {}  # menu label -> index
        max_menu_index = self.menubar.index(tk.END)
        if isinstance(max_menu_index, int):
            for index in range(max_menu_index + 1):
                menu_label = self.menubar.entrycget(index, "label")
                label_to_index[menu_label] = index
                if menu_label in NB_TABS:
                    self.menubar.entryconfigure(index, state=tk.DISABLED)
        if selected_tab_text in NB_TABS:
            self.menubar.entryconfigure(label_to_index[selected_tab_text],
                                        state=tk.NORMAL)

    def show_log(self, schedule: md.Schedule) -> None:
        """Show completed workout"""

        columns = (('exercise', 150), ('when', 150),
                   ('weight', 100), ('reps', 100))
        table = ttk.Treeview(
            self.log_frame, show="headings",
            columns=[itemgetter(0)(t) for t in columns])
        for n, w in columns:
            table.heading(n, text=n)
            table.column(n, width=w)
        query = (
            select(md.Workout)
            .join(md.Workout.schedule)
            .where(md.Schedule.name == schedule.name)
        )
        with db.session_scope(self.engine) as session:
            for wo in session.scalars(query):
                table.insert("", tk.END, values=(wo.exercise.name, wo.when,
                                                 wo.weight, wo.reps))
        table.grid(column=0, row=0, sticky=tk.NSEW)
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)


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
