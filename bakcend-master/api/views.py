import json
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from rest_framework import views
from api import models
from rest_framework.exceptions import APIException
from rest_framework.response import Response
import rest_framework.parsers

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission

from rest_framework.request import Request
from rest_framework import exceptions

class LoginView(views.APIView):
    # def get(self,request,*args,**kwargs):
    #
    #     ret = {
    #         'code':1000,
    #         'data':'老男孩'
    #     }
    #     response = JsonResponse(ret)
    #     response['Access-Control-Allow-Origin'] = "*"
    #     return response

    # def post(self,request,*args,**kwargs):
    #     ret = {'code': 1000, 'msg': None,'data':None}
    #     dict = json.loads(request.body)
    #     user=dict['username']
    #     pwd=dict['password']
    #     obj=models.Account.objects.filter(username=user,password=pwd).first()
    #     if not obj:
    #         ret['code'] = 1001
    #         ret['msg'] = '密码或用户名错误'
    #         response = JsonResponse(ret)
    #         return response
    #     else:
    #         ret['code'] = 1000
    #         ret['data'] = obj.username
    #         response = JsonResponse(ret)
    #         return response
    #
    #
    #     # response = JsonResponse(ret)
    #     # response['Access-Control-Allow-Origin'] = "*"
    #     # return response
    #         obj_token = models.UserAuthToken.objects.all().first()
    #
    #         obj=obj_token.token
    #         ret['token'] = obj
    #         response = JsonResponse(ret)
    #         response['Access-Control-Allow-Origin'] = "*"
    #         return response


    def post(self, request, *args, **kwargs):
        ret = {
            'code': 1000,
            'username': '',
            'token': ''
        }

        body = request.body
        read_body = json.loads(body)

        user_obj = models.Account.objects.filter(**read_body).first()

        if user_obj:
            print(user_obj)
            ret['username'] = user_obj.username
            ret['token'] = user_obj.userauthtoken.token
        else:
            ret['code'] = 1001
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def options(self, request, *args, **kwargs):
        # self.set_header('Access-Control-Allow-Origin', "http://www.xxx.com")
        # self.set_header('Access-Control-Allow-Headers', "k1,k2")
        # self.set_header('Access-Control-Allow-Methods', "PUT,DELETE")
        # self.set_header('Access-Control-Max-Age', 10)
        print(request.POST)
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'content-type'

        # response['Access-Control-Allow-Methods'] = 'PUT'
        return response


# class CoursesView(views.APIView):
#
#     def get(self,request,*args,**kwargs):
#         pk = kwargs.get('pk')
#         if pk:
#             ret = {
#                 'title':"标题标题标题",
#                 'summary':'老师，太饿了。怎么还不下课'
#             }
#         else:
#             ret = {
#                 'code':1000,
#                 'courseList':[
#                      { "name": '21天学会Pytasdfhon', 'id': 1},
#                      { "name": '23天学会Pytasdfhon', 'id': 2},
#                      { "name": '24天学会Pytasdfhon', 'id': 3},
#                 ]
#             }
#
#
#
#
#
#
#
#
#
#
#         response = JsonResponse(ret)
#         response['Access-Control-Allow-Origin'] = "*"
#         return response



class TestAuthentication(BaseAuthentication):
    def authenticate(self, request):
        obj_token = models.UserAuthToken.objects.all().first()
        obj_token=obj_token.token
        val = request.query_params.get('token')
        if val not in obj_token:
            raise exceptions.AuthenticationFailed("用户认证失败")
        return ('obj_token.username', 'obj_token')
    def authenticate_header(self, request):
        pass

