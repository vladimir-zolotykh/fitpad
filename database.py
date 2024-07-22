#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import models as md


@contextmanager
def session_scope(engine):
    """Provide a transactional scope around a series of operations"""

    Session = sessionmaker(engine, class_=Transaction)
    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


class Transaction(Session):
    pass


def initialize(engine):
    """Initialize DB tables"""

    with Session(engine) as session:
        md.Base.metadata.create_all(engine)
        session.commit()
        session.close()
