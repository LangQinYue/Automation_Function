# coding:utf8
import json

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from models import *
from realize import Realize
import logging
from django.contrib.auth import logout
from os import path
import start_keyword
import testdemo

logger = logging.getLogger(__name__)


def login_page(request):
	if request.method == "POST":
		return HttpResponse(Realize.verify(request, request.POST))
	return render(request, "html/signin.html")


def _logout(request):
	logout(request)
	return redirect("/")


def index(request):
	project_list = Project.objects.all()
	return render(request, "html/index.html", locals())

@csrf_exempt
def project(request):
	if request.method == 'POST':
		post_dict = request.POST
		action = request.POST.get('action')
	if request.method == 'GET':
		project_list = Project.objects.all()
		return render(request, 'html/proect_list.html', locals())
		

@csrf_exempt
def element(request):
	if request.method == "POST":
		post_dict = request.POST
		#print post_dict
		action = request.POST.get("action")
		if action == "add_element":
			'''新增元素'''
			try:
				element = {"name": post_dict["ele_name"], "desc": post_dict["ele_desc"],
				           "project": Project.objects.get(pk=post_dict["pro_id"])}

				create_ele = Element.objects.create(**element)
				ele_method_list, ele_content_list = post_dict.getlist("ele_method"), post_dict.getlist("ele_content")
				for method, content in zip(ele_method_list, ele_content_list):
					create_ele.elementcontent_set.create(method=method, content=content)
				return HttpResponse("保存成功")
			except Exception as e:
				logger.error(e)
				return HttpResponse("保存失败")

		elif action == "edit_element":
			'''编辑元素'''
			print post_dict["action"]
			try:
				up_element = Element.objects.filter(pk=post_dict["ele_id"]).update(name=post_dict["ele_name"],
				                                                                   desc=post_dict["ele_desc"],
				                                                                   project_id=Project.objects.get(
						                                                                   pk=post_dict["pro_id"]))
				ele_method_list, ele_content_list = post_dict.getlist("ele_method"), post_dict.getlist("ele_content")
				# update element_content
				Element.objects.update_many(post_dict["ele_id"], ele_method_list, ele_content_list)
				return HttpResponse("保存成功")
			except:
				return HttpResponse("保存失败")
		elif action == "get_element":
			'''编辑元素-获取元素'''
			ele_object = Element.objects.filter(pk=post_dict["ele_id"])
			ele_content = ElementContent.objects.filter(element_id=post_dict["ele_id"])
			ele_object_dict = {}
			# serialize Element ElementContent
			ele_dict = serializers.serialize("json", ele_object)
			ele_content_dict = serializers.serialize("json", ele_content)
			# merge Element ElementContent and return JsonResponse
			ele_object_dict["first_content"] = json.loads(ele_content_dict)[0]["fields"]
			ele_object_dict["second_content"] = json.loads(ele_content_dict)[1]["fields"]
			ele_object_dict['element_data'] = json.loads(ele_dict)[0]["fields"]
			return JsonResponse(ele_object_dict, safe=False)
		elif action == "delete_element":
			id_list = post_dict.getlist("id_list[]")
			try:
				for i in id_list:
					Element.objects.get(pk=i).elementcontent_set.all().delete()
					logger.info(u"删除元素表内容")
					Element.objects.get(pk=i).delete()
					logger.info("删除元素表内容")
				return HttpResponse("successful")
			except Exception as e:
				logger.error(e)
				return HttpResponse(u"删除元素失败")

	if request.method == "GET":
		project_id = request.GET.get("pro_id", None)
		element_list = Project.objects.get(pk=project_id).element_set.all()
		method_list = FindMethod.objects.all()
		return render(request, 'html/element.html', locals())
		#locals()会把element_list method_list project_id传给前台处理 这是一种省力方法 不需要写每个变量了


@csrf_exempt
def case_list(request):
	if request.method == "POST":
		action = request.POST['action']
		print action
		if action == "action_case":
			"""执行用例"""
			try:
				case_id = request.POST['id']
				if request.META.has_key('HTTP_X_FORWARDED_FOR'):
					ip = request.META['HTTP_X_FORWARDED_FOR']
				else:
					ip = request.META['REMOTE_ADDR']
				run_case = start_keyword.start_case(case_id, ip, 'case')
				
				print run_case
				if run_case:
					return HttpResponse("用例运行完毕")
				else:
					return HttpResponse("用例运行失败")
			except Exception as e:
				logger.error(e)

		elif action == "del_case":
			try:
				for case_id in request.POST.getlist("del_list[]"):
					TestCase.objects.get(pk=case_id).delete()
					CaseStep.objects.filter(testcase_id=case_id).delete()
				logger.info(u'删除成功')
				return HttpResponse("删除成功")
			except:
				return HttpResponse("删除失败")

	pro_id = request.GET["pro_id"]
	print pro_id
	test_case_list = TestCase.objects.filter(project_id=pro_id)
	return render(request, "html/case_list.html", locals())


