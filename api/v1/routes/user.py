from fastapi import Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session

from ..models.user import User
from api.v1.schemas.user import DeactivateUserSchema
from api.db.database import get_db
from api.utils.dependencies import get_current_user


user = APIRouter(prefix='/api/v1', tags=['Users'])

@user.patch('/accounts/deactivate', status_code=200)
async def deactivate_account(request: Request, schema: DeactivateUserSchema, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    '''Endpoint to deactivate a user account'''

    if not user.is_active:
        raise HTTPException(400, 'User is inactive')
    
    if schema.confirmation == False:
        raise HTTPException(400, 'Confirmation required to deactivate account')

    user.is_active = False

    # Commit changes to deactivate the user
    db.commit()

    return {"status_code": 200, "message": "Account deactivated successfully"}
