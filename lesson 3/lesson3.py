from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
vacancies_db = db.vacancies
#db.vacancies.find({})
#1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД.
#Приложила скрин созданной базы данных

#2.Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
#Поиск должен происходить по 2-ум полям (минимальной и максимальной зарплате)
#Я написала запрос, как по условию, но в моей программе указан массив salary, внутри которого мин и макс
#и получается обращаться надо к salary

#Поиск по salary_min и salary_max
salary = int(input('Введите критерии зарплаты: '))
def filter_salary(vacancies_db, salary) :
    for vacancy in vacancies_db.find({'$or': [{'salary_max': {'$gte': salary}},
                                            {'salary_max': {'$lte': salary}}]}):
        pprint(vacancy)

#Для поиску по salary
salary_general = int(input('Введите критерии зарплаты: '))
def filter_salary_2(vacancies_db, salary_general) :
    for vacancy in vacancies_db.find({'salary': {'$gte': salary_general}}):
        pprint(vacancy)

#3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
def new_vacancies(vacancies, vacancies_db):
    try:
        if len(vacancies) > 0:
            for vacancy in vacancies:
                vacancies_db.update_one({'link': vacancy['link']}, {'$set': vacancy}, upsert=True)
        return False
    except Exception as E:
        return E