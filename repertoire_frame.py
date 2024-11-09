#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import re
from operator import itemgetter
from typing import Callable, Optional
import tkinter as tk
from tkinter import simpledialog
from tkinter.messagebox import askokcancel
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import SQLAlchemyError  # noqa
import models as md
import database as db
from defaultdlg import askstring
from scrolledtreeview import ScrolledTreeview


class RepertoireFrame(tk.Frame):
    columns = (('exercise', 150), )

    def __init__(
            self, parent, engine: Engine,
            update_workout_menu: Callable[[Optional[tk.Menu]], None]
    ):
        self.engine = engine
        self.update_workout_menu = update_workout_menu
        super().__init__(parent)
        self.tree = ScrolledTreeview(
            self, show='headings',
            columns=[itemgetter(0)(t) for t in self.columns])
        for n, w in self.columns:
            self.tree.heading(n, text=n)
            self.tree.column(n, minwidth=w, width=w)
        self.tree.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.update_repertoire()

    @property
    def db_exer(self):
        exer_book: dict[str, int] = {}
        with db.session_scope(self.engine) as session:
            for exer in session.scalars(select(md.Exercise)):
                exer_book[exer.name] = exer.id
        return exer_book

    def update_repertoire(self):
        self.tree.delete(*self.tree.get_children())
        for exer_name, id in self.db_exer.items():
            self.tree.insert(
                '', tk.END, values=(f'{exer_name} ({id})', ))

    def add_exercise_name(self):
        exer_name = simpledialog.askstring(
            'Extend repertoire', 'Enter exercise name', parent=self)
        if exer_name:
            with db.session_scope(self.engine) as session:
                exer = md.Exercise(name=exer_name)
                session.add(exer)
                session.commit()
            self.update_exercise_list_gui()

    def update_exercise_list_gui(self):
        query = db.select(md.Exercise)
        with db.session_scope(self.engine) as session:
            self.tree.delete(*self.tree.get_children())
            for exer in session.scalars(query):
                self.tree.insert('', tk.END,
                                 values=(f'{exer.name} ({exer.id})', ))
        self.update_workout_menu(None)

    def _get_selected_exer_name(self) -> str:
        def remove_id(s: str) -> str:
            m = re.match(r'^.*(?P<id> \(\d+\))$', s)
            return s[:m.start(1)] if m else s

        iid = self.tree.selection()[0]
        values = self.tree.item(iid, 'values')
        exer_name = remove_id(values[0])
        return exer_name

    def _modify_exercise(
            self, modify_func: Callable[[Session, md.Exercise], None]
    ) -> None:
        exer_name: str = self._get_selected_exer_name()
        with db.session_scope(self.engine) as session:
            exer = session.query(md.Exercise).filter_by(name=exer_name).first()
            if exer:
                modify_func(session, exer)
                session.commit()
                self.update_exercise_list_gui()

    def delete_exercise(self):
        def delete_action(session: Session, exer: md.Exercise) -> None:
            if askokcancel(__name__, f'Delete exercise "{exer.name}" ?',
                           parent=self):
                session.delete(exer)
        self._modify_exercise(delete_action)

    def rename_exercise(self):
        def rename_action(session: Session, exer: md.Exercise) -> None:
            new_name: str = askstring(__name__, 'Enter exercise name',
                                      parent=self, default=exer.name)
            if new_name:
                exer.name = new_name
                session.add(exer)
        self._modify_exercise(rename_action)
