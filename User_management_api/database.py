from databases import database
from airedis import Redis, from_url
import json
from models import UserCreate, UserUpdate

#Database and Redis connections

DATABASE_URL ="postgresql://user:password@localhost:5432/userdb"
REDIS_URL ="redis://localhost:6379/0"

database = Database(DATABASE_URL)
redis_client = from_url(REDIS_URL, encoding="utf-8", decode_response=True)

async def get_db():
    async with database as db:
        yield db

async def get_redis():
    yield redis_client

async def create_user(db:Datase, redis:Redis, user:UserCreate):
    query='''
    INSERT INTO users(name, email, password)
    VALUES(:name, :email, :password)
    RETURNING id, name, email '''

    values = {"name": user.name, 'email':user.email, 'password':user.password}
    user_data= await db.fetch_one(query=query, values=values)

    #cache the user
    await redis.set(f"user:{user_data['id']}",json.dumps(user_data),ex=3600)
    return user_data

async def get_user(db: Database, redis:Redis, user_id: int):
    #check cache first
    cached_user = await redis.get(f"user:{user_id}")
    if cached_user:
        return json.loads(cached_user)

    #fetch from database
    query = "SELECT id, name, email FROM users WHERE id = :id"
    user = await db.fetch_one(query=query, values={"id":user_id})
    if user: 
        #cache for 1hr
        await redis.set(f"user:{user_id}",json.dumps(user),ex=3600)
    return user

async def update_user(db: Database, redis:Redis, user_id:int, user:UserUpdate):
    query ='''
    UPDATE users
    SET name = COALESCE(:name, name),
        email = COALESCE(:email, email),
        password = COALESCE(:password, password)
    WHERE id =:id
    RETURNING id, name, email
    '''
    values = {"id": user_id, "name":user.name, "email":user.email, "password":user.password}
    if user_data:
        #update cache
        await redis.set(f"user:{user_id}", json.dumps(user_data), ex=3600)
        return user_data

async def delete_user(db: Database, redis: Redis, user_id:int):
    query = "DELETE FROM users WHERE id =:id"
    result= await db.execute(query=query, values={"id":user_id})
    if result:
        #Remove from cache
        await redis.delete(f"user:{user_id}")
    return result > 0

async def list_users(db: Database, page:int, page_size:int):
    offset = (page -1) * page_size
    query = "SELECT id, name, email FROM users LIMIT: limit OFFSET:offset"
    return await db.fetch_all(query=query, values={"limit":page_size, "offset": offset})




