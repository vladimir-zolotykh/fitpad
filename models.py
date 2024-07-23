#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Workout(Base):            # parent
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    exercises: Mapped[List["Exercise"]] = relationship(
        back_populates="workout")
    reps: Mapped[int]
    weight: Mapped[float]
    date: Mapped[str]


class Exercise(Base):           # child
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    workout_id: Mapped[int] = mapped_column(ForeignKey("workouts.id"))
    workout: Mapped["Workout"] = relationship(back_populates="exercises")
    name: Mapped[str]
