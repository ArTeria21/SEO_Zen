import aiohttp
import asyncio
from translatepy.translators import YandexTranslate
import json

TRANSLATOR = YandexTranslate()

async def get_the_quote() -> tuple[str, str]:
    async with aiohttp.request(url='https://zenquotes.io/api/random', method='GET') as response:
        quote = await response.text()
    quote_data = json.loads(quote)[0]
    return quote_data['q'], quote_data['a']

def translate(text: str) -> str:
    return TRANSLATOR.translate(text, 'ru').result

async def find_author_in_wikipedia(author: str) -> str:
    author = author.replace(' ', '_')
    async with aiohttp.request(url=f'https://en.wikipedia.org/api/rest_v1/page/summary/{author}', 
                               method='GET') as response:
        data = await response.text()
    data = json.loads(data)
    return data['extract']

async def main():
    quote, author = await get_the_quote()
    translated_quote = translate(quote)
    author_info = await find_author_in_wikipedia(author)
    print(f"Quote: {quote}")
    print(f"Translated Quote: {translated_quote}")
    print(f"Author: {author}")
    print(f"Author Info: {author_info}")

if __name__ == '__main__':
    asyncio.run(main())
