import datetime

from sqlalchemy import Integer, String, DateTime, Numeric, SmallInteger, DATETIME

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Fakenames(Base):
    __tablename__ = 'fakenames'
    __table_args__ = {'extend_existing': True}

    number = mapped_column(Integer, primary_key=True)
    gender = mapped_column(String(6))
    nameset = mapped_column(String(25))
    title = mapped_column(String(6))
    givenname = mapped_column(String(20))
    middleinitial = mapped_column(String(1))
    surname = mapped_column(String(23))
    streetaddress = mapped_column(String(100))
    city = mapped_column(String(100))
    state = mapped_column(String(22))
    statefull = mapped_column(String(100))
    zipcode = mapped_column(String(15))
    country = mapped_column(String(2))
    countryfull = mapped_column(String(100))
    emailaddress = mapped_column(String(100))
    username = mapped_column(String(25))
    password = mapped_column(String(25))
    browseruseragent = mapped_column(String(255))
    telephonenumber = mapped_column(String(25))
    telephonecountrycode = mapped_column(Integer)
    mothersmaiden = mapped_column(String(23))
    # birthday = mapped_column(DateTime)
    birthday: Mapped[datetime.datetime] = mapped_column(DATETIME(timezone=True))
    age = mapped_column(Integer)
    tropicalzodiac = mapped_column(String(11))
    cctype = mapped_column(String(10))
    ccnumber = mapped_column(String(16))
    cvv2 = mapped_column(Numeric(3))
    ccexpires = mapped_column(String(10))
    nationalid = mapped_column(String(20))
    ups = mapped_column(String(24))
    westernunionmtcn = mapped_column(String(10))
    moneygrammtcn = mapped_column(String(8))
    color = mapped_column(String(6))
    occupation = mapped_column(String(70))
    company = mapped_column(String(70))
    vehicle = mapped_column(String(255))
    domain = mapped_column(String(70))
    bloodtype = mapped_column(String(3))
    pounds = mapped_column(Numeric(5, 1))
    kilograms = mapped_column(Numeric(5, 1))
    feetinches = mapped_column(String(6))
    centimeters = mapped_column(SmallInteger)
    guid = mapped_column(String(36))
    latitude = mapped_column(Numeric(10, 8))
    longitude = mapped_column(Numeric(11, 8))
