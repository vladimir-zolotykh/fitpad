#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk


class Frame2D(tk.Frame):
    def __init__(self, parent, **kwargs):
        super(Frame2D, self).__init__(parent, **kwargs)

    def __getitem__(self, rowcol):
        col_max, row_max = self.grid_size()
        row, col = rowcol
        if (0 <= col < col_max) and (0 <= row < row_max):
            slaves = self.grid_slaves(row=row)
            for widget in slaves:
                if widget.grid_info()['column'] == col:
                    return widget
        else:
            raise IndexError()


if __name__ == '__main__':
    root = tk.Tk()
    frame = Frame2D(root, name='frame2d')
    frame.grid(column=0, row=0, sticky=tk.NSEW)
    label = tk.Label(frame, text='Deadlift', name='exercise_name_label')
    label.grid(column=0, row=0, columnspan=3)
    set_no = tk.Entry(frame, width=2, name='set_no_entry')
    set_no.grid(column=0, row=1)
    weight = tk.Entry(frame, width=8, name='weight_entry')
    weight.grid(column=1, row=1)
    reps = tk.Entry(frame, width=4, name='reps_entry')
    reps.grid(column=2, row=1)
    btn = tk.Button(frame, text='Edit', name='edit_button')
    btn.grid(column=0, row=2, columnspan=3)
    root.mainloop()
