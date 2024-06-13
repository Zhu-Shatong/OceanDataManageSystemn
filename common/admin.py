from django.contrib import admin

# Register your models here.

'''
    在此处注册所有的数据库表项 
'''
from .models import *

admin.site.register(SeaSurfaceHeight)
admin.site.register(IdentityInfo)
admin.site.register(QueryAssist)
admin.site.register(Visitor)
admin.site.register(Staff)
admin.site.register(Dataset)
admin.site.register(Score)
admin.site.register(Comment)
admin.site.register(Apply)
admin.site.register(Current_Apply)
admin.site.register(Communication)
admin.site.register(Authorization)
admin.site.register(Permission)
