#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk


class NumberedFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    def print_size(meth):
        """A decorator to print called method's name

        and the Frame's size
        in the form
        NumberedFrame.edit_sets: num_cols = 2, num_rows = 2
        """

        def wrapper(self, *args, **kwargs):
            num_cols, num_rows = self.grid_size()
            cls_name = self.__class__.__name__
            print(f'{cls_name}.{meth.__name__}: {num_cols = }, {num_rows = }')
            return meth(self, *args, **kwargs)
        return wrapper

    @print_size
    def edit_sets(self, msg=None):
        msg = msg if msg else 'Hello'
        print(f'{msg = }')


if __name__ == '__main__':
    root = tk.Tk()
    frame = NumberedFrame(root)
    frame.grid(column=0, row=0, sticky=tk.NSEW)
    for i in range(4):
        _ = tk.Label(frame, text=f'{i}')
        _.grid(column=i % 2, row=i // 2)
    frame.edit_sets('Hello, world!')
    root.mainloop()
