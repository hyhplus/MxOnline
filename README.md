# MxOnline
Django+Xadmin online project.  

## Django环境
这里的Django环境由2.0.1改为2.0.9  
主要是因为GitHub提示(Django2.0.1~Django2.0.8)存在安全漏洞的问题  

## Quick Start  
```py
pip install -r requirements.txt

python manage.py createsuperuser

```

##  MySQL创建数据库  
```py
create database MxOnline default charset=utf8;
```

## 数据库迁移
```py
python manage.py makemigrations
python manage.py migrate
```

## 运行项目
```py
python manage.py runserver 
```
