import json,hashlib,time
from pprint import pprint
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db.models import F

from rest_framework import views
from rest_framework.response import Response
from rest_framework import serializers

from django.http.request import HttpRequest

from api import models

class Myserializers(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = "__all__"
        # fields = ['user', 'pwd', 'ut']
        depth = 2

class Mycomment(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"
        # fields = ['user', 'pwd', 'ut']
        depth = 0



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
        userinfo = json.loads(request.body)
        # print(userinfo)
        if 'username' in userinfo and 'password' in userinfo:
            usr = models.Account.objects.filter(username=userinfo['username'], password=userinfo['password']).first()
            if usr:
                token = hashlib.md5()
                token.update(str(time.time()).encode("utf8"))
                token = token.hexdigest()
                if usr.userauthtoken.token:
                    models.UserAuthToken.objects.filter(user=usr).update(token=token)
                else:
                    models.UserAuthToken.objects.create(user=usr, token=token)
                request.session[token] = {'user': userinfo['username']}
                ret = JsonResponse({'token': token, 'username': userinfo['username'],'sta':True})
                # ret['Access-Control-Allow-Origin'] = '*'
                # ret['Access-Control-Allow-Headers'] = '*'
                return ret
        # ret = JsonResponse('用户名密码错误')
        ret = JsonResponse({'sta':False})
        return ret


    def options(self, request, *args, **kwargs):
        # self.set_header('Access-Control-Allow-Origin', "http://www.xxx.com")
        # self.set_header('Access-Control-Allow-Headers', "k1,k2")
        # self.set_header('Access-Control-Allow-Methods', "PUT,DELETE")
        # self.set_header('Access-Control-Max-Age', 10)
        # print(request.POST)
        response = HttpResponse()
        # response['Access-Control-Allow-Origin'] = '*'
        # response['Access-Control-Allow-Headers'] = '*'
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
        # response['Access-Control-Allow-Origin'] = "*"
        return response


class NewsView(views.APIView):

    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        total_dic = {}
        if pk:
            article = models.Article.objects.filter(pk=pk).first()
            ser = Myserializers(instance=article, many=False)
            ser_c = models.Comment.objects.filter(content_type_id=8,object_id=pk)
            ser_com = Mycomment(instance=ser_c, many=True)
            article.view_num += 1
            article.save()
            # print(ser_com.data)
        else:
            article = models.Article.objects.all()
            ser = Myserializers(instance=article, many=True)
            ser_com = False
            # print(ser.data)
        total_dic['ser'] = ser.data
        if ser_com:
            total_dic['com'] = ser_com.data
        # pprint(total_dic)


        return Response(total_dic)


class CommentView(views.APIView):
    def post(self,request,*args,**kwargs):
        token = request.data.get('token')
        id = request.data.get('id')
        child_id = request.data.get('child_id')
        if token and (id or child_id):
            # article_obj = models.Article.objects.filter(id=id)
            usr_token_obj = models.UserAuthToken.objects.filter(token=token).first()
            usr_obj = models.Account.objects.filter(userauthtoken=usr_token_obj).first()
            if usr_obj and id:
                models.Comment.objects.create(content_type_id=8,object_id=id,content=request.data.get('comment'),
                                              account=usr_obj)
                models.Article.objects.filter(id=id).update(comment_num=F('comment_num')+1)
            if usr_obj and child_id:
                pass
            return Response('ok')
        else:
            return Response('nok')

    def options(self, request, *args, **kwargs):
        response = Response('ok')

        return response


class AgreeView(views.APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        token = request.data.get('token')
        id = request.data.get('id')
        if token and id:
            artecle_obj = models.Article.objects.filter(id=id).first()
            usr_token_obj = models.UserAuthToken.objects.filter(token=token).first()
            usr_obj = models.Account.objects.filter(userauthtoken=usr_token_obj).first()
            if usr_obj and id:
                exist_agree_obj = models.Comment.objects.filter(content_type_id=8,account=usr_obj,object_id=id)
                if exist_agree_obj:
                    models.Comment.objects.filter(content_type_id=8,object_id=id, account=usr_obj).update(
                        agree_number=F('agree_number') - 1)
                    models.Article.objects.filter(id=id).update(agree_num=F('agree_num')-1)
                    exist_agree_obj.delete()
                else:
                    models.Comment.objects.create(content_object=artecle_obj,account=usr_obj)
                    models.Article.objects.filter(id=id).update(agree_num=F('agree_num')+1)
                    models.Comment.objects.filter(content_type_id=8,object_id=id,account=usr_obj).update(agree_number=F('agree_number')+1)
            return Response('ok')
        return Response('nok')

    def options(self, request, *args, **kwargs):
        response = Response()
        return response


class CollectView(views.APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        token = request.data.get('token')
        id = request.data.get('id')
        if token and id:
            usr_token_obj = models.UserAuthToken.objects.filter(token=token).first()
            usr_obj = models.Account.objects.filter(userauthtoken=usr_token_obj).first()
            if usr_obj and id:
                article_obj = models.Article.objects.filter(id=id).first()
                exist_collect_obj = models.Collection.objects.filter(content_type_id=8,object_id=id,account=usr_obj)
                print(exist_collect_obj)
                if exist_collect_obj:
                    exist_collect_obj.delete()
                    models.Article.objects.filter(id=id).update(collect_num=F('collect_num') - 1)
                else:
                    models.Collection.objects.create(content_object=article_obj, account=usr_obj)
                    models.Article.objects.filter(id=id).update(collect_num=F('collect_num')+1)
            return Response('ok')
        return Response('nok')

    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        return response
