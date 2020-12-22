import os
import json


async def save_itemshop_json(raw_data: dict):
    """
    Save json file with collected data from main-API
    It has some difference from the main-API

    : mode: str -> game mode of data [brnews, creativenews, stwnews]
    : raw_data: dict -> raw collected content from the main API
    """
    # News content type
    content = {
        "status": 200,
        "hash": "",
        "images": [],
        "content": {
            "featured": [],
            "daily": []
        },
    }

    # Add images
    for design in os.listdir("./contents"):
        if design.endswith(f"itemshop.png"):
            content["images"].append(f"./contents/{design}")

    # Add raw data from fortnite-api to ["contents"]
    content["content"]["featured"] = raw_data["featured"]["entries"]
    content["content"]["daily"] = raw_data["daily"]["entries"]

    # Add hash code of the content
    content["hash"] = hash(str(content))

    # Save the new data
    with open(f"contents/data/itemshop.json", "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4)


async def update_mreged_news():
    """
    Updates the main news file to decrease the number of requests
    It collects all saved news files, then merge them into one file
    """
    content = {
        "status": 200,
        "hash": "",
        "brnews": {},
        "creativenews": {},
        "stwnews": {}
    }

    # Add all game modes data to the content variable
    with open("./contents/data/brnews.json", "r", encoding="utf-8") as f:
        content["brnews"] = json.load(f)
    with open("./contents/data/creativenews.json", "r", encoding="utf-8") as f:
        content["creativenews"] = json.load(f)
    with open("./contents/data/stwnews.json", "r", encoding="utf-8") as f:
        content["stwnews"] = json.load(f)

    # Add hash code of the content
    content["hash"] = hash(str(content))

    # Save the new data
    with open("./contents/data/news.json", "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4)


async def save_news_json(mode: str, raw_data: dict) -> dict:
    """
    Save json file with collected data from main-API
    It has some difference from the main-API

    : mode: str -> game mode of data [brnews, creativenews, stwnews]
    : raw_data: dict -> raw collected content from the main API
    """
    # News content type
    content = {
        "status": 200,
        "hash": "",
        "video": "",
        "images": [],
        "content": [],
    }

    # Add API-MADE video
    content["video"] = raw_data["image"]

    # Add images
    for design in os.listdir("./contents"):
        if design.endswith(f"{mode}.png"):
            content["images"].append(f"./contents/{design}")

    # Add News tabs
    if mode == "stwnews":
        data = raw_data["messages"]
        for news in data:
            content["content"].append(
                {
                    "adspace": news["adspace"],
                    "title": news["title"],
                    "image": news["image"]
                }
            )
    else:
        data = raw_data["motds"]
        for news in data:
            title = news["title"] if news['tabTitle'] is None else news['tabTitle']
            content["content"].append(
                {
                    "id": news["id"],
                    "title": title,
                    "image": news["image"]
                }
            )

    # Add hash code of the content
    content["hash"] = hash(str(content))

    # Save the new data
    with open(f"contents/data/{mode}.json", "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4)

    await update_mreged_news()
