from itemadapter import ItemAdapter
import csv 
# from pymongo import MongoClient # монго перстал отвечать в колабе


# class VacancyParserPipeline:
#     '''При инициализации сразу запускаем клиент mongo'''
#     def __init__(self):
#         client = MongoClient('localhost:27017')
#         self.mongo_db = client.vacancy_parser

#     '''В пайплайне создаем коллекцию по имени паука и добавляем туда спарсенные данные'''
#     def process_item(self, item, spider):
#         collection = self.mongo_db[spider.name]
#         collection.insert_one(item)
#         return item

class CSVPipeline(object):
    # конструктор
    def __init__(self):
        self.file = 'database.csv' # файл надо создать заранее
        with open(self.file, 'r', newline='') as csv_file: # если поменять 'r' на 'w' - можно создать файл, но нужно делать в режиме дебага
            self.tmp_data = csv.DictReader(csv_file).fieldnames # метод DictReader читает файл и возвращает построчное содержимое файла, не считая заголовки, а fieldnames - только заголовки
        
        self.csv_file = open(self.file, 'a', newline='', encoding='UTF-8') # открываем файл на дозапись ('a') при инициализации

    def process_item(self, item, spider):
        columns = item.fields.keys() # ключи словаря будут названиями колонок в csv

        data = csv.DictWriter(self.csv_file, columns)
        if not self.tmp_data: # если файл пустой
            data.writeheader() # метод сам возьмет передаваемые columns и запишет в header таблицы
            self.tmp_data = True # меняем значение проверки, чтобы второй раз сюда не попасть
        data.writerow(item)

        return item

    # деструктор
    def __del__(self):
        self.csv_file.close() # закрываем файл в конце пайплайна
