#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import sys
from contextlib import contextmanager
from typing import Generator, List, cast, Optional
from operator import itemgetter
from functools import partial
import tkinter as tk
from sqlalchemy import select
from sqlalchemy.engine.base import Engine
import models as md
import database as db
from entry_var import EntryVar
from combo_var import ComboVar
import frame2d_set as f2s


class SetFrame(f2s.Frame2DSet):
    """Make tk widgets representing an exercise"""

    NUM_COLUMNS = 3
    COL_WIDTH = {'set_no': 2, 'weight': 10, 'reps': 3}

    def __init__(
            self, parent, engine: Engine, name: str,
            init_set: bool = True):  # add initial set
        super().__init__(parent)
        self.engine: Engine = engine
        # self.grid(column=0, row=row, sticky=tk.EW)
        self.name = name
        self.last_set: int = 1
        # self.set_no: Dict[int, tk.StringVar] = {}
        pady: int = 2
        self.config(bd=pady, relief=tk.RIDGE)
        self.columnconfigure(0, weight=1)
        for c in range(self.NUM_COLUMNS):
            self.columnconfigure(c, weight=1)
        self.label = label = tk.Label(self, text=name)
        label.grid(column=0, row=0, columnspan=self.NUM_COLUMNS)
        if init_set:
            self.add_set()
        mb = tk.Menubutton(self, relief=tk.RAISED, text='Edit')
        mb.grid(column=0, row=2, columnspan=self.NUM_COLUMNS)
        mb_menu = tk.Menu(mb, tearoff=0)
        mb['menu'] = mb_menu
        mb_menu.add_command(label='Add set', command=self.add_set)
        mb_menu.add_command(label='Edit sets', command=self.edit_sets)
        label.configure(pady=pady + (mb.winfo_reqheight() -
                                     label.winfo_reqheight()) // 2)

    @property
    def exer_name(self) -> str:
        return self.label.cget('text')

    @contextmanager
    def num_rows_printed(self, label='***'):
        n1 = self.grid_size()[1]
        yield
        n2 = self.grid_size()[1]
        print(f'{label} num_rows = {n1}/{n2}')
        sys.stdout.flush()

    def __iter__(self):
        return self._yield_sets()

    def _yield_sets(self) -> Generator[List[str], None, None]:
        num_columns, num_rows = self.grid_size()
        for i in range(1, num_rows - 1):
            values = []
            for j in range(1, num_columns):  # skip set_no
                w: tk.Widget = self[i, j]
                if isinstance(w, ComboVar):
                    v: ComboVar = cast(ComboVar, w)
                    values.append(v.get())
                else:
                    raise TypeError(f'Expected ComboVar widget, got {type(w)}')
            yield values

    def edit_sets(self):
        self.arrange()

    def grid_the_set(
            self, num_row: int,
            wo: Optional[md.Workout] = None
    ) -> None:
        """Grid a set's widgets

        Exercises have sets. A set has tk widgets organized in a
        row. This method adds widgets for one set.
        """
        # [(weight, reps), ...]
        hist: list[tuple[float, float]] = self.get_exer_history(self.exer_name)
        weight_hist = [itemgetter(0)(h) for h in hist]
        reps_hist = [itemgetter(1)(h) for h in hist]
        if wo:
            weight_hist[0] = wo.weight
            reps_hist[0] = wo.reps

        # Widget type, widget width, init values
        cfg = ((EntryVar, 2, (num_row, )),
               (ComboVar, 10, weight_hist),
               (ComboVar, 3, reps_hist))
        for col, (cls, width, values) in enumerate(cfg):
            var = tk.StringVar()
            w = cls(self, textvariable=var, width=width)
            if isinstance(w, EntryVar):
                w.configure(takefocus=False)
            if values:
                var.set(str(values[0]))
            if issubclass(cls, ComboVar):
                field: ComboVar = cast(ComboVar, w)
                field.configure(values=values)
            w.grid(column=col, row=num_row)
        self.last_set += 1

    def get_exer_history(self, exer_name: str, hist_len: int = 10):
        # query = (
        #     select(md.Workout)
        #     .join(md.Workout.exercise)
        #     .where(md.Exercise.name == exer_name))

        # Example how to use .select_from
        query = (
            select(md.Workout)
            .select_from(md.Exercise)
            .join(md.Exercise.workouts)
            .where(md.Exercise.name == exer_name)
        )
        hist: list[tuple[float, float]] = []
        with db.session_scope(self.engine) as session:
            for wo in session.scalars(query):
                hist.append((wo.weight, wo.reps))
        return hist

    def add_set(self, wo: Optional[md.Workout] = None):
        """Take weight, reps fields from WO parameter"""

        num_rows: int = self.grid_size()[1]
        _grid_the_set = partial(self.grid_the_set, wo=wo)
        if 2 <= num_rows:
            mb = self.grid_slaves(row=num_rows - 1)[0]  # menu button
            last: int = num_rows - 1
            _grid_the_set(last)
            mb.grid(column=0, row=last + 1, columnspan=self.NUM_COLUMNS)
        elif num_rows == 1:
            _grid_the_set(self.last_set)
        else:
            raise TypeError(f'{num_rows = }: must be 1 or >= 2')
