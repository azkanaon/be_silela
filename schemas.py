from typing import List
import datetime as _dt
import pydantic as _pydantic
from pydantic import Field
from typing import Optional

class _UserBase(_pydantic.BaseModel):
    nik: str
    no_kk: str
    rt: str
    rw: str
    nama: str
    email: str
    telp: str
    fotoKtp: str

class UserCreate(_UserBase):
    password: str

class User(_UserBase):
    id: int

    class Config:
        orm_mode = True

