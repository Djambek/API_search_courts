import requests
from bs4 import BeautifulSoup as bs
import json

def to_normal(text:str) -> str:
	return text.replace("  ", "").replace("\n", "") # надо изучить регулярки

class SearchCase():
	def __init__(self, link:str):
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		request = requests.get(link, headers=headers)
		self.page = bs(request.text, 'html.parser')
		with open("m.html", "w") as f:
			f.write(request.text)
			f.close()
		self.cases = {'cases':[]}
	def get_cases(self):
		form = self.page.find("div", class_="searchResultContainer")
		if form.find("div", class_="paginationContainer") is None:
			self.cases["pages"] = 1
		else:		
			self.cases["pages"] = form.find("div", class_="paginationContainer").find("li", class_="active").find("form", id="paginationForm").text.split()[2]
			#print(form.find("div", class_="paginationContainer"))
		table_container = self.page.find("div", class_="wrapper-search-tables")
		#print(table_container)
		for table in self.page.find_all("div", class_="wrapper-search-tables"):
			#print(table)
			for tbody in table.find_all("tbody"):
				for tr in tbody.find_all("tr"):
					tmp = {}
					td = tr.find_all("td")

					#ссылка на дело
					tmp['url'] = "https://mos-gorsud.ru"+to_normal(td[0].find("nobr").find("a")['href'])


					# номер дела
					#print()
					tmp['number'] = to_normal(td[0].find("nobr").find("a").text)


					# истец и ответчик || стороны
					#print(td[1].find("div", class_="row_card"))
					participants_tag = td[1].find("div", class_="row_card").find("div", class_="right")
					type_first = to_normal(participants_tag.find_all("strong")[0].text)
					name_first = to_normal(str(participants_tag).split(" </strong>")[1].split("<br/>")[0])
					if len(participants_tag.find_all("strong")) == 2:
						type_second = to_normal(participants_tag.find_all("strong")[1].text)
						name_second = to_normal(str(participants_tag).split("</strong>")[2].split("<br/>")[0])
						tmp['participants'] = [{"type": type_first, "name": name_first}, {"type": type_second, "name": name_second}]
					else:
						tmp['participants'] = [{"type": type_first, "name": name_first}]
					# Статус дела
					tmp["status"] = to_normal(td[2].find("div", class_="table-row-wrap").find("div", class_="table-row-content").text)

					# Судья
					tmp["judge"] = to_normal(td[3].find("div", class_="table-row-wrap").find("div", class_="table-row-content").text)

					# Категория дела
					tmp["category"] = to_normal(td[5].find("div", class_="table-row-wrap").find("div", class_="table-row-content").text)
					self.cases['cases'].append(tmp)


	def to_json(self):
		return json.dumps(self.cases, ensure_ascii=False)

	def write_file(self):
		with open('data.json', 'w', encoding="utf-8") as f:
			json.dump(self.cases, f, ensure_ascii=False)


