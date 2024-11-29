#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Optional, cast
from datetime import datetime
from collections import defaultdict
import tkinter as tk
from tkinter import ttk
# from tkinter.simpledialog import askstring
from sqlalchemy import select
from sqlalchemy.engine.base import Engine
import models as md
import database as db
from schedule_dialog import ScheduleDialog
from setframe import SetFrame
from mutableview import ScheduleView
import exerframe as EF
from retrospect_frame import ensure_type
import defaultdlg

# col_names = ['id', 'when', 'weight', 'reps']
col_names: list[str] = [col.name for col in md.Workout.__table__.columns]
# rel_names = ['exercise', 'schedule']
rel_names: list[str] = [rel.key for rel in md.Workout.__mapper__.relationships]
col_config = (('#0', 100, rel_names[1]), (rel_names[0], 150),
              *(zip(col_names[1:4], (100, 100, 100))))


def notebooktabto_widget(
        nb: ttk.Notebook, tab_name: str
) -> Optional[tk.Frame]:
    # ('.!notebook.!exerframe', '.!notebook.!scheduleframe',
    #  '.!notebook.!repertoireframe')
    # ['Workout', 'Schedule', 'Repertoire']
    # [ ExerFrame, ScheduleFrame, RepertoireFrame]
    for index, widget_name in enumerate(nb.tabs()):
        tab: str = nb.tab(index, 'text')
        if tab == tab_name:
            return nb.nametowidget(widget_name)
    return None


def get_notebooktabid(nb: ttk.Notebook, tab_name: str) -> Optional[int]:
    for index, _ in enumerate(nb.tabs()):
        tab: str = nb.tab(index, 'text')
        if tab == tab_name:
            return index
    return None


class ScheduleFrame(tk.Frame):
    def __init__(self, parent: ttk.Notebook, engine: Engine):
        super().__init__(parent)
        self.engine = engine
        self.exer_frame: EF.ExerFrame = ensure_type(
            notebooktabto_widget(parent, 'Workout'), EF.ExerFrame)
        self.tree = tree = ScheduleView(
            self, engine, self.update_view,
            columns=(col_names[1], rel_names[0], *col_names[2:4]))
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
        self.update_view()

    def modify_menu(self, parent: tk.Menu) -> tk.Menu:
        """Add ScheduleFrame specific menu items

        return the submenu
        """

        parent.add_command(label='Delete', command=self.tree.delete_item)
        parent.add_command(label='Rename', command=self.tree.rename_item)
        return parent

    def _expand_item(self, iid: str) -> None:
        self.tree.see(iid)
        self.tree.item(iid, open=True)
        for child in self.tree.get_children(iid):
            self._expand_item(child)

    def expand(self, schedule_name: str):
        '''Expand the tree below the `schedule_name' node'''
        for iid in self.tree.get_children():
            name = self.tree.item(iid, 'text')
            if name == schedule_name:
                self._expand_item(iid)
                break

    def update_view(self):
        with db.session_scope(self.engine) as session:
            self._make_view(self.tree, session.scalars(select(md.Schedule)))

    def _make_view(
            self,
            tree: ttk.Treeview,
            schedules: list[md.Schedule]
    ) -> None:
        """
        Make collapsible/expandable ttk.Treeview
        """
        schedule: md.Schedule
        tree.delete(*tree.get_children())
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

    def load_schedule(self):
        schedule_names: list[str] = []
        with db.session_scope(self.engine) as session:
            schedule: md.Schedule
            for schedule in session.scalars(select(md.Schedule)):
                schedule_names.append(schedule.name)

        dialog = ScheduleDialog(self, title="Select schedule",
                                values=schedule_names)
        schedule_name: str = dialog.schedule_name
        if not schedule_name:
            return
        query = (select(md.Schedule)
                 .where(md.Schedule.name == schedule_name))
        with db.session_scope(self.engine) as session:
            schedule = session.scalar(query)
            workouts_by_exer_name = defaultdict(list)
            for wo in schedule.workouts:
                workouts_by_exer_name[wo.exercise.name].append(wo)

            for exer_name, workouts in workouts_by_exer_name.items():
                set_frame = self.exer_frame.add_exer(exer_name,
                                                     init_exer=False)
                for wo in workouts:
                    set_frame.add_set(wo)

    def save_schedule(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        schedule_name: str = defaultdlg.askstring(
            __name__, 'Schedule name',
            parent=self, default=f'Schedule_{now}')
        if not schedule_name:
            return
        with db.session_scope(self.engine) as session:
            def get_exercise(exer_name):
                return session.scalar(select(md.Exercise)
                                      .where(md.Exercise.name == exer_name))

            exer_no: str
            set_frame: SetFrame
            schedule: md.Schedule = md.Schedule(name=schedule_name)
            session.add(schedule)
            for exer_no, set_frame in self.exer_frame:
                # exer = session.get_exer(set_frame.exer_name)
                exer = get_exercise(set_frame.exer_name)
                for weight, reps in set_frame:
                    wo = md.Workout(exercise=exer, when=now, weight=weight,
                                    reps=reps)
                    session.add(wo)
                    schedule.workouts.append(wo)
            session.commit()
            # self.show_log(schedule)
