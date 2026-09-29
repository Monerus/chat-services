from datetime import datetime

from pydantic import BaseModel, ConfigDict

# МБ на удаление
class MessageCreate(BaseModel):
    content: str
    receiver_id: str

class MessageResponse(BaseModel):
    id: str
    content: str | None = None
    sender_id: str
    receiver_id: str
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    image_url: str | None = None
    # content_type: str | None = None

class MessageUpdate(BaseModel):
    content: str

class MessageDeleteResponse(BaseModel):
    success: str = "Успешно"