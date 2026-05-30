from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient

from app.models import mongodb
from app.models.site import SiteModel
from app.site_scraper import NaverSiteScraper

from bs4 import BeautifulSoup
import html


def clean_html(raw_text: str) -> str:
    decoded = html.unescape(raw_text)
    return BeautifulSoup(decoded, "html.parser").get_text()


app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # site = SiteModel(
    #     keyword="python",
    #     title="FastAPI Tutorial",
    #     link="https://fastapi.tiangolo.com/",
    #     description="FastAPI 공식 문서 예제",
    # )
    # save_site = await mongodb.engine.save(site)
    # print(save_site.model_dump(), flush=True)
    return templates.TemplateResponse(request, "index.html", {"title": "마크"})


@app.get("/search", response_class=HTMLResponse)
async def read_item(request: Request, q: str):
    keyword = q

    if not keyword:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"message": "검색어를 입력해주세요"},
        )
    naver_site_scraper = NaverSiteScraper()

    sites = await naver_site_scraper.search(keyword, 10)

    site_models = []

    for site in sites:
        print(site)
        site_model = SiteModel(
            keyword=keyword,
            title=clean_html(site["title"]),
            link=site["link"],
            description=clean_html(site.get("description", "")),
        )
        site_models.append(site_model)

    await mongodb.engine.save_all(site_models)
    return templates.TemplateResponse(
        request=request, name="index.html", context={"keyword": q, "sites": site_models}
    )


@app.on_event("startup")
async def on_app_start():
    print("hello server")
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    print("goodbye server")
    mongodb.close()
