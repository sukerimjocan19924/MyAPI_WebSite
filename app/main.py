from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient

from app.models import mongodb
from app.models.site import SiteModel

app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    site = SiteModel(
        keyword="python",
        title="FastAPI Tutorial",
        link="https://fastapi.tiangolo.com/",
        description="FastAPI 공식 문서 예제",
    )
    save_site = await mongodb.engine.save(site)
    print(save_site.model_dump(), flush=True)
    return templates.TemplateResponse(request, "index.html", {"title": "마크"})


@app.get("/search", response_class=HTMLResponse)
async def read_item(request: Request, q: str):
    return templates.TemplateResponse(request, "index.html", {"keyword": q})


@app.on_event("startup")
async def on_app_start():
    print("hello server")
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    print("goodbye server")
    mongodb.close()
