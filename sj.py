from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_link = 'https://russia.superjob.ru'
params = {
        'keywords': 'python'
    }
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
link = f'{main_link}/vacancy/search/'

response = requests.get(link, params=params, headers=headers)
soup = bs(response.text,'html.parser')

if response.ok:
    vacancies_list = soup.findAll('div', {'class': 'f-test-vacancy-item'})
    vacancies = []
    for vacancy in vacancies_list:
        vacancy_data = {}
        vacancy_name = vacancy.find('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'})
        vacancy_link = vacancy_name['href']
        try:
            vacancy_salary = float(('span',{'class': '_1OuF_ _1qw9T f-test-text-company-item-salary'}).text)
        except:
            vacancy_salary = None

        vacancy_data['name'] = vacancy_name.text
        vacancy_data['salary'] = vacancy_salary
        vacancy_data['link'] = vacancy_link

        vacancies.append(vacancy_data)

    pprint(vacancies)