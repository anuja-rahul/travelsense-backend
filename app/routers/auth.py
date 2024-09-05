from ..database import get_db
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=["User Authentication"]
)

# user_header_scheme = APIKeyHeader(name="admin_token")


@router.post("/login", response_model=schemas.Token)
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(user_credentials.username == models.User.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"id": user.id})

    return {"access_token": access_token,
            "token_type": "bearer"}


@router.get("/verify", response_model=schemas.VerificationBase, status_code=status.HTTP_201_CREATED)
def get_verification_code(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    user_query = db.query(models.User).filter(current_user.id == models.User.id)
    user = user_query.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: [{current_user.id}] does not exist")
    try:
        verification_query = db.query(models.UserVerification).filter(current_user.id == models.UserVerification.user_id)
        existing_verification = verification_query.first()

        if existing_verification:
            existing_verification.code = utils.get_one_time_passcode()
            db.commit()
            db.refresh(existing_verification)
            return existing_verification
        else:
            new_user_code = models.UserVerification(user_id=current_user.id, code=utils.get_one_time_passcode())
            db.add(new_user_code)
            db.commit()
            db.refresh(new_user_code)
            return new_user_code

    except Exception:
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail=f"email or username already in use.")


@router.post("/verify", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut)
def verify_user(verification_code: schemas.VerificationCheck, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(current_user.id == models.User.id)
    user = user_query.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: [{current_user.id}] does not exist")

    if user.verified:
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail=f"User already verified")
    else:
        verification_query = db.query(models.UserVerification).filter(current_user.id == models.UserVerification.user_id)
        existing_verification = verification_query.first()

        if existing_verification:
            if existing_verification.code == verification_code.code:
                user.verified = True
                db.commit()
                db.refresh(user)
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No verification code was found.")


