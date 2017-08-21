from django.http import HttpResponse
import feedparser
import json
from django.views.decorators.csrf import csrf_exempt
#from django.views import View
import asyncio
import aiohttp
import os
import async_timeout
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
import aiofiles
from rest_framework import permissions
from rest_framework.views import APIView


feed_urls = {
    'FSFTN': 'https://fsftn.org/blog/rss/',
    'norvig': 'http://norvig.com/rss-feed.xml'
}
aggregate_feed_objects = []

file_save_path = '/home/manoj.mohan/Downloads/feeds/'


def file_name_generator(url):
    ''' Returns the key of global feed_urls for the given value of dictionary'''
    for key, value in feed_urls.items():
        if value == url:
            return key


async def download_feeds(session, url):
    ''' Coroutine which downloads feeds from url given in the argument'''
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            file_name = file_name_generator(url)
            file_full_name = os.path.join(file_save_path, file_name)
            async with aiofiles.open(file_full_name, 'wb+') as f_handle:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    await f_handle.write(chunk)
            return await response.release()


async def main_async_call_to_coroutines(loop):
    ''' Coroutine which sets the task inside the event loop '''
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [download_feeds(session, url) for url in feed_urls.values()]
        await asyncio.gather(*tasks)


def load_feed_from_files():
    ''' reads the feed files from the local filesystem and loads it to the
    global variable aggregate_feed_objects '''
    for url_name in feed_urls.keys():
        full_file_path = file_save_path + url_name
        aggregate_feed_objects.append(feedparser.parse(full_file_path))


def update_sources():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Making the global aggaggregate_feed_objects empty.
    global aggregate_feed_objects
    aggregate_feed_objects = []
    loop.run_until_complete(main_async_call_to_coroutines(loop))


#@method_decorator(csrf_exempt, name='dispatch')
class Articles(APIView):
    permission_classes = (permissions.IsAuthenticated,)
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

        try:
            page = result.page(input_page_number)
        except PageNotAnInteger:
            return HttpResponse('Please pass an int argument for page. eg. ../articles?page=1')

        page = page.object_list
        result_json = json.dumps(page, ensure_ascii=False)
        return HttpResponse(result_json,
                            content_type='application/json; charset=utf-8')




@csrf_exempt
def update_load_feeds(request):
    ''' Function Based Views which is invoked when /feed_ninja/update_load is
    called '''
    update_sources()
    return HttpResponse('Done')
