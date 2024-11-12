#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC
from abc import abstractmethod
from typing import Callable, Union, Optional
import re
from sqlalchemy import Engine
from sqlalchemy.orm import Session
import tkinter as tk
from tkinter.messagebox import askokcancel
import models as md
import database as db
from scrolledtreeview import ScrolledTreeview
import defaultdlg

ExerciseOrSchedule = Union[md.Exercise, md.Schedule]


class MutableView(ScrolledTreeview, ABC):
    def __init__(
            self, parent: tk.Frame, engine: Engine,
            update_view_callback: Callable[[], None], **kw
    ) -> None:
        self.engine = engine
        self.update_view_callback = update_view_callback
        self._selected_text: Optional[str] = None
        super().__init__(parent, **kw)
        self.bind('<<TreeviewSelect>>', self.on_select)

    def on_select(self, event: tk.Event):
        iid: tuple[str, ...] = self.selection()
        if iid:
            self._selected_text = self._get_view_selection(iid[0])

    @abstractmethod
    def _get_view_selection(self, iid: str) -> Optional[str]:
        return None

    @abstractmethod
    def _get_item_name(self, iid: str) -> str:
        pass

    @abstractmethod
    def _get_item(
            self, session: Session, item_name: str
    ) -> Optional[Union[md.Exercise, md.Schedule]]:
        pass

    def _modify_item(
            self,
            modify_func: Callable[[Session, Union[md.Exercise, md.Schedule]],
                                  None]
    ) -> None:
        iid = self.selection()
        item_name: str = self._get_item_name(iid[0])
        # item_name: str = self.item(iid, 'text')
        with db.session_scope(self.engine) as session:
            item: Optional[Union[md.Exercise, md.Schedule]] = \
                self._get_item(session, item_name)
            if item:
                modify_func(session, item)
                session.commit()
                if callable(self.update_view_callback):
                    self.update_view_callback()
                # recover a selection if possible

    def delete_item(self):
        def delete_action(
                session: Session,
                item: Union[md.Exercise, md.Schedule]
        ) -> None:
            if askokcancel(
                    __name__,
                    f'Delete {type(item).__name__.lower()} "{item.name}" ?',
                    parent=self):
                session.delete(item)
        self._modify_item(delete_action)

    def rename_item(self):
        def rename_action(
                session: Session,
                item: Union[md.Exercise, md.Schedule]
        ) -> None:
            new_name: str = defaultdlg.askstring(
                __name__, f'Enter new {type(item).__name__.lower()} name',
                parent=self, default=item.name)
            if new_name:
                item.name = new_name
                session.add(item)
        self._modify_item(rename_action)


class ScheduleView(MutableView):
    def _get_view_selection(self, iid):
        return self.item(iid, 'text')

    def _get_item_name(self, iid):
        return self.item(iid, 'text')

    def _get_item(self, session, item_name):
        schedule = (session.query(md.Schedule)
                    .filter_by(name=item_name).first())
        return schedule


class RepertoireView(MutableView):
    def _get_view_selection(self, iid):
        iid = self.selection()
        if iid:
            return self.item(iid, 'values')[0]

    def _get_item_name(self, iid):
        def remove_id(s: str) -> str:
            m = re.match(r'^.*(?P<id> \(\d+\))$', s)
            return s[:m.start(1)] if m else s
        # iid = self.selection()[0]
        values = self.item(iid, 'values')
        exer_name = remove_id(values[0])
        return exer_name

    def _get_item(self, session, item_name):
        exer = (session.query(md.Exercise).filter_by(name=item_name).first())
        return exer
