import datetime
from pydantic import BaseModel


class FakenamesBase(BaseModel):
    number: int
    gender: str
    nameset: str
    title: str
    givenname: str
    middleinitial: str
    surname: str
    streetaddress: str
    city: str
    state: str
    statefull: str
    zipcode: str
    country: str
    countryfull: str
    emailaddress: str
    username: str
    password: str
    browseruseragent: str
    telephonenumber: str
    telephonecountrycode: int
    mothersmaiden: str
    birthday: datetime.date
    age: int
    tropicalzodiac: str
    cctype: str
    ccnumber: str
    cvv2: int
    ccexpires: str
    nationalid: str
    ups: str
    westernunionmtcn: str
    moneygrammtcn: str
    color: str
    occupation: str
    company: str
    vehicle: str
    domain: str
    bloodtype: str
    pounds: float
    kilograms: float
    feetinches: str
    centimeters: int
    guid: str
    latitude: float
    longitude: float


class FakenamesCreate(FakenamesBase):
    pass


class FakenamesUpdate(FakenamesBase):
    pass


class FakenamesDelete(BaseModel):
    deleted: bool
    gender: str
    nameset: str
    title: str
    givenname: str
    middleinitial: str
    surname: str
    guid: str


class Fakenames(FakenamesBase):
    number: int

    class Config:
        from_attributes = True
