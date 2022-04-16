import json
url = "https://mos-gorsud.ru/rs/lyublinskij/search?formType=shortForm&courtAlias=basmannyj&uid=&instance=&processType=&category=&letterNumber=&caseNumber=&participant="


from courts_case import SearchCase
from details import Details
#search = SearchCase(url)
#search.get_cases()
#search.to_json()
#print(search.to_json())
d = Details("https://mos-gorsud.ru/rs/basmannyj/services/cases/civil/details/783ed0b1-bd62-11ec-808d-1bd22efd743d")
d.get_info()
print(d.to_json())