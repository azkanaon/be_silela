import fastapi as _fastapi
from fastapi.middleware.cors import CORSMiddleware
import services as _services, schemas as _schemas
import sqlalchemy.orm as _orm
import fastapi.security as _security
from typing import List
from datetime import datetime
from fastapi import File, UploadFile
from fastapi.responses import FileResponse

app = _fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_services.create_database()

@app.post('/register')
def create_user(
    user: _schemas.UserCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="email already use")
    user = _services.create_user(db=db, user=user)
    return _services.create_token(user=user)

@app.post("/user/token")
def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = _services.authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return _services.create_token(user=user)

@app.get("/user", response_model=_schemas.User)
def get_user(
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
):
    return user

@app.get("/user/all", response_model=list)
def get_user_all(
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.get_user_all(db=db)

@app.get("/user/{email}", response_model=_schemas.User)
def get_user_by_email(
    email: str,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = _services.get_user_by_email(db=db, email=email)
    if not (user):
        raise _fastapi.HTTPException(status_code=400, detail="Sudah digunakan")
    else:
        return user

@app.delete("/user/delete/{user_id}")
def delete_user(
    user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    _services.delete_user(db=db, user_id=user_id)
    return {"message": f"successfully deleted user with id: {user_id}"}

@app.post("/uploadImage")
def upload(file: UploadFile = File(...)):
    try:
        filename = file.filename
        if not (filename.endswith(".png") or filename.endswith(".jpg")):
            raise _fastapi.HTTPException(status_code=400, detail="Hanya file PNG dan JPG yang diperbolehkan") #gak tau kenapa gak jalan

        contents = file.file.read()
        with open("./data_file/" + file.filename, "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "Error upload file"}
    finally:
        file.file.close()

    return {"message": f"Upload berhasil: {file.filename}"}

@app.get("/getFile/{nama_file}")
async def getFile(nama_file: str):
    return FileResponse("./data_file/" + nama_file)
