#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Tuple
import frame2d as f2
from entry_var import EntryVar


class Frame2DSet(f2.Frame2D):
    def row_range(self) -> Tuple[int, int]:
        _, num_rows = self.grid_size()
        return (1, num_rows - 1)

    def arrange(self):
        cols, rows = self.grid_size()
        for i in range(1, rows - 1):
            slaves = self.grid_slaves(row=i)
            saved.append(slaves)
            set_no: EntryVar = self[i, 0]
            if int(set_no.get()) == 0:
                pass
            else:
                pass

            print(numbered_set)
        # print(f'Frame2DSet.arrange {cols = }, {rows = }')


