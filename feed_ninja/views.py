from django.http import HttpResponse
# Create your views here.
import feedparser
import json


def test_view(request):
    result = feedparser.parse('https://fsftn.org/blog/rss/')
    result = result['entries'][0]
    result_json = json.dumps(result)
    print (result_json)
    return HttpResponse(result_json)
