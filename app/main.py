from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
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

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
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

    naver_site_scraper = NaverSiteScraper()

    sites = await naver_site_scraper.search(keyword, 10)

    favorite_sites = await mongodb.engine.find(SiteModel, SiteModel.is_favorite == True)

    favorite_links = [site.link for site in favorite_sites]
    site_models = []

    for site in sites:
        print(site)
        site_model = SiteModel(
            keyword=keyword,
            title=clean_html(site["title"]),
            link=site["link"],
            description=clean_html(site.get("description", "")),
        )

        if site_model.link in favorite_links:
            site_model.is_favorite = True

        site_models.append(site_model)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"keyword": q, "sites": site_models, "next_url": f"/search?q={q}"},
    )


@app.post("/favorites")
async def toggle_favorite(
    request: Request,
    keyword: str = Form(...),
    link: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    next_url: str = Form("/"),
):
    favorite_site = await mongodb.engine.find_one(
        SiteModel,
        (SiteModel.keyword == keyword)
        & (SiteModel.link == link)
        & (SiteModel.is_favorite == True),
    )
    if favorite_site:
        await mongodb.engine.delete(favorite_site)
    else:
        site = SiteModel(
            keyword=keyword,
            link=link,
            title=title,
            description=description,
            is_favorite=True,
        )
        await mongodb.engine.save(site)

    return RedirectResponse(url=next_url, status_code=303)


@app.get("/favorites", response_class=HTMLResponse)
async def favorites(request: Request):
    sites = await mongodb.engine.find(SiteModel, SiteModel.is_favorite == True)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "즐겨찾기 목록", "sites": sites, "next_url": "/favorites"},
    )


@app.on_event("startup")
async def on_app_start():
    print("hello server")
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    print("goodbye server")
    mongodb.close()
