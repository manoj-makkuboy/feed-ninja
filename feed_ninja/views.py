from django.http import HttpResponse, JsonResponse
# Create your views here.
import feedparser
import json
import logging
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import asyncio
import time
import aiohttp
import os
import async_timeout

feed_urls = {
    'FSFTN': 'https://fsftn.org/blog/rss/',
    'norvig': 'http://norvig.com/rss-feed.xml'
}
aggregate_feed_objects = []
logger = logging.getLogger(__name__)




@csrf_exempt
def get_title(request):
    json_input = json.loads(request.body)
    recent = json_input['recent']
    update_sources()
    result = []

    for feed in aggregate_feed_objects:
        for entry in feed['entries'][:recent]:
            result.append(entry['title'])

    result_json = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result_json,
                        content_type='application/json; charset=utf-8')


def file_name_generator_function(url):
    for key, value in feed_urls.items():
        if value == url:
            return key


async def download_coroutine(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            save_path = '/home/manoj.mohan/Downloads/'

            file_name = file_name_generator_function(url)

            file_full_name = os.path.join(save_path, file_name)
            with open(file_full_name, 'wb+') as f_handle:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f_handle.write(chunk)
            return await response.release()


async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [download_coroutine(session, url) for url in feed_urls.values()]
        await asyncio.gather(*tasks)

def update_sources():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Making the global aggaggregate_feed_objects empty.
    global aggregate_feed_objects
    aggregate_feed_objects = []
    loop.run_until_complete(main(loop))
