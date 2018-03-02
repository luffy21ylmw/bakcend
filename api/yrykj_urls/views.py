import json,hashlib,time,redis
from pprint import pprint
from rest_framework.request import Request
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db.models import F


from rest_framework import views

from rest_framework import serializers
from rest_framework.permissions import BasePermission


import json
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from rest_framework.views import APIView

from rest_framework.response import Response



from api.plugins.token_auth import LuffyTokenAuthentication

from api.plugins import redis_pool
from api.plugins.exception import PricePolicyDoesNotExist

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

class Mycourse(serializers.ModelSerializer):

    class Meta:
        model = models.Course
        # fields = "__all__"
        fields = ['get_course_type_display', 'id']
        depth = 2


class MyShoppingCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = "__all__"
        depth = 2

class LuffyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.query_params.get('token'):
            return True


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
                print(usr.__dict__)
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
        course = models.Course.objects.all()
        ser_course = Mycourse(instance=course,many=True)
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
        print(ser_course.data)
        response = JsonResponse(ser_course.data,safe=False)
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
        parent_id = request.data.get('parent_id')
        if token and (id or parent_id):
            # article_obj = models.Article.objects.filter(id=id)
            usr_token_obj = models.UserAuthToken.objects.filter(token=token).first()
            usr_obj = models.Account.objects.filter(userauthtoken=usr_token_obj).first()
            if usr_obj and id and not parent_id:
                models.Comment.objects.create(content_type_id=8,object_id=id,content=request.data.get('comment'),
                                              account=usr_obj)
                models.Article.objects.filter(id=id).update(comment_num=F('comment_num')+1)
            if usr_obj and id and parent_id:
                models.Comment.objects.create(content_type_id=8,object_id=id,content=request.data.get('comment'),
                                              account=usr_obj,p_node_id=id)
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



CONN = redis.Redis(connection_pool=redis_pool.POOL)

class ShoppingCarView(APIView):
    message = '无权访问'
    """
    购物车接口
    """
    authentication_classes = [LuffyTokenAuthentication, ]
    permission_classes = [LuffyPermission, ]

    def get(self, request, *args, **kwargs):
        response = {'code': 1000, 'data': None}
        try:
            product_dict = CONN.hget(settings.REDIS_SHOPPING_CAR_KEY, request.user.id)

            if product_dict:
                product_dict = json.loads(product_dict.decode('utf-8'))
                response['data'] = product_dict
        except Exception as e:
            response['code'] = 1001
            response['msg'] = "获取购物车列表失败"

        return Response(response)

    def post(self, request, *args, **kwargs):

        response = {'code': 1000, 'msg': None}
        try:
            course_id = int(request.data.get('course_id'))
            policy_id = int(request.data.get('policy_id'))

            # 获取课程信息
            course = models.Course.objects.exclude(course_type=2).filter(status=0).get(id=course_id)

            # 序列化课程信息，并获取其关联的所有价格策略
            ser = MyShoppingCarSerializer(instance=course, many=False)
            product = ser.data

            # 判断价格策略是否存在
            policy_exist = False
            for policy in product['price_policy_list']:
                if policy['id'] == policy_id:
                    policy_exist = True
                    break
            if not policy_exist:
                raise PricePolicyDoesNotExist()

            # 设置默认选中的价格策略
            product.setdefault('choice_policy_id', policy_id)
            # 获取当前用户在购物车中已存在的课程，如果存在则更新，否则添加新课程
            product_dict = CONN.hget(settings.REDIS_SHOPPING_CAR_KEY, request.user.id)
            if not product_dict:
                product_dict = {course_id: product}
            else:
                product_dict = json.loads(product_dict.decode('utf-8'))
                product_dict[course_id] = product
            # 将新课程写入到购物车
            CONN.hset(settings.REDIS_SHOPPING_CAR_KEY, request.user.id, json.dumps(product_dict))

        except ObjectDoesNotExist as e:
            response['code'] = 1001
            response['msg'] = '视频不存在'
        except PricePolicyDoesNotExist as e:
            response['code'] = 1002
            response['msg'] = '价格策略不存在'
        except Exception as e:
            print(e)
            response['code'] = 1003
            response['msg'] = '添加购物车失败'

        return Response(response)

    def delete(self, request, *args, **kwargs):
        """
        删除购物车中的课程
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = {'code': 1000}
        try:
            course_id = kwargs.get('pk')
            product_dict = CONN.hget(settings.REDIS_SHOPPING_CAR_KEY, request.user.id)
            if not product_dict:
                raise Exception('购物车中无课程')
            product_dict = json.loads(product_dict.decode('utf-8'))
            if course_id not in product_dict:
                raise Exception('购物车中无该商品')
            del product_dict[course_id]
            CONN.hset(settings.REDIS_SHOPPING_CAR_KEY, request.user.id, json.dumps(product_dict))
        except Exception as e:
            response['code'] = 1001
            response['msg'] = str(e)

        return Response(response)

    def put(self, request, *args, **kwargs):
        """
        更新购物车中的课程的默认的价格策略
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = {'code': 1000}
        try:
            course_id = kwargs.get('pk')
            policy_id = request.data.get('policy_id')
            product_dict = CONN.hget(settings.REDIS_SHOPPING_CAR_KEY, request.user.id)
            if not product_dict:
                raise Exception('购物车清单不存在')
            product_dict = json.loads(product_dict.decode('utf-8'))
            if course_id not in product_dict:
                raise Exception('购物车清单中商品不存在')

            policy_exist = False
            for policy in product_dict[course_id]['price_policy_list']:
                if policy['id'] == policy_id:
                    policy_exist = True
                    break
            if not policy_exist:
                raise PricePolicyDoesNotExist()

            product_dict[course_id]['choice_policy_id'] = policy_id
            CONN.hset(settings.REDIS_SHOPPING_CAR_KEY, request.user.id, json.dumps(product_dict))
        except PricePolicyDoesNotExist as e:
            response['code'] = 1001
            response['msg'] = '价格策略不存在'
        except Exception as e:
            response['code'] = 1002
            response['msg'] = str(e)

        return Response(response)


class Course_buy(APIView):
    pass