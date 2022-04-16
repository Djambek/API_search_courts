import requests
from bs4 import BeautifulSoup as bs
import json

def to_normal(text:str) -> str:
	return text.replace("  ", "").replace("\n", "") # надо изучить регулярки

class Details():
	def __init__(self, link):
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		request = requests.get(link, headers=headers)
		self.page = bs(request.text, 'html.parser')
		self.case = dict()

	def get_info(self):

		# табличка с основной информацией
		for div in self.page.find_all("div", class_="cardsud_wrapper"):
			for div_row in div.find_all("div", class_="row_card"):
				name = to_normal(div_row.find("div", class_="left").text)
				value = to_normal(div_row.find("div", class_="right").text)
				if name == "Уникальный идентификатор дела":
					self.case["id"] = value
				else:
					self.case["id"] = ""
				if name == "Номер заявления" or name == "Номер дела ~ материала":
					self.case["number"] = value
				else:
					self.case["number"] = ""
				if name == "Номер входящего документа":
					self.case["number_input_document"] = value
				else:
					self.case["number_input_document"] = ""
				if name == "Дата поступления":
					self.case["register_date"] = value
				else:
					self.case["register_date"] = ""
				if name == "Стороны":			
					participants_tag = div_row.find("div", class_="right")
					type_first = to_normal(participants_tag.find_all("strong")[0].text)
					name_first = to_normal(str(participants_tag).split(" </strong>")[1].split("<br/>")[0])
					if len(participants_tag.find_all("strong")) == 2:
						type_second = to_normal(participants_tag.find_all("strong")[1].text)
						name_second = to_normal(str(participants_tag).split("</strong>")[2].split("<br/>")[0])
						self.case['participants'] = [{"type": type_first, "name": name_first}, {"type": type_second, "name": name_second}]
					else:
						self.case['participants'] = [{"type": type_first, "name": name_first}]
				if name == "Cудья":
					self.case["judge"] = value
				else:
					self.case["judge"] = value
				if name == "Категория дела":
					self.case["category"] = value
				else:
					self.case["category"] = ""
				if name == "Текущее состояние":
					self.case["status"] = value
				else:
					self.case["status"] = ""
				
				# if name == "Дата поступления дела в апелляционную инстанцию":
				# 	self.case["date_of_appellate_instance"] = value
				# if name == "Номер судебного состава":
				# 	self.case["number_judge_team"] = value
				# if name = "Номер дела в суде нижестоящей инстанции":
				# 	self.case["number_case_last_instance"] = value
				# if name == "Номер дела в суде вышестоящей инстанции":
				# 	self.case["number_case_next_instance"] = value
				# if name == 
		# Движение дела
		self.case["history"] = []
		try:
			table = self.page.find("div", id="state-history").find("table", class_="custom_table margin-top-0 mainTable").find("tbody")
			for tr in table.find_all("tr"):
				tmp = {}
				td = tr.find_all("td")
				tmp["date"] = to_normal(td[0].text)
				tmp["status"] = to_normal(td[1].text)
				tmp["document"] = to_normal(td[2].text)
				self.case["history"].append(tmp)
		except AttributeError:
			pass

		
		# История местонахождения
		self.case["places_history"] = []
		try:
			table = self.page.find("div", id="state-history").find("table", class_="custom_table mainTable margin-top-0").find("tbody")
			for tr in table.find_all("tr"):
				tmp = {}
				td = tr.find_all("td")

				tmp["date"] = to_normal(td[0].text)
				tmp["place"] = to_normal(td[1].text)
				tmp["comment"] = to_normal(td[2].text)

				self.case["places_history"].append(tmp)
		except AttributeError:
			pass

		
		# Судебные заседания
		self.case["sessions"] = []
		try:
			table = self.page.find("div", id="sessions").find("table", class_="custom_table mainTable margin-top-0").find("tbody")
			for tr in table.find_all("tr"):
				tmp = {}
				td = tr.find_all("td")

				tmp["date"] = to_normal(td[0].text)
				tmp["hall"] = to_normal(td[1].text)
				tmp["stage"] = to_normal(td[2].text)
				tmp["result"] = to_normal(td[3].text)
				tmp["reson"] = to_normal(td[4].text)
				tmp["video"] = to_normal(td[5].text)

				self.case["sessions"].append(tmp)
		except AttributeError:
			pass

		# судебные акты
		
		self.case["documents"] = []
		try:
			table = self.page.find("div", id="act-documents").find("table", class_="custom_table mainTable").find("tbody")
			for tr in table.find_all("tr"):
				tmp = {}
				td = tr.find_all("td")

				tmp["date"] = to_normal(td[0].text)
				tmp["kind_document"] = to_normal(td[1].text)
				tmp["document_text"] = to_normal(td[2].text)

				self.case["documents"].append(tmp)
		except AttributeError:
			pass

	def to_json(self):
		return json.dumps(self.case, ensure_ascii=False, sort_keys=False)
