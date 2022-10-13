import sys
import os
import yaml
from loguru import logger
from pathlib import Path
import ezkfg as ez


def init_log():
    """Initialize loguru log information"""
    event_logger_format = (
        "<g>{time:YYYY-MM-DD HH:mm:ss}</g> | "
        "<lvl>{level}</lvl> - "
        # "<c><u>{name}</u></c> | "
        "{message}"
    )
    logger.remove()
    logger.add(
        sink=sys.stdout,
        colorize=True,
        level="DEBUG",
        format=event_logger_format,
        diagnose=False,
    )

    return logger


def init_path(cfg):
    cfg["cache_path"] = Path("./../cached")
    cfg["cache_path"].mkdir(parents=True, exist_ok=True)

    return cfg


def init(cfg_path: str):
    cfg = ez.Config().load(cfg_path)
    cfg = init_path(cfg)
    init_log()
    return cfg


def get_item_info(item, key):
    try:
        return item[key]
    except KeyError:
        return ""


def get_dblp_items(dblp_data):
    try:
        items = dblp_data["result"]["hits"]["hit"]
    except KeyError:
        items = []

    # item{'author', 'title', 'venue', 'year', 'type', 'access', 'key', 'doi', 'ee', 'url'}
    res_items = []

    for item in items:
        res_item = {}
        # format author
        authors = get_item_info(item["info"], "authors")
        authors = [author["text"] for author in authors["author"]]

        logger.info(f"authors: {authors}")

        res_item["author"] = ", ".join(authors)
        needed_keys = [
            "title",
            "venue",
            "year",
            "type",
            "access",
            "key",
            "doi",
            "ee",
            "url",
        ]
        for key in needed_keys:
            res_item[key] = get_item_info(item["info"], key)

        res_items.append(res_item)

    return res_items


def get_msg(items, topic):
    msg = f"## {topic}\n\n"
    msg += f"""Explore {len(items)} new papers about {topic} on dblp!!!\n\n"""

    for item in items:
        msg += f"[{item['title']}]({item['url']})\n"
        msg += f"- Authors: {item['author']}\n"
        msg += f"- Venue: {item['venue']}\n"
        msg += f"- Year: {item['year']}\n"

    return msg
