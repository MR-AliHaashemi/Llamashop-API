from sanic import Sanic
from sanic.response import file
from asyncio import get_event_loop
from .tasks import FortiteAPI

app = Sanic(__name__)


@app.route('/itemshop')
async def itemshop(request):
    """returns the itemsho data"""
    return await file("./contents/data/itemshop.json")


@app.route('/news/<gamemode>')
async def news_gamemode(request, gamemode):
    """
    returns the news data based on game mode

    :gamemode -> stw / br / creative
    """
    if gamemode == "br":
        return await file(f"./contents/data/brnews.json")
    elif gamemode == "creative":
        return await file(f"./contents/data/creativenews.json")
    elif gamemode == "stw":
        return await file(f"./contents/data/stwnews.json")


@app.route('/cdn/<filename>')
async def cdn_files(request, filename):
    """returns a file!"""
    return await file(f"./contents/{filename}")


if __name__ == "__main__":
    loop = get_event_loop()

    loop.create_task(FortiteAPI().track_itemshop())
    loop.create_task(FortiteAPI().track_news())
    loop.create_task(
        app.create_server(return_asyncio_server=True, access_log=False)
    )

    loop.run_forever()
