from django.http import HttpResponse, JsonResponse
# Create your views here.
import feedparser
import json
import logging
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import asyncio
import time


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
#    time.sleep(2)
    result = []

    for feed in aggregate_feed_objects:
        for entry in feed['entries'][:recent]:
            result.append(entry['title'])

    result_json = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result_json,
                        content_type='application/json; charset=utf-8')

async def make_task(url):
    logger.error("start",url)
    aggregate_feed_objects.append(await my_coroutine(url))
    logger.error("stop",url)

async def my_coroutine(url):
#    await asyncio.sleep(1) #asyncio.coroutine(feedparser.parse(url))
    return  feedparser.parse(url)
def update_sources():

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    global aggregate_feed_objects
    aggregate_feed_objects = []
    tasks = [asyncio.ensure_future(make_task('https://fsftn.org/blog/rss/')),
             asyncio.ensure_future(make_task('http://norvig.com/rss-feed.xml'))]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)
#    loop.close()
