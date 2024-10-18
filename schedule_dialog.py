#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from tkinter import ttk, simpledialog  # noqa
from ttkwidgets.autocomplete import AutocompleteCombobox


class ScheduleDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, values=None):
        self.schedule_name = ''
        self.values = values
        super().__init__(parent, title=title)

    def body(self, master):
        self.combobox = AutocompleteCombobox(
            master, completevalues=self.values)
        self.combobox.grid(row=0, column=1, padx=10, pady=10)
        self.combobox.current(0)

        return self.combobox

    def apply(self):
        """Called when OK is pressed

        Get the value from the Combobox and save it in schedule_name
        """

        self.schedule_name = self.combobox.get()
