# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.html import format_html

class SafeInformationManagee(models.Manager):
	def problem_attr_count(self,attr,date_from,date_to):
		return self.filter(problem_attribute__icontains=attr,publish_time__range=(date_from,date_to)).count()

class SafeInformation(models.Model):
	history_time=models.DateField(verbose_name='历史时间')
	publish_time=models.DateField(verbose_name='发布日期')
	problem=models.TextField(verbose_name='整改问题')
	problem_origin=models.CharField(max_length=50,verbose_name='问题来源')
	problem_platform=models.CharField(max_length=50,verbose_name='发布平台')
	problem_attribute=models.CharField(max_length=50,verbose_name='问题属性')
	problem_reason=models.TextField(blank=True,verbose_name="问题原因")
	consequence=models.TextField(blank=True,verbose_name='问题后果')
	problem_level=models.CharField(max_length=50,verbose_name='问题等级')
	responsiblity=models.CharField(max_length=50,verbose_name='责任单位')
	publisher=models.CharField(max_length=50,verbose_name='发布人员')
	deadline=models.DateField(verbose_name='整改期限')

	objects=SafeInformationManagee()

	def __unicode__(self):
		return self.problem

	class Meta:
		verbose_name='安全信息数据库'
		verbose_name_plural='安全信息数据库'
