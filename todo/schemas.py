from ninja import Schema
from datetime import datetime

class TodoSchema(Schema):
    title: str
    description: str
    created_at: datetime  # datetime으로 변경
    completed: bool
    important: bool

    class Config:
        # Pydantic의 `datetime`을 ISO 8601 형식의 문자열로 변환
        json_encoders = {
            datetime: lambda v: v.isoformat()  # datetime 객체를 ISO 8601 형식으로 변환
        }
