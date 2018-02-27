import json
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework import views
import rest_framework.parsers

from api import models

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
            ret ={"概述":[],"章节":[],"评价":[],"问题":[]}
            courselist = models.Course.objects.filter(id=pk).values('name',"coursedetail__course_slogan","brief")
            self.dispatch()

        else:
            ret = {
                'code': 1000,
                'courseList': []
            }
            courselist=models.Course.objects.all()
            for course in courselist:
                ret['courseList'].append({
                    'id':course.id,
                    'course_img':course.course_img,
                    'name':course.name,
                    'brief':course.brief,
                    'level':course.get_level_display()
                })
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response









