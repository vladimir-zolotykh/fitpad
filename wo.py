#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk


class Workout(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(self).__init__(*args, **kwargs)
        self.title('Workout')
        self.geometry('500x200+400+300')


if __name__ == '__main__':
    Workout().mainloop()
