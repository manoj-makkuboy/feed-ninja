from django.http import HttpResponse, JsonResponse
# Create your views here.
import feedparser
import json
import logging
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views import View
import asyncio
import time
import aiohttp
import os
import async_timeout
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

feed_urls = {
    'FSFTN': 'https://fsftn.org/blog/rss/',
    'norvig': 'http://norvig.com/rss-feed.xml'
}
aggregate_feed_objects = []
logger = logging.getLogger(__name__)

file_save_path = '/home/manoj.mohan/Downloads/feeds/'



@csrf_exempt
def get_title(request):
    json_input = json.loads(request.body)
    recent = json_input['recent']
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

            file_name = file_name_generator_function(url)
            file_full_name = os.path.join(file_save_path, file_name)
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


def load_feed_from_files():
    for url_name in feed_urls.keys():
        full_file_path = file_save_path + url_name
        logging.warning(full_file_path)
        aggregate_feed_objects.append(feedparser.parse(full_file_path))


def update_sources():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Making the global aggaggregate_feed_objects empty.
    global aggregate_feed_objects
    aggregate_feed_objects = []
    loop.run_until_complete(main(loop))

@method_decorator(csrf_exempt, name='dispatch')
class Articles(View):
    def get(self, request):
        json_input = request.GET.get('recent', '')
        input_page_number = request.GET.get('page', '')
        try:
            recent = int(json_input)
        except ValueError:
            recent = None

        result = []

        load_feed_from_files()

        for feed in aggregate_feed_objects:
            for entry in feed['entries'][:recent]:
                result.append({'title': entry['title'],
                               'description': entry['description'],
                               'link': entry['link']})
        result = Paginator(result, 2)
        page = result.page(input_page_number)
        page = page.object_list
        result_json = json.dumps(page, ensure_ascii=False)
        return HttpResponse(page,
                            content_type='application/json; charset=utf-8')

@csrf_exempt
def update_load_feeds(request):
    update_sources()
    return HttpResponse('Done')
