from flask import Flask
from courts_case import SearchCase
from flask_restful import Api, Resource, reqparse
import random
import json
# app = Flask(__name__)
# api = Api(app)

# class Quote(Resource):
# 	def get(self, link=""):
# 		if link != "":
# 			s = SearchCase("https://"+link)
# 			s.get_cases()
# 			return search.to_json(), 200
# 		return link, 404

# api.add_resource(Quote, "/cases", "/cases/", "/cases/<string:link>")
# if __name__ == '__main__':
#     app.run(debug=True)

#!flask/bin/python
from flask import Flask, request, jsonify
from flask import abort
from details import Details

app = Flask(__name__)

@app.route('/')
def index():
	return "Hello, World!"

@app.route('/search_case', methods=['GET'])
def search_cases():
	args = request.args
	link = ""
	for arg in args:
		link += arg + "="+args[arg]+"&"
	link = link.replace("link", "")
	s = SearchCase(link[1:-1])
	s.get_cases()
	return app.response_class(s.to_json(), mimetype="application/json"), 200

@app.route('/details', methods=['GET'])
def get_info_about_case():
	args = request.args
	link = args.get("link")
	d = Details(link)
	d.get_info()

	return app.response_class(d.to_json(), mimetype="application/json"), 200

if __name__ == '__main__':
	app.run(debug=True)