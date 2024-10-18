import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import database as _database
import datetime as _dt
import passlib.hash as _hash

class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    nik = _sql.Column(_sql.String)
    no_kk = _sql.Column(_sql.String)
    rt = _sql.Column(_sql.String)
    rw = _sql.Column(_sql.String)
    nama = _sql.Column(_sql.String)
    email = _sql.Column(_sql.String, unique=True)
    password = _sql.Column(_sql.String)
    telp = _sql.Column(_sql.String)
    fotoKtp = _sql.Column(_sql.String)

    def verify_password(self, passwords: str):
        return _hash.bcrypt.verify(passwords, self.password)
    

