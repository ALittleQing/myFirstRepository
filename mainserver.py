import tornado.ioloop
import tornado.web
from tornado.options import options,define
import os
import MySQLdb

define("host",default="10.10.10.112")
define("user",default="root")
define("passwd",default="1234")
define("db",default="Chen")
define("port",default=3306)

def queryall(sql):
    db = MySQLdb.connect(
            options.host,
            options.user,
            options.passwd,
            options.db,
            options.port,
            charset="utf8",
            )
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		# self.write("<p>Hello</p>")
		self.render("index.html")
# 
class AjaxHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('ajax_info.txt')

class EChartsHandler(tornado.web.RequestHandler):
	def get(self):
		sql = 'select * from case_work'
		datas = queryall(sql)
		print datas
		self.render("ECharts.html",datas=datas)
# 
settings = dict(
		template_path = os.path.join(os.path.dirname(__file__),'templates'),
    	static_path = os.path.join(os.path.dirname(__file__),'static'),
		debug=True,
	)
def make_app():
	return tornado.web.Application([
			(r"/",MainHandler),
			(r"/echarts",EChartsHandler),
			(r"/99",AjaxHandler),
		],**settings)
if __name__ == "__main__":
	print 'start...'
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()