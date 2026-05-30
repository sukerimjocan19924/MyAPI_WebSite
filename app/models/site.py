from odmantic import Model
from pydantic import ConfigDict


class SiteModel(Model):
    keyword: str
    title: str
    link: str
    description: str

    model_config = {"collection": "sites"}
