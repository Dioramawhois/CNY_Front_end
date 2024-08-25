from utils.logger import logger
from telethon.errors import (
    UsernameInvalidError, UserNotMutualContactError, ChannelPrivateError, ChannelInvalidError,
    InviteHashExpiredError, InviteHashInvalidError, FloodWaitError, UserAlreadyParticipantError
)
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
import asyncio

class ChatManager:
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client

    async def send_message(self, identifier, message):
        for attempt in range(3):  # Максимум 3 попытки
            try:
                entity = await self.telegram_client.get_input_entity(identifier)
                await self.telegram_client.send_message(entity, message)
                logger.info(f"Message sent to {identifier}: {message}")
                return True
            except Exception as e:
                logger.error(f"Failed to send message to {identifier} on attempt {attempt + 1}: {e}")
                await asyncio.sleep(2)  # Небольшая задержка перед следующей попыткой
        logger.error(f"Max retries reached for {identifier}. Skipping...")
        return False

    async def join_channel(self, channel_link):
        try:
            if 'joinchat' in channel_link:
                invite_hash = channel_link.split('/')[-1]
                await self.telegram_client(ImportChatInviteRequest(invite_hash))
            else:
                channel_entity = await self.telegram_client.get_entity(channel_link)
                await self.telegram_client(JoinChannelRequest(channel_entity))
            logger.info(f"Joined channel: {channel_link}")
            return True
        except Exception as e:
            logger.error(f"Failed to join channel {channel_link}: {e}")
            return False
