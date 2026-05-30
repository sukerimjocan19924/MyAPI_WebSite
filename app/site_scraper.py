import asyncio
import aiohttp
from app.config import get_secret


class NaverSiteScraper:
    NAVER_API_SITE = "https://openapi.naver.com/v1/search/webkr"
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["items"]

    def unit_url(self, keyword, start):
        return {
            "url": f"{self.NAVER_API_SITE}?query={keyword}&display=10&start={start}",
            "headers": {
                "X-Naver-Client-Id": self.NAVER_API_ID,
                "X-Naver-Client-Secret": self.NAVER_API_SECRET,
            },
        }

    async def search(self, keyword, total_page):
        apis = [self.unit_url(keyword, 1 + i * 10) for i in range(total_page)]

        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[
                    NaverSiteScraper.fetch(session, api["url"], api["headers"])
                    for api in apis
                ]
            )
            result = []

            for data in all_data:
                if data is not None:
                    for site in data:
                        result.append(site)

            return result

    def run(self, keyword, total_page):
        return asyncio.run(self.search(keyword, total_page))


if __name__ == "__main__":
    scraper = NaverSiteScraper()
    print(scraper.run("파이썬", 3))
