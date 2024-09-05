from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from ..database import get_db
from ..config import settings


router = APIRouter(
    prefix="/admins",
    tags=["Admin Authentication"]
)

admin_header_scheme = APIKeyHeader(name="admin_token")


@router.post("/login", response_model=schemas.Token)
def admin_login(admin_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    admin = db.query(models.Admin).filter(admin_credentials.username == models.Admin.email).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(admin_credentials.password, admin.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"id": admin.id})
    return {"access_token": access_token,
            "token_type": "bearer"}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminOut)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db), key: str = Depends(admin_header_scheme)):
    if key == settings.ADMIN_TOKEN:
        try:
            hashed_password = utils.hash(admin.password)
            admin.password = hashed_password
            new_admin = models.Admin(name=admin.name, email=admin.email, password=hashed_password)
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
        except Exception:
            raise HTTPException(status_code=status.HTTP_226_IM_USED, detail=Exception)
        return new_admin
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")


@router.get("/", response_model=schemas.AdminOut, status_code=status.HTTP_200_OK)
def get_admin(db: Session = Depends(get_db), admin_user: int = Depends(oauth2.get_current_admin)):
    admin = db.query(models.Admin).filter(admin_user.id == models.Admin.id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"admin with id: {admin_user.id} was not found")
    if admin_user.id != admin.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to perform this action")
    return admin
