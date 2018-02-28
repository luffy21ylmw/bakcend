import json
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework import views
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
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

class CourseSerilizer(ModelSerializer):
    level=serializers.SerializerMethodField()
    class Meta:
        model=models.Course
        fields=['name','brief','level']
        depath=2
    def get_level(self,obj):
        return obj.get_level_display()

class CourseDetailSerilizer(ModelSerializer):
    recommend_courses=serializers.SerializerMethodField()
    class Meta:
        model = models.CourseDetail
        fields = ['course_slogan', 'video_brief_link','why_study','what_to_study_brief','career_improvement','prerequisite','hours','recommend_courses']
        depath = 2
    def get_recommend_courses(self,obj):
        li=[]
        for obj in obj.recommend_courses.all():
            li.append(obj.name)
        return li

class CoursesView(views.APIView):

    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            ret ={"概述":{},"章节":{},"评价":{},"问题":{}}
            courselist = models.Course.objects.filter(id=pk)
            course_detail = models.CourseDetail.objects.filter(course_id=pk)
            course_ser=CourseSerilizer(instance=courselist,many=True)
            course_detail_ser=CourseDetailSerilizer(instance=course_detail,many=True)

            for course in course_ser.data:
                ret["概述"]["name"]=course["name"]
                ret["概述"]['课程概述']=course['brief']
                ret["概述"]['level']=course['level']

            for course_detail in course_detail_ser.data:
                ret["概述"]["slogan"]=course_detail["course_slogan"]
                ret["概述"]["学习时间"] =course_detail["hours"]
                ret["概述"]["why_study"] = course_detail["why_study"]
                ret["概述"]["what_to_study_brief"] = course_detail["what_to_study_brief"]
                ret["概述"]["career_improvement"] = course_detail["career_improvement"]
                ret["概述"]["prerequisite"] = course_detail["prerequisite"]
                ret["概述"]["recommend_courses"] = course_detail["recommend_courses"]

            print(ret)


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









