# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Index, UniqueConstraint, exc, ForeignKey
from contextlib import contextmanager
import logging

import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """
    Provide a transactional scope around a series of operations.
    """

    session = Session()

    try:
        yield session
        session.commit()
    except exc.IntegrityError as e:
        session.rollback()
        logging.warning(e.args[0])
    finally:
        session.close()


class Telephony(Base):
    __tablename__ = 'telephony'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    call_type = Column(String)
    department = Column(String)
    telephone_from = Column(String, index=True)
    telephone_to = Column(String, index=True)
    duration = Column(Integer)

    __table_args__ = (
        UniqueConstraint('datetime', 'call_type', 'telephone_from', 'telephone_to'),
        Index('index_call', 'datetime', 'call_type', 'telephone_from', 'telephone_to'))

    def __init__(self, datetime, call_type, department, telephone_from, telephone_to, duration):
        self.datetime = datetime
        self.call_type = call_type
        self.department = department
        self.telephone_from = telephone_from
        self.telephone_to = telephone_to
        self.duration = duration

    def __repr__(self):
        return "<Call('{}', '{}', '{}', '{}', '{}', '{}')>".format(self.datetime, self.call_type, self.department,
                                                                   self.telephone_from, self.telephone_to,
                                                                   self.duration)


class Calltouch(Base):
    __tablename__ = 'calltouch'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    type = Column(String)
    department = Column(String)
    telephone = Column(String, ForeignKey('telephony.telephone_from'), index=True)
    email = Column(String, index=True)
    source = Column(String)
    medium = Column(String)
    subject = Column(String)
    fio = Column(String)
    status = Column(String)
    deadline = Column(DateTime)
    utm_content = Column(String)
    utm_compaign = Column(String)
    requestid = Column(Integer, index=True)
    keyword = Column(String)

    __table_args__ = (
        UniqueConstraint('datetime', 'type', 'telephone', 'requestid'),
        Index('index_calltouch', 'datetime', 'type', 'telephone', 'requestid'),
    )

    def __init__(self, datetime, type, department, telephone, email, source, medium, subject, fio, status, deadline,
                 utm_content, utm_compaign, requestid, keyword):
        self.datetime = datetime
        self.type = type
        self.department = department
        self.telephone = telephone
        self.email = email
        self.source = source
        self.medium = medium
        self.subject = subject
        self.fio = fio
        self.status = status
        self.deadline = deadline
        self.utm_content = utm_content
        self.utm_compaign = utm_compaign
        self.requestid = requestid
        self.keyword = keyword

    def __repr__(self):
        return "<Lead('{}', '{}', '{}', '{}', '{}', '{}')>".format(self.datetime, self.type, self.telephone, self.email,
                                                                   self.source, self.medium)


class Erp(Base):
    __tablename__ = 'erp'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    client = Column(String)
    telephone = Column(String, ForeignKey('calltouch.telephone'), index=True)
    auto = Column(String)
    vin = Column(String, index=True)
    nak = Column(Integer)
    kom_num = Column(String, index=True)
    sum = Column(Integer)
    author = Column(String)
    manager = Column(String)
    contract = Column(String, index=True)
    ext_num = Column(String)
    contract_type = Column(String)
    status_auto = Column(String)
    availability = Column(String)
    all_money = Column(Integer)

    __table_args__ = (
        UniqueConstraint('datetime', 'telephone', 'vin', 'kom_num', 'contract'),
        Index('index_erp', 'datetime', 'telephone', 'vin', 'kom_num', 'contract'))

    def __init__(self, datetime, client, telephone, auto, vin, nak, kom_num, sum, author, manager, contract, ext_num,
                 contract_type, status_auto, availability, all_money):
        self.datetime = datetime
        self.client = client
        self.telephone = telephone
        self.auto = auto
        self.vin = vin
        self.nak = nak
        self.kom_num = kom_num
        self.sum = sum
        self.author = author
        self.manager = manager
        self.contract = contract
        self.ext_num = ext_num
        self.contract_type = contract_type
        self.status_auto = status_auto
        self.availability = availability
        self.all_money = all_money

    def __repr__(self):
        return "<Contract ('{}', '{}', '{}', '{}', '{}', '{}')>".format(self.datetime, self.client, self.telephone,
                                                                        self.auto, self.vin, self.sum)


class Ads(Base):
    __tablename__ = 'ads'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    source = Column(String, index=True)
    source_type = Column(String, index=True)
    department = Column(String, ForeignKey('calltouch.department'), index=True)
    shows = Column(Integer)
    clicks = Column(Integer)
    money = Column(Integer)

    __table_args__ = (
        UniqueConstraint('datetime', 'source', 'source_type', 'department'),
        Index('index_Ads', 'datetime', 'source', 'source_type', 'department'))

    def __init__(self, datetime, source, source_type, department, shows, clicks, money):
        self.datetime = datetime
        self.source = source
        self.source_type = source_type
        self.department = department
        self.shows = shows
        self.clicks = clicks
        self.money = money

    def __repr__(self):
        return "<Ads ('{}', '{}', '{}', '{}', '{}', '{}', '{}')>".format(self.datetime, self.source, self.source_type,
                                                                         self.department, self.shows, self.clicks,
                                                                         self.money)


class Traffic(Base):
    __tablename__ = 'traffic'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    source = Column(String, index=True)
    medium = Column(String, index=True)
    value = Column(Integer)

    __table_args__ = (
        UniqueConstraint('datetime', 'source', 'medium', 'value'),
        Index('index_Traffic', 'datetime', 'source', 'medium', 'value'))

    def __init__(self, datetime, source, medium, value):
        self.datetime = datetime
        self.source = source
        self.medium = medium
        self.value = value

    def __repr__(self):
        return "<Traffic ('{}', '{}', '{}', '{}')>".format(self.datetime, self.source, self.medium, self.value)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
