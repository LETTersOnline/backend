# Training Online System

注意开发原则：
- Simple is better than complex
- Don't repeat yourself

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