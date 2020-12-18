from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import requests
import re
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['jobs']
jobs = db.jobs

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

main_link = 'https://hh.ru'

link = f'{main_link}/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=python'

response = requests.get(link, headers=headers)
soup = bs(response.text,'html.parser')

#Функция, которая создает базу данных
def db_vacancy(vacancy_name, vacancy_city, vacancy_salary, vacancy_link):
    jobs.insert_one({'name': vacancy_name,
                     'city': vacancy_city,
                     'link': vacancy_link,
                     'salary': vacancy_salary})
if response.ok:
    vacancies_list = soup.findAll('div', {'data-qa':'vacancy-serp__vacancy'})
    vacancies = []
for vacancy in vacancies_list:
    vacancy_data = {}
    vacancy_name = vacancy.find('span',{'class':'resume-search-item__name'})
    vacancy_city = vacancy.find('span', {'class': 'vacancy-serp-item__meta-info'})
    vacancy_link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
    vacancy_salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'})
    if not vacancy_salary:
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        vacancy_salary = vacancy_salary.getText() \
            .replace(u'\xa0', u'')

        vacancy_salary = re.split(r'\s|-', vacancy_salary)

        if vacancy_salary[0] == 'до':
            salary_min = None
            salary_max = int(vacancy_salary[1])
        elif vacancy_salary[0] == 'от':
            salary_min = int(vacancy_salary[1])
            salary_max = None
#У меня не получилось добавить исключение по зарплате,
#потому что выдает ошибку "ValueError: invalid literal for int() with base 10: ''"
#поэтому я просто указала salary и он показывает от и до, либо пустое значение при зп 'не указано'

    vacancy_data['salary'] = vacancy_salary
    vacancy_data['name'] = vacancy_name.text
    vacancy_data['city'] = vacancy_city.text
    vacancy_data['link'] = vacancy_link['href']
    vacancies.append(vacancy_data)

pprint(vacancies)

