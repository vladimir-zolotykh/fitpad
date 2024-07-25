#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Workout
from sqlalchemy import create_engine


if __name__ == '__main__':
    engine = create_engine('sqlite:///fitpad.db', echo=True)
    session = Session(engine)
    stmt = select(Workout).where(True)
    for workout in session.scalars(stmt):
        print(workout)
