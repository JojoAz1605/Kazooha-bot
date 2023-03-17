import os
import mysql.connector
import interactions
import re

from dotenv import load_dotenv
from utils.functions import convert_discord_id_to_time

load_dotenv()
HOST = os.getenv("DATABASE_HOST")
USER = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE = os.getenv("DATABASE_NAME")

emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "'"
                           "]+", flags=re.UNICODE)


def open_connection() -> mysql.connector.connection.MySQLConnection:
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )


async def insert_message(msg: interactions.Message) -> None:
    db = open_connection()
    msg_guild = await msg.get_guild()
    guild_name = emoji_pattern.sub(r'', msg_guild.name)
    msg_channel = await msg.get_channel()
    channel_name = emoji_pattern.sub(r'', msg_channel.name)
    author_name = emoji_pattern.sub(r'', msg.author.username)
    msg_content = emoji_pattern.sub(r'', msg.content)
    cursor = db.cursor()
    print(msg.timestamp)
    cursor.execute(f"INSERT INTO Kazooha.Messages (id, guildId, guildName, channelId, channelName, authorId, authorName, sentTime, content) VALUE ('{msg.id}', '{msg.guild_id}', '{guild_name}', '{msg.channel_id}', '{channel_name}', '{msg.author.id}', '{author_name}', CURRENT_TIMESTAMP, '{msg_content}');")
    db.commit()
    cursor.close()
    db.close()