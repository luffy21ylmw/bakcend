import json,hashlib,time

from django.utils.deprecation import MiddlewareMixin
from django.http.response import JsonResponse,HttpResponse

from api import models

class Myloginauth(MiddlewareMixin):
    def process_request(self, request):
        pass



    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Headers'] = '*'
        return response