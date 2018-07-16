# coding:utf8
from django.contrib import admin
from models import *
# Register your models here.

admin.site.register(MyUser)
admin.site.register(DateBase)
admin.site.register(Project)
admin.site.register(Keyword)
admin.site.register(Element)
admin.site.register(ElementContent)
admin.site.register(TestCase)
admin.site.register(CaseStep)
admin.site.register(TestScenario)
admin.site.register(ScenarioContent)
admin.site.register(FindMethod)
