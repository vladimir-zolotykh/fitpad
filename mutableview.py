#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC
from abc import abstractmethod
from typing import Callable, Union
from sqlalchemy.orm import Session
from tkinter.messagebox import askokcancel
import models as md
import database as db
from scrolledtreeview import ScrolledTreeview
from defaultdlg import askstring
import defaultdlg


class MutableView(ScrolledTreeview, ABC):
    def __init__(self, parent, **kw):
        if 'update_view_callback' in kw:
            self.update_view_callback = kw.get('update_view_callback')
        super().__init__(parent, **kw)

    @abstractmethod
    def _get_item_name():
        pass

    @abstractmethod
    def _get_item(
            self, session: Session, item_name: str
    ) -> Union[md.Exercise, md.Schedule]:
        pass

    def _modify_item(
            self, modify_func: Callable[[Session, md.Schedule], None]
    ) -> None:
        item_name: str = self._get_item_name()
        # iid = self.selection()[0]
        # item_name: str = self.item(iid, 'text')
        with db.session_scope(self.engine) as session:
            item: Union[md.Exercise, md.Schedule] = \
                self._get_item(session, item_name)
            if item:
                modify_func(session, item)
                session.commit()
                if callable(self.update_view_callback):
                    self.update_view_callback()

    @abstractmethod
    def delete_item(self):
        pass

    @abstractmethod
    def rename_item(self):
        pass


class ScheduleView(MutableView):
    def _get_item_name(self) -> str:
        iid = self.selection()[0]
        schedule_name: str = self.item(iid, 'text')
        return schedule_name

    def _get_item(
            self, session: Session, item_name: str
    ) -> md.Schedule:
        schedule = (session.query(md.Schedule)
                    .filter_by(name=item_name).first())
        return schedule

    def delete_item(self):
        """Delete selected schedule"""

        def delete_action(session: Session, schedule: md.Schedule) -> None:
            if askokcancel(__name__, f'Delete schedule "{schedule.name}" ?',
                           parent=self):
                session.delete(schedule)
        self._modify_item(delete_action)

    def rename_item(self):
        """Rename selected schedule"""

        def rename_action(session: Session, schedule: md.Schedule) -> None:
            new_name: str = defaultdlg.askstring(
                __name__, 'Enter new schedule name',
                parent=self, default=schedule.name)
            if new_name:
                schedule.name = new_name
                session.add()
        self._modify_item(rename_action)


class RepertoireView(MutableView):
    def _get_item_name() -> str:
        def remove_id(s: str) -> str:
            m = re.match(r'^.*(?P<id> \(\d+\))$', s)
            return s[:m.start(1)] if m else s
        iid = self.selection()[0]
        values = self.item(iid, 'values')
        exer_name = remove_id(values[0])
        return exer_name
        
    def _get_item(
            self, session: Session, item_name: str
    ) -> md.Exercise:
        exer = (session.query(md.Exercise).filter_by(name=item_name).first())
        return exer

    def delete_item(self):
        def delete_action(session: Session, exer: md.Exercise) -> None:
            if askokcancel(__name__, f'Delete exercise "{exer.name}" ?',
                           parent=self):
                session.delete(exer)
        self._modify_item(delete_action)

    def rename_item(self):
        def rename_action(session: Session, exer: md.Exercise) -> None:
            new_name: str = askstring(__name__, 'Enter exercise name',
                                      parent=self, default=exer.name)
            if new_name:
                exer.name = new_name
                session.add(exer)
        self._modify_item(rename_action)
