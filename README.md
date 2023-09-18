# Vacancy_parser

Представляю вам парсер, позволяющий собирать информацию о вакансиях с сайта hh.ru. 

Парсер может быть запущен 3 способами:

1) Через любую IDE - скачать файлы / распаковать архив и запустить runner.py.

2) Через терминал - скачать файлы / распаковать архив, в термпинале запустить runner.py и через пробел ввести искомую вакансию, но для этого придется перекомментировать пару строк в runner.py (внутри файла оставлен соответствующий комментарий).

3) Через Google.colab - скопировать архив vacancy_parser в колаб, запустить команды ниже на исполнение. Для этого варианта не требуется runner.py, но придется перекомментировать пару строк внутри паука hh.py (внутри файла оставлен соответствующий комментарий).

!pip install scrapy 

!unzip vacancy_parser.zip 

!scrapy crawl hh

Все полученные данные складываются в database.csv. Далее всю собранную информацию можно обрабатывать используя, например, pandas. Альтернативно данные могут складываться в БД MongoBD (необходимо раскомментировать соответствующие строки в items.py и settings.py), но через google colab монгодб перестал отвечать, поэтому я сделал его не основным вариантом. Для чтения из Монго ДБ необходимо установить у себя PyMongo.

Комментарии по работе парсера можно найти в коде. Спасибо.
