from django.http import HttpResponse, JsonResponse
# Create your views here.
import feedparser
import json
import logging
from django.views.decorators.csrf import csrf_protect, csrf_exempt

feed_urls = {
    'FSFTN': 'https://fsftn.org/blog/rss/',
    'norvig': 'http://norvig.com/rss-feed.xml'
}
aggregate_feed_objects= []
logger = logging.getLogger(__name__)


@csrf_exempt
def get_title(request):
    json_input = json.loads(request.body)
    recent = json_input['recent']
    update_sources()
    result = []

    for feed in aggregate_feed_objects:
        for entry in feed['entries']:
            result.append(entry['title'])

    result_json = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result_json,
                        content_type='application/json; charset=utf-8')


def update_sources():

    for feed_url in feed_urls.values():
        aggregate_feed_objects.append(feedparser.parse(feed_url))




