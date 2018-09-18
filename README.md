# Training Online System

注意开发原则：
- Simple is better than complex
- Don't repeat yourself
- 充分应用restful api特性，用http状态码进行标识，直接返回对应的结果

使用djangorestframework-jwt作为前后端分离认证的凭证

利用/auth/login/获取token

```
curl -X POST -d "handle=admin&password=password123" http://localhost:8000/auth/login/
```

也可以使用邮箱登陆获取token

```
curl -X POST -d "handle=admin@admin.com&password=password123" http://localhost:8000/auth/login/

```

需要在header中带上验证字段

```
curl -H "Authorization: JWT <your_token>" http://localhost:8000/protected-url/
```

本地开发：

初始化数据库postgres


```
> psql
> CREATE USER onlinejudge WITH PASSWORD 'onlinejudge';
> CREATE DATABASE onlinejudge WITH OWNER onlinejudge;
```



```python
#
# class UserRegisterAPI(utils.APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserSerializer
#
#     def post(self, request):
#         """
#         User register api
#         """
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return self.success("Succeeded")
#         else:
#             return self.invalid_serializer(serializer)
```

不需要配置static目录，但是需要配置media目录，用于存储上传的文件和图片

TODO: 
- 增加一个config model，用来存储各种前端可以进行配置的项目
- 增加一个Tracking model，用来记录用户行为: https://medium.com/@atulmishra_69567/tracking-user-login-activity-in-django-rest-framework-jwt-authentication-32e0194e77d0
- 需要分离account和profile model