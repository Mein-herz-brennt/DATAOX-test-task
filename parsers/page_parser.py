import re
from aiohttp import ClientSession
from bs4 import BeautifulSoup


class CarPageParser:
    def __init__(self, page_link: str):
        self.page_link = page_link
        self.page_text: str | None = None
        self.soup: BeautifulSoup | None = None
        self.car_info = {
            'url': self.page_link,
            'title': None,
            'price_usd': None,
            'odometer': None,
            'username': None,
            'phone_number': None,
            'image_url': None,
            'images_count': None,
            'car_number': None,
            'car_vin': None,
        }

    async def get_page_text(self) -> str:
        async with ClientSession() as session:
            async with session.get(self.page_link) as response:
                page_text = await response.text()
                self.page_text = page_text
        return self.page_text

    async def get_soup(self) -> BeautifulSoup:
        self.soup = BeautifulSoup(self.page_text, 'lxml')
        return self.soup

    @staticmethod
    async def _convert_thousands(text: str) -> int:
        if not text: return 0
        # Очищуємо від усього, крім цифр (95 тис -> 95000)
        digits = re.sub(r'\D', '', text)
        if 'тис.' in text:
            return int(digits) * 1000
        return int(digits) if digits else 0

    async def _set_title(self):
        tag = self.soup.find('h1', class_='common-text ws-pre-wrap titleL')
        self.car_info['title'] = tag.text.strip() if tag else None

    async def _set_price_usd(self):
        tag = self.soup.select_one('#basicInfoPrice strong')
        if tag:
            price = re.sub(r'\D', '', tag.text)
            self.car_info['price_usd'] = int(price) if price else None

    async def _set_odometer(self):
        tag = self.soup.select_one('#basicInfoTableMainInfo0 span, #basicInfoTableMainInfo0')
        if tag:
            self.car_info['odometer'] = await self._convert_thousands(tag.text)

    async def _set_username(self):
        match = re.search(r'"userName":"([^"]+)"', self.page_text)
        if match:
            self.car_info['username'] = match.group(1)

    async def _set_phone_number(self):
        match = re.search(r'"phoneId":"(\d+)"', self.page_text)
        if match:
            self.car_info['phone_number'] = int("38" + match.group(1))

    async def _set_image_url(self):
        tag = self.soup.find('meta', property='og:image')
        if tag:
            self.car_info['image_url'] = tag.get('content')
        else:
            img_container = self.soup.find('div', class_='photobox')
            if img_container and img_container.find('img'):
                self.car_info['image_url'] = img_container.find('img').get('src')

    async def _set_images_count(self):
        tag = self.soup.find('div', class_='visible photo-slider').find("span", class_='common-badge alpha medium')
        count = tag.text.split('з')[1]
        self.car_info['images_count'] = int(count) if count else 0

    async def _set_car_number(self):
        tag = self.soup.find('div', class_='car-number ua').find('span')
        if tag:
            self.car_info['car_number'] = tag.text.strip()

    async def _set_car_vin(self):
        tag = self.soup.find('div', id='badgesVinGrid').find('span', id='badgesVin')
        self.car_info['car_vin'] = tag.text.strip() if tag else None

    async def parse_all(self):
        if not self.page_text:
            await self.get_page_text()
        if not self.soup:
            await self.get_soup()

        # Безпечний виклик усіх методів
        methods = [
            self._set_title, self._set_price_usd, self._set_odometer,
            self._set_username, self._set_phone_number, self._set_image_url,
            self._set_images_count, self._set_car_number, self._set_car_vin
        ]

        for method in methods:
            try:
                await method()
            except Exception:
                continue
        print(self.car_info)
        return self.car_info