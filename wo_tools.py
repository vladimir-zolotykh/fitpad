#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from typing import Dict, List, Optional, cast
from prettytable import PrettyTable
from entry_var import EntryVar
from frame2d import Frame2D


class NumberedExer(list):
    """class to `unpack' the grid structure

    The grid structure represents has two widgets: tk.Entry
    (`exer_no') and Frame2D(ExerTk) and is made in
    NumberedFrame. NumberedExer.__getattr__ is used to
    grid_forget/[re-]grid_pack
    """

    def __init__(self, frame: Frame2D):
        num_cols, num_rows = frame.grid_size()
        assert num_rows == 1
        self.frame = frame      # '.workout_frame.exer_wrap_frame00'
        super().__init__(frame[0, col] for col in range(num_cols))

    def __getattr__(self, name):
        return getattr(self.frame, name)

    def exer_name(self) -> str:
        frame2d: Frame2D = self[1]
        # exertk_frame: ExerTk = frame2d[0, 0]
        exertk_frame = frame2d[0, 0]
        label: tk.Label = cast(tk.Label, exertk_frame.grid_slaves(row=0)[0])
        return label.cget('text')

    def exer_no(self) -> int:
        if isinstance(self[0], EntryVar):
            return int(self[0].get())
        else:
            raise TypeError(f'Expected EntryVar, got {type(self[0])}')


class Wo(list):
    def __init__(self, frame: Frame2D):
        # frame: '.workout_frame'
        num_cols, num_rows = frame.grid_size()  # 1, 1
        super().__init__(
            [NumberedExer(cast(Frame2D, frame.grid_slaves(row=row)[0]))
             for row in range(num_rows)])
        self.sort(key=lambda e: e.exer_no())


class Row(list):
    def __init__(self, widgets: List[tk.Widget]):
        super().__init__(widgets)

    @staticmethod
    def grid_column(widget: tk.Widget) -> int:
        """Return the column of widget"""

        return int(widget.grid_info()['column'])

    @classmethod
    def from_grid(cls, box: tk.Frame, row: int) -> 'Row':
        slaves = sorted(box.grid_slaves(row=row), key=Row.grid_column)
        return cls(slaves)

    @classmethod
    def from_list(cls, row: List[tk.Widget]) -> 'Row':
        return cls(sorted(row, key=Row.grid_column))

    def column(self, column: int = 0) -> Optional[tk.Widget]:
        for w in self:
            if Row.grid_column(w) == column:
                return w
        return None

    def set_no(self) -> int:
        """Return the set number

        Each set [of exercise] has a set number, the 1st Entry widget
        of a grid row"""

        w: Optional[tk.Widget] = self.column(0)
        if isinstance(w, EntryVar):
            var: tk.StringVar = w.configure('textvariable')
            return int(var.get())
        else:
            raise TypeError(f'Expected Entry widget, got {type(w)}')


def grid_info(container: tk.Frame) -> str:
    num_cols, num_rows = container.grid_size()
    table = PrettyTable()
    # table.align = 'l'
    table.field_names = ['row', 'num columns']
    for num_row in range(num_rows):
        table.add_row([num_row, len(container.grid_slaves(row=num_row))])
    return str(table)


def rows_info(rows: Dict[int, Row]) -> str:
    table = PrettyTable()
    table.field_names = ['row', 'num columns']
    for row in range(len(rows)):
        try:
            table.add_row([row, len(rows[row + 1])])
        except KeyError:
            pass
    return str(table)
