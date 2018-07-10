import json

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def bad_request(request):
    return HttpResponse(json.dumps({
        'status': 400,
        'msg': 'bad request'
    }), content_type='application/json')


@csrf_exempt
def page_not_found(request):
    return HttpResponse(json.dumps({
        'status': 404,
        'msg': 'not found'
    }), content_type='application/json')


@csrf_exempt
def server_error(request):
    return HttpResponse(json.dumps({
        'status': 500,
        'msg': 'server error'
    }), content_type='application/json')

