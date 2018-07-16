# coding:utf8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class DateBase(models.Model):
	name = models.CharField(max_length=50, verbose_name=u"名称")
	host = models.CharField(max_length=20, verbose_name=u"IP/域名")
	username = models.CharField(max_length=50, verbose_name=u"用户名")
	password = models.CharField(max_length=50, verbose_name=u"密码")
	port = models.CharField(max_length=4, verbose_name=u"端口")
	db = models.CharField(max_length=50, verbose_name=u"数据库")

	class Meta:
		verbose_name = u"数据库表"
		verbose_name_plural = verbose_name
		db_table = "DateBase"

	def __unicode__(self):
		return self.name


class Project(models.Model):
	name = models.CharField(max_length=50, verbose_name=u"名称")
	address = models.CharField(max_length=100, verbose_name=u"地址")
	desc = models.CharField(max_length=200, verbose_name=u"说明")
	create_at = models.DateTimeField(auto_now_add=True, null=True)
	update_at = models.DateTimeField(auto_now=True, null=True)
	db = models.ForeignKey(DateBase, verbose_name=u"数据库ID")

	class Meta:
		verbose_name = u"项目表"
		verbose_name_plural = verbose_name
		db_table = "Project"

	def __unicode__(self):
		return self.name


class MyUserManager(BaseUserManager):
	def current_time(self):
		"""get current time """
		from datetime import datetime
		return datetime.now().strftime("%Y-%m-%d")

	def create_user(self, username, email, qq=None, mobile=None, department=None, project=None, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""

		if not username:
			raise ValueError('username is unique')

		user = self.model(username=username, email=self.normalize_email(email), date_of_birth=self.current_time(),
		                  qq=qq,
		                  mobile=mobile, department=department, project=project)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password, qq=None, mobile=None, department=None, project=None, ):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(username, email, password=password, qq=qq, mobile=mobile,
		                        department=department, project=project)
		user.is_admin = True
		user.save(using=self._db)
		return user


class MyUser(AbstractBaseUser):
	username = models.CharField(max_length=50, verbose_name="username", unique=True, )
	qq = models.CharField(max_length=10, verbose_name="QQ", null=True)
	mobile = models.CharField(max_length=11, verbose_name="Phone Number", null=True)
	department = models.CharField(max_length=20, verbose_name="Department", null=True)
	email = models.EmailField(verbose_name='Email Address', max_length=255, unique=True, )
	project = models.ForeignKey(Project, verbose_name="Project", null=True)
	date_of_birth = models.DateField()
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	objects = MyUserManager()
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['date_of_birth']

	def get_full_name(self):
		# The user is identified by their email address
		return self.username

	def get_short_name(self):
		# The user is identified by their email address
		return self.username

	def __unicode__(self):  # __unicode__ on Python 2
		return self.username

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin


class FindMethod(models.Model):
	method = models.CharField(max_length=10, verbose_name=u"定位方式")
	display = models.CharField(max_length=10, verbose_name=u"显示名称")

	class Meta:
		verbose_name = u"定位方式表"
		verbose_name_plural = verbose_name
		db_table = u"FindMethod"

	def __unicode__(self):
		return self.method


class Keyword(models.Model):
	name = models.CharField(max_length=50, verbose_name=u"关键字")
	display_name = models.CharField(max_length=50, verbose_name=u"显示的关键字")

	class Meta:
		verbose_name = u"关键字表"
		verbose_name_plural = verbose_name
		db_table = "keyword"

	def __unicode__(self):
		return self.name


class Ele_Manger(models.Manager):
	def update_many(self, element_id, ele_method_list, ele_content_list):
		"""根据element_id跟新element_content"""
		content_list = ElementContent.objects.filter(element_id=element_id)
		for ele_index, content in enumerate(zip(ele_method_list, ele_content_list)):
			ElementContent.objects.filter(pk=content_list[ele_index].id).update(method=content[0],
			                                                                    content=content[1])


class Element(models.Model):
	name = models.CharField(max_length=50, verbose_name=u"名称")
	desc = models.CharField(max_length=200, verbose_name=u"说明")
	create_at = models.DateTimeField(auto_now_add=True, null=True)
	update_at = models.DateTimeField(auto_now=True, null=True)
	objects = Ele_Manger()
	project = models.ForeignKey(Project, verbose_name=u"项目ID")

	class Meta:
		verbose_name = "元素表"
		verbose_name_plural = verbose_name
		db_table = "Element"
		ordering = ['-id']

	def __unicode__(self):
		return self.name


class ElementContent(models.Model):
	method = models.CharField(max_length=10, verbose_name=u"定位方式")
	content = models.CharField(max_length=100, verbose_name=u"定位值")
	element = models.ForeignKey(Element, verbose_name=u"元素ID")

	class Meta:
		verbose_name = u"元素内容表"
		verbose_name_plural = verbose_name
		db_table = "ElementContent"

	def __unicode__(self):
		return self.method


class TestCase(models.Model):
	name = models.CharField(max_length=50, verbose_name=u"用例名称")
	nature = models.CharField(max_length=50, verbose_name=u"用例性质")
	status = models.CharField(max_length=20, verbose_name=u"用例状态")
	level = models.CharField(max_length=5, verbose_name=u"用例等级", null=True)
	create_at = models.DateField(auto_now_add=True, null=True)
	update_at = models.DateField(auto_now=True, null=True)
	project = models.ForeignKey(Project, verbose_name=u"项目ID")

	class Meta:
		verbose_name = u"测试用例表"
		verbose_name_plural = verbose_name
		db_table = "TestCase"

	def __unicode__(self):
		return self.name


class CaseStep(models.Model):
	# 后期需要保留element null=True的选项.有用
	keyword = models.CharField(max_length=20, verbose_name=u"关键字")
	element = models.CharField(max_length=10, verbose_name=u"元素表ID", null=True)
	value = models.CharField(max_length=255, verbose_name=u"输入值")
	desc = models.CharField(max_length=200, verbose_name=u"步骤说明")
	testcase = models.ForeignKey(TestCase, verbose_name=u"用例ID")

	class Meta:
		verbose_name = u"用例步骤表"
		verbose_name_plural = verbose_name
		db_table = "CaseStep"

	def __unicode__(self):
		return self.keyword


class TestScenario(models.Model):
	name = models.CharField(max_length=50, verbose_name=u"名称")
	status = models.CharField(max_length=10, verbose_name=u"状态")
	create_at = models.DateTimeField(auto_now_add=True, null=True)
	update_at = models.DateTimeField(auto_now=True, null=True)
	project = models.ForeignKey(Project, verbose_name=u"项目ID")

	class Meta:
		verbose_name = u"测试场景表"
		verbose_name_plural = verbose_name
		db_table = "TestScenario"

	def __unicode__(self):
		return self.name


class ScenarioContent(models.Model):
	case = models.CharField(max_length=5, verbose_name=u"用例ID")
	scenario = models.ForeignKey(TestScenario, verbose_name=u"场景ID")

	class Meta:
		verbose_name = u"场景用例表"
		verbose_name_plural = verbose_name
		db_table = "ScenarioContent"

	def __unicode__(self):
		return self.case
