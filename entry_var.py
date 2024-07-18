#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk


class EntryVar(tk.Entry):
    def __init__(self, parent, cnf=None, **kw):
        super(EntryVar, self).__init__(parent, cnf, **kw)
        if isinstance(cnf, dict):
            kw.update(cnf)
        if 'textvariable' in kw:
            self._var = kw.get('textvariable')

    def configure(self, cnf=None, **kw):
        if cnf is None and not kw:
            return super().configure()
        elif isinstance(cnf, str):
            if cnf == 'textvariable':
                return self._var
            else:
                return self._get_config(cnf)
        elif isinstance(cnf, dict):
            kw.update(cnf)
        return self._set_config(**kw)

    config = configure

    def _get_config(self, option=None):
        if option:
            return super().configure(option)
        else:
            return super().configure()

    def _set_config(self, **options):
        if 'textvariable' in options:
            self._var = options.get('textvariable')
        return super().configure(**options)
