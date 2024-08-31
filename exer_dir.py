#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Dict, List
from exertk import SetFrame
from frame2d_exer import Frame2DExer
from numbered_frame import NumberedFrame


class ExerDir(Dict[str, SetFrame]):
    """A dict of Workout exercises

    Dict[str, SetFrame]
    """

    def __init__(self, frame: Frame2DExer):
        super().__init__()
        self.frame: Frame2DExer = frame
        self.row: int = 0

    def del_exer(self, name: str):
        del self[name]
        self.row -= 1

    def edit_exer(self):
        deleted_exer: List[str] = self.frame.arrange()
        exer_name: str
        for exer_name in deleted_exer:
            self.del_exer(exer_name)

    def add_exer(self, name: str):
        numbered_frame = NumberedFrame(self.frame, self.row)
        self[name] = SetFrame(numbered_frame.exer_box, name, 0)
        self.row += 1
