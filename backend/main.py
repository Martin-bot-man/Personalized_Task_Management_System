from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3
from typing  import List

app = FastAPI()

class Task(BaseModel):
    id :int | None = None
    title:str
    description: str | None = None
    status: str = "pending"
    created_at:datetime | None =datetime.now()

def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS tasks(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       title TEXT NOT NULL,
       description TEXT,
       status TEXT NOT NULL,
       created_at TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()
init_db()    
        
#crud operations

@app.get("/")
def home():
    return{"message": "Welcome to the Task Management API!"}


@app.post("/tasks/", response_model= Task)
async def create_task(task: Task):
    conn = sqlite3.connect ("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks( title, description, status, created_at) VALUES(?, ?, ?, ?)",
        (task.title, task.description, task.status, task.created_at.isoformat())

    )
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {**task.dict(), "id": task_id}

@app.get("/tasks/", response_model = List[Task]) 
async def get_tasks():
    conn = sqlite3.connect ("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, status, created_at FROM tasks ")
    tasks = [
        Task(id = row[0], title=row[1], description=row[2], status=row[3], created_at=row[4])
        for row in cursor.fetchall()
    ]
    conn.close()
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    conn = sqlite3.connect ("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, status, created_at FROM tasks WHERE id = ? ",(task_id,))    
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task (id=row[0], title=row[1], description=row[2], status=row[3], created_at=row[4])

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
     conn= sqlite3.connect("tasks.db")
     cursor = conn.cursor()
     cursor.execute(
         "UPDATE tasks SET title=?, description=?, status=?, created_at=? WHERE id=?",
         (task.title, task.description, task.status, task.created_at.isoformat(), task_id)
)
     conn.commit()
     conn.close()
     if cursor.rowcount == 0:
         raise HTTPException(status_code=404, detail= "Task not found")
     return {**task.dict(),"id": task_id}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id:int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id =?", (task_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount ==0 :
        raise HTTPException(status_code =404, detail="Task not found")
    return{"detail":"Task deleted"}
     
         

