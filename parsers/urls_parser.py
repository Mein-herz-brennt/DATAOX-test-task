from typing import List, Set
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from decouple import config


class LinksParser:
    main_page_link = config('PAGE_LINK')

    def __init__(self):
        self.car_links: Set[str] = set()

    async def _get_page_text(self, session: ClientSession, link: str) -> str:
        async with session.get(link) as response:
            return await response.text()

    async def _count_of_pages(self, session: ClientSession) -> int:
        page = await self._get_page_text(session, self.main_page_link)
        soup = BeautifulSoup(page, 'lxml')

        tag = soup.find("span", class_="page-item dhide text-c")
        if not tag:
            return 1

        return int(tag.text.split('/')[-1].strip())

    async def _pages_links_builder(self, session: ClientSession) -> List[str]:
        pages_count = await self._count_of_pages(session)
        return [
            f'https://auto.ria.com/uk/car/used/?page={i}'
            for i in range(1, pages_count + 1)
        ]

    async def parse_all_car_links(self) -> List[str]:
        async with ClientSession() as session:
            pages = await self._pages_links_builder(session)

            for page_url in pages:
                page = await self._get_page_text(session, page_url)
                soup = BeautifulSoup(page, 'lxml')

                cars = soup.select("a.m-link-ticket[href]")
                for car in cars:
                    self.car_links.add(car["href"])

        return list(self.car_links)

