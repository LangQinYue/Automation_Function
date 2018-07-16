# -.- coding:utf-8 -.-
__author__ = 'lang.qy'
# import MySQLdb
# import MySQLdb.cursors
import sqlite3


class DB(object):
	@classmethod
	def connect(cls):
		try:
# 			ddb = MySQLdb.connect("192.168.80.141", "root", "helloworld", port=3306, db="django",
# 			                     cursorclass=MySQLdb.cursors.DictCursor, charset="utf8")
			db = sqlite3.connect('D:\\eclipsworkdir\\Automation_Platform\\db.sqlite3')
			return db, db.cursor()
		except Exception as e:
			raise ValueError("Connect Mysql Error", e)

	@classmethod
	def query(cls, sql):
		db, cur = cls.connect()
		try:
			cur.execute(sql)
			db.commit()

		except Exception,e:
			print e
		return cur.fetchall()
	@classmethod
	def case(cls, case_id):
		sql = "select id,name,nature,status,level from TestCase where id = {}".format(case_id)
		if len(cls.query(sql))>0:
			casekey = ['id','name','nature','status','level']
			case = list(cls.query(sql)[0])
			return dict(zip(casekey,case))

	@classmethod
	def step(cls, case_id):
		"""
		:param case_id: case id
		:return: case step
		"""
		sql = "select keyword,value,desc,element from CaseStep where testcase_id = {}"
		stepkey=['keyword','value','desc','element']
		step = cls.query(sql.format(case_id))
		stepdict = [dict(zip(stepkey,x)) for x in step ]
		#print stepdict
		case_step = []
		for step_dict in stepdict:
			if step_dict['keyword'] == "import_case":  # 如果是导入用例,则加入该用例的步骤
				import_case_id = step_dict['element']
				for import_step in cls.query(sql=sql.format(import_case_id)):
					case_step.append(import_step)
			else:
				case_step.append(step_dict)
		return case_step

	@classmethod
	def url(cls, case_id):
		"""
		:param case_id: case id
		:return:
		"""
		sql = "SELECT address FROM Project WHERE id = (SELECT project_id FROM TestCase WHERE id = {})".format(case_id)
		if len(cls.query(sql))>0:
			return str(cls.query(sql)[0][0]).decode('utf-8').encode('utf-8')
		else:
			print 'not query data'

	@classmethod
	def element(cls, ele_id):
		if ele_id:
			sql = "select content,method from ElementContent where element_id = {}".format(ele_id)
			ele = list(cls.query(sql))
			elekey = ['content','method']
			loc_list = [dict(zip(elekey,x)) for x in ele ]
			sql = "select name from Element where id = {}".format(ele_id)
			name = cls.query(sql)[0][0]
			print name
			for i in loc_list:
				i['name'] = name
			return loc_list
		else:
			pass

	@classmethod
	def suite_parse_case(cls, dict_data):
		"""
		:param dict_data: {"ip": "127.0.0.1", "type": "suite", "id": "8"}
		:return: case list
		"""
		sql = "select `ScenarioContent`.`case` as id  from `ScenarioContent` where `ScenarioContent`.`scenario_id` = {}".format(
				dict_data["id"])
		case_content_list = []
		a = cls.query(sql)

		for i in a:
			case_content = cls.case(int(i[0]))
			#print case_content
			case_content["ip"] = dict_data['ip']
			case_content["type"] = "case"
			case_content_list.append(case_content)
		return case_content_list


if __name__ == "__main__":
	#a= DB.element(12)
	data = {'ip':'127.0.0.1','id':2}
	print DB.element(29)
