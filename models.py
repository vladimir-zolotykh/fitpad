#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Workout(Base):
    __tablename__ = 'workout'
    id: Mapped[int] = mapped_column(primary_key=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercise.id'))
    exercise: Mapped['Exercise'] = relationship(back_populates='workouts')
    reps: Mapped[int]
    weight: Mapped[float]
    date: Mapped[str]


class Exercise(Base):
    __tablename__ = 'exercise'
    id: Mapped[int] = mapped_column(primary_key=True)
    workouts: Mapped[List['Workout']] = relationship(back_populates='exercise')
    name: Mapped[str]
