from django.http import HttpResponse, JsonResponse
# Create your views here.
import feedparser
import json
import logging
from django.views.decorators.csrf import csrf_protect, csrf_exempt


logger = logging.getLogger(__name__)


@csrf_exempt
def test_view(request):
    json_input = json.loads(request.body)
    logger.error(json_input['name'], exc_info=1)
    result = feedparser.parse('https://fsftn.org/blog/rss/')
    result = result['entries'][0]
    result_json = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result_json,
                        content_type='application/json; charset=utf-8')
#    return HttpResponse(result_json,
#                        content_type='application/json; charset=utf-8')
