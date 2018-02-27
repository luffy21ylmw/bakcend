import json
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework import views
import rest_framework.parsers

class LoginView(views.APIView):
    def get(self,request,*args,**kwargs):

        ret = {
            'code':1000,
            'data':'老男孩'
        }
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response

    def post(self,request,*args,**kwargs):
        print(json.loads(request.body))
        ret = {
            'code':1000,
            'username':'老男孩',
            'token':'71ksdf7913knaksdasd7',
        }
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response

    def options(self, request, *args, **kwargs):
        # self.set_header('Access-Control-Allow-Origin', "http://www.xxx.com")
        # self.set_header('Access-Control-Allow-Headers', "k1,k2")
        # self.set_header('Access-Control-Allow-Methods', "PUT,DELETE")
        # self.set_header('Access-Control-Max-Age', 10)
        print(request.POST)
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'
        # response['Access-Control-Allow-Methods'] = 'PUT'
        return response


class CoursesView(views.APIView):

    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            ret = {
                'title':"标题标题标题",
                'summary':'老师，太饿了。怎么还不下课'
            }
        else:
            ret = {
                'code':1000,
                'courseList':[
                     { "name": '21天学会Pytasdfhon', 'id': 1},
                     { "name": '23天学会Pytasdfhon', 'id': 2},
                     { "name": '24天学会Pytasdfhon', 'id': 3},
                ]
            }
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response









