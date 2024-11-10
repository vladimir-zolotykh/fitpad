#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC
from abc import abstractmethod
from typing import Callable, Union
import re
from sqlalchemy.orm import Session
from tkinter.messagebox import askokcancel
import models as md
import database as db
from scrolledtreeview import ScrolledTreeview
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

    def delete_item(self):
        def delete_action(
                session: Session,
                item: Union[md.Exercise, md.Schedule]
        ) -> None:
            if askokcancel(__name__, f'Delete {type(item)} "{item.name}" ?',
                           parent=self):
                session.delete(item)
        self._modify_item(delete_action)

    def rename_item(self):
        def rename_action(
                session: Session,
                item: Union[md.Exercise, md.Schedule]
        ) -> None:
            new_name: str = defaultdlg.askstring(
                __name__, f'Enter new {type(item)} name',
                parent=self, default=item.name)
            if new_name:
                item.name = new_name
                session.add()
        self._modify_item(rename_action)


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


class RepertoireView(MutableView):
    def _get_item_name(self) -> str:
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
