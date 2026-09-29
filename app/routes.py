from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.messageSchema import *
from app.database import *
from app.repository.message_repository import *
from app.service.messagesService import *
from app.dependencies import *
import boto3
from botocore.exceptions import ClientError
from uuid import uuid4
from app.service.S3Service import S3BucketService

router = APIRouter(prefix="/messages", tags=["Message"])


aws_access_key_id = '1a31776050b84a7586a2c4a4aee65517'
aws_secret_access_key = 'effbd9b2acdc48b481bfe4abba839f80'


s3 = boto3.client(
    service_name='s3',
    endpoint_url='https://s3.ru-1.storage.selcloud.ru',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    verify=False
)

bucket_name = "dream"


@router.post("/messages/", response_model=MessageResponse)
async def create_message(
    message_in: MessageCreate,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    repository = MessageRepository(session)

    service = MessageService(repository)

    return await service.message_create(
        content=message_in.content,
        sender_id=current_user,
        receiver_id=message_in.receiver_id,
    )


@router.post("/add_attachment/")
async def add_attachment(
    receiver_id: str = Form(),
    file: UploadFile = File(),
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    repository = MessageRepository(session)

    service = S3BucketService(
        bucket_name=bucket_name,
        endpoint="https://s3.ru-1.storage.selcloud.ru",
        access_key=aws_access_key_id,
        secret_key=aws_secret_access_key,
        message=repository,
    )

    result = await service.upload_file_object(
        file=file, user_id=current_user, receiver_id=receiver_id
    )

    image_url = service.generate_file_url(result.image_key)

    return MessageResponse(
        id=result.id,
        sender_id=result.sender_id,
        receiver_id=result.receiver_id,
        content=result.content,
        created_at=result.created_at,
        image_url=image_url,
    )


@router.get("/list-messages/")
async def get_messages(
    recipient_id: str,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    repository = MessageRepository(session)
    service = MessageService(repository)

    s3_service = S3BucketService(
        bucket_name=bucket_name,
        endpoint="https://s3.ru-1.storage.selcloud.ru",
        access_key=aws_access_key_id,
        secret_key=aws_secret_access_key,
        message=repository,
    )
    messages = await service.get_messages(current_user, recipient_id)

    result = []

    for message in messages:
        image_url = None

        if message.image_key:
            image_url = s3_service.generate_file_url(
                message.image_key
            )

        result.append(
            MessageResponse(
                id=message.id,
                sender_id=message.sender_id,
                receiver_id=message.receiver_id,
                content=message.content,
                created_at=message.created_at,
                image_url=image_url,
            )
        )

    return result


@router.get("/get-img")
async def get_img(
    image_key: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    repository = MessageRepository(session)

    service = S3BucketService(
        bucket_name=bucket_name,
        endpoint="https://s3.ru-1.storage.selcloud.ru",
        access_key=aws_access_key_id,
        secret_key=aws_secret_access_key,
        message=repository,
    )

    url = await service.generate_file_url(image_key)
    return url

@router.get("/dialogs/")
async def all_dialogs(
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):

    repository = MessageRepository(session)
    service = MessageService(repository)

    return await service.get_all_msg(sender_id=current_user)


@router.patch("/{message_id}/", response_model=MessageResponse)
async def upd_messages(
    updated_content: MessageCreate,
    message_id: str,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):

    repository = MessageRepository(session)
    service = MessageService(repository)

    return await service.update_messages(
        sender_id=current_user,
        message_id=message_id,
        receiver_id=updated_content.receiver_id,
        content=updated_content.content,
    )


@router.delete("/delete-message/", response_model=MessageDeleteResponse)
async def dlt_message(
    receiver_id: str,
    message_id: str,
    current_user=Depends(get_current_user),
    session: AssertionError = Depends(db_helper.session_dependency),
):

    repository = MessageRepository(session)
    service = MessageService(repository)

    return await service.delete_messages(
        sender_id=current_user, message_id=message_id, receiver_id=receiver_id
    )


@router.delete("/delete-chat-messages/")
async def dlt_chat_messages(
    receiver_id: str,
    current_user=Depends(get_current_user),
    session: AssertionError = Depends(db_helper.session_dependency),
):
    repository = MessageRepository(session)
    service = MessageService(repository)

    return await service.delete_chat_message(
        sender_id=current_user, receiver_id=receiver_id
    )
