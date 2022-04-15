import json
url = "https://mos-gorsud.ru/rs/lyublinskij/search?formType=shortForm&courtAlias=basmannyj&uid=&instance=2&processType=1&category=&letterNumber=&caseNumber=&participant="


from courts_case import SearchCase
search = SearchCase(url)
search.get_cases()
#search.to_json()
print(json.dumps(search.to_json(), indent=4))