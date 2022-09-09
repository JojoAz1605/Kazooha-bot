import io
import discord
import datetime
import requests
import saucenao_api
import imagehash
import re
import os

from saucenao_api import SauceNao
from saucenao_api.errors import LongLimitReachedError, ShortLimitReachedError
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
SAUCENAO_TOKEN = os.getenv("SAUCENAO_TOKEN")
SAUCENAO_TOKEN2 = os.getenv("SAUCENAO_TOKEN2")


async def get_channel_stat(channel: discord.TextChannel) -> tuple[int, dict[str: int]]:
    stats = {}
    messages = await channel.history(limit=None).flatten()
    for message in messages:
        if not message.author.bot:
            name = message.author.name
            if name not in stats:
                stats[name] = 1
            else:
                stats[name] += 1
    return len(messages), stats


def convert_discord_id_to_time(discord_id: int):
    return int((int(bin(discord_id)[:-22], 2) + 1420070400000) / 1000)


def merge_dict(dict1: dict, dict2: dict) -> dict[str: int]:
    res = {}
    for key in dict1:
        if key not in res:
            res[key] = dict1[key]
        else:
            res[key] += dict1[key]
    for key in dict2:
        if key not in res:
            res[key] = dict2[key]
        else:
            res[key] += dict2[key]
    return res


async def download_discord_avatar(user: discord.User) -> None:
    filename = f"img\\avatar\\{user.id}.jpg"
    await user.avatar_url.save(filename)


def log(thing: str) -> None:
    date = datetime.datetime.now().strftime("%H:%M:%S")
    filename = datetime.datetime.now().strftime("%d-%m-%Y")
    ze_log = f"[{date}] - {thing}\n"
    print(f"[LOG] - {ze_log}", end='')
    with open(f"logs/{filename}.txt", 'a', encoding='utf-8') as log_file:
        log_file.write(ze_log)


def get_all_images(link: str) -> list[str]:
    soup = BeautifulSoup(requests.get(link).content, features="html.parser")
    images = []
    for img in soup.findAll('img'):
        images.append(urljoin(link, img.get('src')))

    return images


def get_img_from_link(link: str) -> io.BytesIO:
    return io.BytesIO(requests.get(link).content)


def compare_image(link1: str, link2: str) -> bool:
    hash0 = imagehash.average_hash(Image.open(get_img_from_link(link1)))
    hash1 = imagehash.average_hash(Image.open(get_img_from_link(link2)))
    cutoff = 5  # maximum bits that could be different between the hashes.

    if hash0 - hash1 < cutoff:
        return True
    else:
        return False


def check_if_matching_in_link(base_image: str, link: str) -> bool:
    all_images = get_all_images(link)
    for image_link in all_images:
        if compare_image(base_image, image_link):
            return True
    return False


def get_link_from_message(msg: discord.Message) -> str:
    return re.search("(?P<url>https?://\S+)", msg.content).group("url")


def detect_from_link(link: str) -> saucenao_api.BasicSauce:
    global SAUCENAO_TOKEN, SAUCENAO_TOKEN2
    if link[0] == '<':
        link = link[1:-1]
    try:
        results = SauceNao(SAUCENAO_TOKEN, numres=1).from_url(link)
    except LongLimitReachedError or ShortLimitReachedError:
        results = SauceNao(SAUCENAO_TOKEN2, numres=1).from_url(link)
    log(f"Recherche effectuée, il en reste {results.long_remaining}")
    return results[0]