@csrf_exempt
def scenario_list(request):
	if request.method == "POST":
		action = request.POST['action']
		if action == "del_scenario":
			del_list = request.POST.getlist("data[]")
			try:
				for scenario_id in del_list:
					del_obj = TestScenario.objects.get(id=scenario_id)
					del_obj.scenariocontent_set.all().delete()
					del_obj.delete()
				return HttpResponse("删除成功")
			except:
				logger.info("删除失败")
		elif action == "run_suite":
			suite_id = request.POST['suite_id']
			try:
				if request.META.has_key('HTTP_X_FORWARDED_FOR'):
					ip = request.META['HTTP_X_FORWARDED_FOR']
				else:
					ip = request.META['REMOTE_ADDR']
				run_suite = start_keyword.start_case(case_id=suite_id, current_ip=ip, _type='suite')
				if run_suite:
					return HttpResponse("用例运行完毕")
				else:
					return HttpResponse("用例运行失败")
			except Exception as e:
				logger.error(e)

	pro_id = request.GET["pro_id"]
	scenario = TestScenario.objects.filter(project_id=pro_id)
	return render(request, "html/case_scenario.html", locals())


@csrf_exempt
def add_case_scenario(request):
	if request.method == "POST":
		case_id_list = request.POST.getlist("case_id")
		name = request.POST.get("scenario_name")
		project_id = request.POST.get("project_id")
		status = request.POST.get("scenario_status")
		add_scenario = Project.objects.get(id=project_id).testscenario_set.create(name=name, status=status)
		for c_id in case_id_list:
			add_scenario.scenariocontent_set.create(case=c_id)
		return HttpResponse("保存成功")

	pro_id = request.GET["pro_id"]
	test_case_list = TestCase.objects.filter(project_id=pro_id)
	return render(request, "html/add_scenario.html", locals())


@csrf_exempt
def edit_scenario(request):
	if request.method == "POST":
		req = request.POST
		scenario_obj = TestScenario.objects.get(id=req['scenario_id'])
		scenario_obj.name, scenario_obj.status = req['scenario_name'], req['scenario_status']

		try:
			scenario_obj.scenariocontent_set.all().delete()
			for i in req.getlist("case_id"):
				scenario_obj.scenariocontent_set.create(case=i)
			scenario_obj.save()
			return HttpResponse("保存成功")
		except:
			logger.info("编辑场景保存失败")

	if request.method == "GET":
		scenario_id = request.GET['id']
		pro_id = request.GET['pro_id']
		scenario_obj = TestScenario.objects.get(id=scenario_id)
		case_id_list = [i.case for i in scenario_obj.scenariocontent_set.all()]
		case_obj_list = [TestCase.objects.get(id=i) for i in case_id_list]
		test_case_list = TestCase.objects.filter(project_id=pro_id)
		return render(request, "html/edit_scenario.html", locals())


@csrf_exempt
def add_case(request):
	if request.method == 'POST':
		post_dict = request.POST
		action = post_dict.get("action", None)
		if action == "look_element":
			logger.info(u"查看元素")
			try:
				ele_id = post_dict["ele_id"]
				logger.info(u"元素ID:%s" % ele_id)
				json_ele = \
					json.loads(
							serializers.serialize("json", Element.objects.filter(pk=ele_id), fields=('name', "desc")))[0]['fields']
				json_content = json.loads(
						serializers.serialize("json", ElementContent.objects.filter(element_id=ele_id),fields=('method', 'content')))
				json_ele["first"] = json_content[0]["fields"]
				json_ele["second"] = json_content[1]["fields"]
				logger.info(u"返回前端字典:%s" % json.dumps(json_ele))
				return JsonResponse(json_ele, safe=False)
			except Exception as e:
				logger.error(e)
		elif action == "add_test_case":
			logger.info(u"新增用例-写入数据")
			unique_case = TestCase.objects.filter(name=post_dict['case_name']).__bool__()

			if not unique_case:
				try:
					case_dict = {"name": post_dict['case_name'], "nature": post_dict['nature'],
					             "status": post_dict['status'],
					             "level": post_dict['level'], "project_id": post_dict['project_id']}

					create_obj = TestCase.objects.create(**case_dict)
					keyword_list, element_list = post_dict.getlist("keyword"), post_dict.getlist("ele_id")
					value_list, desc_list = post_dict.getlist("value"), post_dict.getlist("desc")
					for keyword, element, value, desc in zip(keyword_list, element_list, value_list, desc_list):
						create_obj.casestep_set.create(keyword=keyword, element=element, value=value, desc=desc)
					return HttpResponse("保存成功")
				except Exception as e:
					logger.error(e)
					return HttpResponse("保存失败")
			else:
				return HttpResponse(u"用例名称重复")

	elif request.method == "GET":
		if request.GET.get("action") == "add_case":
			pro_id = request.GET["pro_id"]
			keyword = Keyword.objects.all()
			element_list = Element.objects.all()
			action = "add_test_case" #action赋值 post方法用到
			import_case = Project.objects.get(pk=pro_id).testcase_set.all()
			element_list = Element.objects.filter(project_id=pro_id)
			return render(request, 'html/add_case.html', locals())


