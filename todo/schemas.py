# schemas.py
from ninja import Schema

class TodoSchema(Schema):
    title: str
    description: str
    created_at: str
    completed: bool
    important: bool
