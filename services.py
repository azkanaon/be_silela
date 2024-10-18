import database as _database, models as _models, schemas as _schemas
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import jwt as _jwt
import fastapi as _fastapi
import fastapi.security as _security
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

_JWT_SECRET = "thisisnotverysafe"
oauth2schema = _security.OAuth2PasswordBearer(
    tokenUrl="/user/token", scheme_name="oauth2schema"
)

def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()

def create_user(db: _orm.Session, user: _schemas.UserCreate):
    hashed_password = _hash.bcrypt.hash(user.password)
    db_user = _models.User(
        nik=user.nik,
        no_kk=user.no_kk,
        rt=user.rt,
        rw=user.rw,
        nama=user.nama,
        email=user.email,
        password=hashed_password,
        telp=user.telp,
        fotoKtp=user.fotoKtp
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_token(user: _models.User):
    user_schema_obj = _schemas.User.from_orm(user)
    user_dict = user_schema_obj.dict()

    expires = datetime.utcnow() + timedelta(minutes=60)
    user_dict["exp"] = expires

    token = _jwt.encode(user_dict, _JWT_SECRET)
    return dict(access_token=token, token_type="bearer")

def authenticate_user(email: str, password: str, db: _orm.Session):
    user = get_user_by_email(email=email, db=db)

    if not user:
        return False

    if not user.verify_password(passwords=password):
        return False

    return user

def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Email Atau Password Salah"
        )

    return _schemas.User.from_orm(user)

def get_user_all(db: _orm.Session = _fastapi.Depends(get_db),):
    users = db.query(_models.User).all()
    return users

def delete_user(db: _orm.Session, user_id: int):
    db.query(_models.User).filter(_models.User.id == user_id).delete()
    db.commit()