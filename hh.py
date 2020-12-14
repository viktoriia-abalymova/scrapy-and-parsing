from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

main_link = 'https://hh.ru'
params = {
        'L_save_area': 'true',
        'clusters': 'true',
        'enable_snippets': 'true',
        'text': 'Python',
        'showClusters': 'true'
    }
link = f'{main_link}/search/vacancy'

response = requests.get(link, params=params, headers=headers)
soup = bs(response.text,'html.parser')

if response.ok:
    vacancies_list = soup.findAll('div', {'class': 'vacancy-serp_vacancy'})
    vacancies = []
for vacancy in vacancies_list:
    vacancy_data['name'] = vacancy_name.text
    vacancy_data['salary'] = vacancy_salary
    vacancy_data['link'] = vacancy_link

    vacancies.append(vacancy_data)
    vacancy_data = {}
    vacancy_name = vacancy.find('span',{'class':'resume-search-item__name'})
    vacancy_link = vacancy_name['href']
try:
        vacancy_salary= float(('div',{'class':'vacancy-serp-item__compensation'}).text)
except:
        vacancy_salary= None

pprint(vacancies)

