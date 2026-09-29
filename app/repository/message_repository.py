from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, delete
from app.models.message import *
from app.schemas.messageSchema import *
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _get_message_query(self): pass

    async def create(self, 
                    content: str, 
                    sender_id: str,
                    receiver_id: str) -> Message:
        
        message = Message(
            content = content,
            sender_id = sender_id,
            receiver_id = receiver_id
        )
        try:
            self.session.add(message)

            await self.session.commit()
            await self.session.refresh(message)

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")

        return message
    
    async def add_attachment(self, 
                             sender_id: str,
                             receiver_id: str,
                             attachment: str,
                             ):
        message = Message(
            sender_id = sender_id,
            receiver_id = receiver_id,
            image_key = attachment,
        )

        try:
            self.session.add(message)

            await self.session.commit()
            await self.session.refresh(message)

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")

        return message


    #Изменить сообщение(Доделать изменять сообщение может только человек написавший его)
    async def update_message(self, 
                        sender_id: str,
                        message_id: str,
                        receiver_id: str, 
                        content: str):
        stmt = select(Message).where(
            Message.sender_id == sender_id,
            Message.receiver_id == receiver_id,
            Message.id == message_id,
        )

        result = await self.session.execute(stmt)
        message = result.scalar_one_or_none()

        if message is None:
           raise HTTPException(status_code=404, detail="Not found")

        message.content = content
        message.created_at = datetime.now(timezone(timedelta(hours=3)))

    
        await self.session.commit()
        await self.session.refresh(message)

        return message



    # Удалить сообщение для всех.
    async def delete_messages(self,
                              sender_id: str,
                              message_id: str,
                              receiver_id: str):

        #Нахожу сообщение 
        stmt = select(Message).where(
            Message.sender_id == sender_id,
            Message.receiver_id == receiver_id,
            Message.id == message_id,
        )

        result = await self.session.execute(stmt)
        message = result.scalar_one_or_none()

        if message is None:
            raise HTTPException(status_code=404, detail="Not found")

        #Удаляю выбранное сообщение 
        await self.session.delete(message)
        await self.session.commit()

        return message


    #Удалить всю историю чата
    async def delete_chat_messages(self,
                              sender_id: str,
                              receiver_id: str):
        stmt = (
            delete(Message)
            .where(
                or_(
                    and_(
                        Message.sender_id == sender_id,
                        Message.receiver_id == receiver_id,
                    ),
                    and_(
                        Message.sender_id == receiver_id,
                        Message.receiver_id == sender_id,
                    ),
                    )
            )
            .returning(Message)
            )

        result = await self.session.execute(stmt)
        messages = result.scalars().all()

        await self.session.commit()

        return messages

    
    async def get_message(self,
                          sender_id: str,
                          receiver_id: str):
        stmt = select(Message).where(
        or_(
            and_(
                Message.sender_id == sender_id,
                Message.receiver_id == receiver_id,
            ),
            and_(
                Message.sender_id == receiver_id,
                Message.receiver_id == sender_id,
            ),
        )
        ).order_by(Message.created_at).limit(15)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    
    async def gel_all_messages(self, sender_id: str):
        stmt = select(Message).where(
            Message.sender_id == sender_id
        ).limit(3).order_by(Message.created_at)

        result = await self.session.execute(stmt)
        return result.scalars().all()
        

        

        
        

        
    
    