@csrf_exempt
def edit_case(request):
	if request.method == "GET":
		case_id = request.GET.get("id")
		case_obj = TestCase.objects.get(pk=case_id)
		
		step_list = []

		for step in CaseStep.objects.filter(testcase_id=case_id):
			step_dict = step.__dict__ #把一个对象变成了一个字典
			step_dict["display_name"] = Keyword.objects.get(name=step_dict["keyword"]).display_name
			ele_name = step_dict["element"]
			if step_dict["keyword"] == "import_case":
				print ele_name
				step_dict["element_name"] = TestCase.objects.get(id=ele_name).name
			else:
				if step_dict["element"] == "":
					step_dict["element_name"] = "请选择元素"
				else:
					step_dict["element_name"] = Element.objects.get(id=ele_name).name
			step_list.append(step_dict)
		element_list = Element.objects.all()#在edit_case.html元素为select_element使用
		keyword_list = Keyword.objects.all()
		pro_id = TestCase.objects.get(id=case_id).project_id
		case_list_obj = Project.objects.get(id=pro_id).testcase_set.all()
		return render(request, "html/edit_case.html", locals())

	elif request.method == "POST":
		pro_id = request.POST.get("pro_id")
		case_id = request.POST.get("case_id")
		status = request.POST.get("status")
		nature = request.POST.get("nature")
		level = request.POST.get("level")
		name = request.POST.get("case_name")
		keyword = request.POST.getlist("keyword")#获取name属性为keywor的数据 是一组哦 所以要用getlist方法
		ele_id = request.POST.getlist("ele_id")
		value = request.POST.getlist("value")
		desc = request.POST.getlist("desc")

		try:
			TestCase.objects.filter(id=case_id).update(name=name, nature=nature, status=status, level=level)
			case_query_dict = TestCase.objects.get(id=case_id)
			case_query_dict.casestep_set.all().delete()
			case_query_dict.casestep_set.all().delete()
			for i in range(len(keyword)):
				case_query_dict.casestep_set.create(keyword=keyword[i], element=ele_id[i],
				                                    value=value[i], desc=desc[i])
			return HttpResponse("保存成功")
		except:
			logger.info("删除步骤失败")
			return HttpResponse("保存失败")


@csrf_exempt
def ajax_html(request):
	action = request.GET.get("action", None)
	if action == 'import_case':
		"""导入用例"""
		case_object = TestCase.objects.get(pk=request.GET["id"])
		keyword = Keyword.objects.get(name='import_case')
		return render(request, 'ajax/import_case.html', locals())
	if action == 'add_case_step':
		"""增加步骤"""
		keyword = Keyword.objects.all()
		return render(request, "ajax/add_case_step.html", locals())

	elif action == "import_step":
		"""导入步骤"""
		step_list = CaseStep.objects.filter(testcase_id=request.GET['id'])
		import_step = []
		for i in step_list:
			step_dict = i.__dict__
			step_dict['key_display'] = Keyword.objects.get(name=i.keyword).display_name
			if i.element:
				step_dict['ele_name'] = Element.objects.get(pk=i.element).name
			else:
				step_dict['ele_name'] = "点击选择元素"
			import_step.append(step_dict)
		key_list = Keyword.objects.all()
		return render(request, "ajax/import_step.html", locals())

	elif action == "add_case_scenario":
		case_id_list = request.GET["case_list"].split(",")
		add_case_list = [TestCase.objects.get(id=i) for i in case_id_list]
		return render(request, 'ajax/add_case_scenario.html', locals())

	elif action == "edit_case_import_step":
		case_id = request.GET['id']
		step_list = []
		for step in CaseStep.objects.filter(testcase_id=case_id):
			step_dict = step.__dict__
			step_dict["display_name"] = Keyword.objects.get(name=step_dict["keyword"]).display_name
			step_list.append(step_dict)
			if step_dict['element']:
				step_dict["element_name"] = Element.objects.get(id=step_dict['element']).name
			else:
				step_dict["element_name"] = "请选择元素"
		keyword_list = Keyword.objects.all()
		return render(request, "ajax/edit_case_import_step.html", locals())


def is_html_path(request):
	name = request.GET.get("name", None)
	html_path = path.dirname(path.dirname(__file__)) + "/templates/report/" + name + ".html"
	if path.exists(html_path):
		return HttpResponse(True)
	else:
		return HttpResponse(False)


def report(request, html_name):
	if html_name.endswith(".png"):
		png_path = path.dirname(path.dirname(__file__)) + "/templates/report/" + html_name
		with open(png_path, 'rb') as f:
			ime_date = f.read()
		return HttpResponse(ime_date, content_type="image/png")
	else:
		return render(request, 'report/{}.html'.format(request.GET["name"]))


def test(request):
	return render(request, "html/modals.html")

