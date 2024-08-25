from utils.logger import logger
from telethon.errors import (
    UserPrivacyRestrictedError, PeerFloodError, FloodWaitError, 
    ChannelPrivateError, ChannelInvalidError, InviteHashExpiredError, 
    InviteHashInvalidError, FloodWaitError, UserAlreadyParticipantError,
    RPCError
)
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
import random
import asyncio

class ChatManager:
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client

    async def send_message(self, identifier, message):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                input_entity = await self.telegram_client.get_input_entity(identifier)

                # Если это канал, проверяем подписку и подписываемся при необходимости
                if input_entity.__class__.__name__ in ['Channel', 'ChannelFull', 'Chat']:
                    logger.info(f"Identified recipient {identifier} as a chat.")
                    if not await self.is_subscribed(identifier):
                        logger.info(f"Not subscribed to channel {identifier}. Attempting to join.")
                        await self.join_channel(identifier)
                
                # Отправляем сообщение
                await self.telegram_client.send_message(input_entity, message)
                logger.info(f"Message sent to {identifier}: {message}")
                return  # Сообщение успешно отправлено, выходим из функции

            except FloodWaitError as e:
                logger.warning(f"Flood wait error: Waiting for {e.seconds} seconds before retrying.")
                await asyncio.sleep(e.seconds)
            except PeerFloodError:
                logger.warning("Peer flood error: Too many requests. Waiting before retrying.")
                await asyncio.sleep(random.randint(60, 120))
            except (ChannelPrivateError, ChannelInvalidError, UserPrivacyRestrictedError) as e:
                logger.error(f"Failed to send message to {identifier}: {e}")
                break  # Эти ошибки не требуют повторных попыток
            except Exception as e:
                logger.error(f"Failed to send message to {identifier} on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"Max retries reached for {identifier}. Skipping...")
                else:
                    await asyncio.sleep(random.randint(5, 10))  # Рандомная задержка перед повторной попыткой

    async def is_subscribed(self, identifier):
        try:
            channel = await self.telegram_client.get_entity(identifier)
            return not channel.left
        except (ChannelPrivateError, ChannelInvalidError, RPCError) as e:
            logger.error(f"Failed to check subscription for {identifier}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while checking subscription: {e}")
            return False

    async def join_channel(self, identifier):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if 'joinchat' in identifier:
                    invite_hash = identifier.split('/')[-1]
                    await self.telegram_client(ImportChatInviteRequest(invite_hash))
                else:
                    channel_entity = await self.telegram_client.get_entity(identifier)
                    await self.telegram_client(JoinChannelRequest(channel_entity))
                logger.info(f"Successfully joined channel {identifier}")
                return True  # Успешно подписались, выходим из функции

            except FloodWaitError as e:
                logger.warning(f"Flood wait error while joining channel: Waiting for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
            except UserAlreadyParticipantError:
                logger.info(f"Already a participant in the channel: {identifier}")
                return True
            except (InviteHashInvalidError, InviteHashExpiredError):
                logger.error(f"Invalid or expired invite link: {identifier}")
                break  # Эти ошибки не требуют повторных попыток
            except Exception as e:
                logger.error(f"Failed to join channel {identifier} on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"Max retries reached for joining {identifier}. Skipping...")
                else:
                    await asyncio.sleep(random.randint(5, 10))  # Рандомная задержка перед повторной попыткой

        return False  # Не удалось подписаться после всех попыток
