#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Exercise
from sqlalchemy import create_engine


if __name__ == '__main__':
    engine = create_engine('sqlite:///fitpad.db', echo=True)
    session = Session(engine)
    stmt = select(Exercise).where(True)
    for exercise in session.scalars(stmt):
        print(exercise)
