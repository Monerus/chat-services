from fastapi import HTTPException, Depends 
from app.repository.message_repository import *
from app.schemas.messageSchema import *
from app.service.S3Service import S3BucketService

class MessageNotFoundError(Exception):
    pass

class MessageService:

    def __init__(self, message: MessageRepository):
        self.message = message

    async def message_create(self, 
                            content: str, 
                            sender_id: str,
                            receiver_id: str):

        return await self.message.create(
            content,
            sender_id,
            receiver_id
        )

    async def update_messages(self, 
                        sender_id: str,
                        message_id: str,
                        receiver_id: str,
                        content: str):
        result = await self.message.update_message(
            sender_id = sender_id, 
            message_id = message_id, 
            receiver_id = receiver_id, 
            content = content)

        if result is None: 
            raise MessageNotFoundError()

        return result

    async def delete_messages(self,
                              sender_id: str,
                              message_id: str,
                              receiver_id: str): 
        result = await self.message.delete_messages(
            sender_id=sender_id,
            message_id=message_id,
            receiver_id=receiver_id
        )

        if result is None: 
            raise MessageNotFoundError()

        return result

    async def delete_chat_message(self,
                                   sender_id: str,
                                   receiver_id: str):
        await self.message.delete_chat_messages(sender_id=sender_id,
                                                receiver_id=receiver_id)
        return {
            "Sussess: ": "Успешно удалено"
        }
#
    async def get_messages(self, sender_id: str, receiver_id: str) -> list[Message]:

        result = await self.message.get_message(sender_id, receiver_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_200_OK, detail="Напиши привет!)"
            )

        return result
#
    async def get_all_msg(self, sender_id: str) -> list[Message]:

        result = await self.message.gel_all_messages(sender_id=sender_id)

        if not result:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                        detail="Напиши привет!)")

        return result
