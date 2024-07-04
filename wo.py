#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Dict, Any, List, Optional
from functools import partial
import tkinter as tk


class ExerTk(tk.Frame):
    """Make tk widgets representing an exercise"""

    NUM_COLUMNS = 3
    COL_WIDTH = {'set_no': 2, 'weight': 10, 'reps': 3}

    def __init__(self, parent, name: str, row: int):
        super(ExerTk, self).__init__(parent)
        self.grid(column=0, row=row, sticky=tk.EW)
        self.name = name
        self.last_set: int = 1
        self.set_no: Dict[int, tk.StringVar] = {}
        self.config(bd=2, relief=tk.RIDGE)
        self.columnconfigure(0, weight=1)
        for c in range(self.NUM_COLUMNS):
            self.columnconfigure(c, weight=1)
        tk.Label(self, text=name).grid(
            column=0, row=0, columnspan=self.NUM_COLUMNS)
        self.add_set0()
        mb = tk.Menubutton(self, relief=tk.RAISED, text='Edit')
        mb.grid(column=0, row=2, columnspan=self.NUM_COLUMNS)
        mb_menu = tk.Menu(mb, tearoff=0)
        mb['menu'] = mb_menu
        mb_menu.add_command(label='Add set', command=self.add_set2)
        mb_menu.add_command(label='Move up')
        mb_menu.add_command(label='Move down')
        mb_menu.add_command(label='Remove')
        mb_menu.add_command(label='Edit sets', command=self.edit_sets)

    def edit_sets(self):
        def get_column(widget: tk.Widget) -> int:
            return int(widget.grid_info()['column'])

        def get_widget(
                widgets: List[tk.Widget], column: int = 0
        ) -> Optional[tk.Widget]:
            for w in widgets:
                # if w.grid_info()['column'] == column:
                if get_column(w) == column:
                    return w
            return None

        def get_set_no(widgets: List[tk.Widget]) -> int:
            w = get_widget(widgets, 0)
            if isinstance(w, tk.Entry):
                return int(w.get())
            else:
                raise TypeError('Expected Entry widget')

        _, num_rows = self.grid_size()
        sets_sorted = sorted(
            [self.grid_slaves(row=row) for row in range(1, num_rows - 1)],
            key=get_set_no)
        rows_sorted: Dict[int, List[tk.Widget]] = {}
        for num_row, row in enumerate(sets_sorted, 1):
            print(f'rows_sorted: {num_row = }')
            if get_set_no(row) == 0:
                for w in row:
                    w.destroy()
                self.last_set -= 1
                # del self.set_no[get_set_no(row)]
            else:
                rows_sorted[num_row] = sorted(row, key=get_column)
                for w in row:
                    w.grid_forget()
        for num_row, row in rows_sorted.items():
            print(f'{num_row = }')
            var = self.set_no[num_row]
            var.set(num_row)
            for col, w in enumerate(row):
                w.grid(column=col, row=num_row + 1)

    def _add_set_row(self, row):
        """Grid a set's widgets

        Exercises have sets. A set has tk widgets organized in a
        row. This method adds widgets for one set.
        """
        var = tk.StringVar()
        var.set(str(row))
        self.set_no[row] = var
        for c, w in enumerate(self.COL_WIDTH.values()):
            e = tk.Entry(self, width=w)
            e.grid(column=c, row=row)
            if c == 0:
                e.config(textvariable=var)

    def add_set2(self):
        num_rows = self.grid_size()[1]
        # 3 <= num_rows
        mb = self.grid_slaves(row=num_rows-1)[0]  # menu button
        last_set_row = num_rows - 1
        self._add_set_row(last_set_row)
        mb.grid(column=0, row=last_set_row + 1, columnspan=self.NUM_COLUMNS)

    def add_set0(self):
        # self.grid_size()[1] == 1
        self._add_set_row(self.last_set)
        self.last_set += 1


class ExerDir(Dict[str, ExerTk]):
    """A dict of Workout exercises

    Dict[str, ExerTk]
    """

    def __init__(self, frame: tk.Frame):
        super().__init__()
        self.frame: tk.Frame = frame
        self.row: int = 0

    def add_exer(self, name: str):
        self[name] = ExerTk(self.frame, name, self.row)
        self.row += 1

    def del_exer(self, name: str):
        exertk = self[name]
        exertk.destroy()
        self.row -= 1


class Workout(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(Workout, self).__init__(*args, **kwargs)
        self.title('Workout')
        self.geometry('500x200+400+300')
        menubar = tk.Menu(self, tearoff=0)
        self['menu'] = menubar
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Quit', command=self.quit)
        menubar.add_cascade(label='File', menu=file_menu)
        add_exer_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Add exercise', menu=add_exer_menu)
        self.exer_dir: Dict[str, Any] = {
            'squat': None, 'bench press': Any, 'deadlift': Any
        }
        frame = tk.Frame(self)
        frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        dir = ExerDir(frame)
        for name in self.exer_dir:
            _add_exer = partial(dir.add_exer, name)
            add_exer_menu.add_command(label=name, command=_add_exer)


if __name__ == '__main__':
    Workout().mainloop()
