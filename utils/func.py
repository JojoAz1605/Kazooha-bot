import datetime
import time

import interactions
import discord
import os

from utils.functions import log
from utils.database import insert_message


async def detect_message(msg: interactions.Message, client: interactions.Client) -> None:
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    if not msg.author.bot and len(msg.content) != 0:
        await insert_message(msg)
        ze_time = datetime.datetime.now().strftime("%H:%M:%S")

        ze_log = f"[{ze_time}] - {msg.author.username} a dit: {msg.content}\n"
        print(f"[MSG] - {ze_log}", end='')
        await image_log(msg, date, client)


async def image_log(msg: interactions.Message, date: str, client: interactions.Client) -> None:
    guild = await msg.get_guild()
    if len(msg.attachments) != 0:
        try:
            os.makedirs(rf"image_logs/{msg.author.username}/{date}/{guild.name}")
        except FileExistsError:
            pass
        for att in msg.attachments:
            await save_attachment(client, att, rf"image_logs/{msg.author.username}/{date}/{guild.name}/{att.filename}")


async def save_attachment(client: interactions.Client, att: interactions.Attachment, filename: str) -> str:
    att._client = client._http
    att_data = await att.download()
    if not os.path.exists(filename):
        with open(filename, 'wb') as outfile:
            outfile.write(att_data.getbuffer())
    else:
        ze_filename = list(filename)
        del ze_filename[-4:]
        extension = filename[-4:]
        for i in range(1, 101):
            nom_du_fichier = f"{''.join(ze_filename)}_{i}{extension}"
            if not os.path.exists(nom_du_fichier):
                with open(nom_du_fichier, 'wb') as outfile:
                    outfile.write(att_data.getbuffer())
                    return nom_du_fichier


def contain_image(msg: discord.Message) -> bool:
    try:
        return len(msg.embeds[0].image) > 0
    except IndexError:
        return False


async def delete_if_not_noice_image(msg: discord.Message):
    time.sleep(2)
    if msg.guild.id == 950118071425724466 and msg.author.id == 1025308201824026644 and not contain_image(msg):
        log(f"Message supprimé: {msg.content}")
        await msg.delete()
