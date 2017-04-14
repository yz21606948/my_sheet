# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from safetyInfo.models import SafeInformation


# Register your models here.
class SafeInformationAdmin(admin.ModelAdmin):
	list_display=('problem','problem_attribute','deadline')
	list_filter=('problem_origin',)
	date_hierarchy='publish_time'
	ordering=('-publish_time',)
	site_header='安全信息数据库管理'

admin.site.register(SafeInformation,SafeInformationAdmin)
