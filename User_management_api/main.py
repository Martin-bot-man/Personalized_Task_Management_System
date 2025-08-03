from fastapi import FastAPI, Request, HTTPException, Depends,Query
from fastapi.responses import ORJSONResponse
from python_gzip_middleware import GzipMiddleware
app.add_middleware(GzipMiddleware)
from slowapi.errors import RateLimitExceeded 
from models import UserCreate, UserUpdate, UserOut
from database import get_db, get_redis,create_user, get_user,update_user, delete_user, list_users
import logging

#configuring logging
logging.basicConfig(level=logging.INFO)
logger= logging.getLogger(__name__)

#initializing fastApI with orjsonresponse for faster json

app = FastAPI(default_response_clfrom fastapi import FastAPI, Request, HTTPException, Depends, Query
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import gzip
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from models import UserCreate, UserUpdate, UserOut
from database import get_db, get_redis, create_user, get_user, update_user, delete_user, list_users
from sqlalchemy.orm import Session
from aioredis import Redis
import logging

# Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initializing FastAPI with ORJSONResponse for faster JSON
app = FastAPI(default_response_class=ORJSONResponse)

# Custom Gzip Middleware
class GzipMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.headers.get("content-encoding", "").lower() != "gzip":
            if "text" in response.headers.get("content-type", "") or "application/json" in response.headers.get("content-type", ""):
                body = response.body
                if body and len(body) > 1000:  # Minimum size to compress
                    compressed_body = gzip.compress(body)
                    response.body = compressed_body
                    response.headers["content-encoding"] = "gzip"
                    response.headers["content-length"] = str(len(compressed_body))
        return response

# Add Gzip middleware for response compression
app.add_middleware(GzipMiddleware)

# Setup rate limit
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # Note: _rate_limit_exceeded_handler should be defined or imported

# CRUD Endpoints
@app.post("/users/", response_model=UserOut)
@limiter.limit("5/minute")
async def create_user_endpoint(user: UserCreate, request: Request, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    try:
        user_data = await create_user(db, redis, user)
        return user_data
    except Exception as e:
        logger.error(f'Error creating user: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}", response_model=UserOut)
@limiter.limit("10/minute")
async def get_user_endpoint(user_id: int, request: Request, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    logger.info(f"Fetching user: {user_id}")
    user = await get_user(db, redis, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserOut)
@limiter.limit("5/minute")
async def update_user_endpoint(user_id: int, user: UserUpdate, request: Request, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    logger.info(f"Updating user: {user_id}")
    updated_user = await update_user(db, redis, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user  # Moved outside the if block

@app.delete("/users/{user_id}")
@limiter.limit("5/minute")
async def delete_user_endpoint(user_id: int, request: Request, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    logger.info(f"Deleting user: {user_id}")  # Fixed to user_id
    success = await delete_user(db, redis, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@app.get("/users/", response_model=list[UserOut])
@limiter.limit("10/minute")
async def list_users_endpoint(request: Request, db: Session = Depends(get_db), page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    logger.info(f"Listing users: page {page}, size {page_size}")
    users = await list_users(db, page, page_size)
    return users

#add Gzip middleware for response compression
app.add_middleware(GzipMiddleware, minimum_size=1000)

#setup rate limit 

limiter= Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

#crud Endpoints
@app.post("/users/", response_model=UserOut)
@limiter.limit("5/minute")
async def create_user_endpoint(user: UserCreate, request: Request, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    try: 
        user_data = await create_user(db, redis,user)
        return user_data
    except Exception as e:
        logger.error(f'Error creating user:{str(e)}') 
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/users/{user_id}", response_model=UserOut)
@limiter.limit("10/minute")  
async def get_user_endpoint(user_id:int, request:Request, db=Depends(get_db),redis=Depends(get_redis)):
    logger.info(f"fetching user:{user_id}")
    user = await get_user(db, redis, user_id)
    if not user:
        raise HTTPException(status_code=404, detail= "User not found")
    return user

@app.put("/users/{user_id}", response_model= UserOut)
@limiter.limit("5/minute")
async def update_user_endpoint(user_id:int, user: UserUpdate, request:Request, db=Depends(get_db),redis=Depends(get_redis)):
    logger.info(f"Updating user:{user_id}")
    updated_user = await update_user(db, redis, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
        return updated_user

@app.delete("/users/{user_id}")        
@limiter.limit("5/minute")
async def delete_user_endpoint(user_id:int, request:Request, db=Depends(get_db),redis=Depends(get_redis)):
    logger.info(f"Deleting user: {user.id}")
    success = await delete_user(db, redis, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return{"message": "User deleted"}

@app.get("/users/", response_model=list[UserOut])
@limiter.limit("10/minute")
async def list_users_endpoint(request: Request, db=Depends(get_db), page: int= Query(1, ge=1),page_size:int=Query(10, ge=1, le=100)):
    logger.info(f"Listing users:page{page}, size{page_size}")
    users = await list_users(db, page, page_size)
    return users



