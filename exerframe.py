#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Generator, Tuple
import tkinter as tk
from sqlalchemy.engine.base import Engine
import frame2d_exer as f2e
from setframe import SetFrame
from entry_var import EntryVar


class ExerFrame(f2e.Frame2DExer):
    def __init__(self, parent, engine: Engine, **kwargs):
        super().__init__(parent, *kwargs)
        self.parent = parent
        self.engine: Engine = engine
        self.grid_row = 0

    @property
    def exer_order(self):
        return self.grid_row + 1

    def __iter__(self):
        return self._yield_exercises()

    def delete_grids(self):
        for w in self.yield_grids():
            if isinstance(w, SetFrame):
                w.delete_grids()
            w.destroy()
        self.grid_row = 0

    def _yield_exercises(self) -> Generator[
            Tuple[str, SetFrame], None, None]:
        num_columns, num_rows = self.grid_size()
        for i in range(num_rows):
            ev: EntryVar = self[i, 0]
            sf: SetFrame = self[i, 1]
            yield (ev.get(), sf)

    def add_exer(
            self, exer_name: str,
            init_exer: bool = True  # pass as `init_set' to SetFrame
    ) -> SetFrame:
        var = tk.StringVar()
        var.set(str(self.exer_order))  # refactor EntryVar.set()
        exer_no: EntryVar = EntryVar(self, textvariable=var, takefocus=False,
                                     width=2)
        exer_no.grid(column=0, row=self.grid_row)
        set_frame = SetFrame(self, self.engine, exer_name, init_set=init_exer)
        set_frame.grid(column=1, row=self.grid_row, sticky=tk.EW)
        self.columnconfigure(1, weight=1)
        self.grid_row += 1
        return set_frame

    def edit_exer(self):
        self.arrange()
