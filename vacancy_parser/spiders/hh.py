import scrapy
from scrapy.http import HtmlResponse
from vacancy_parser.items import VacancyParserItem
from scrapy.loader import ItemLoader


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']

    '''Переинициализируем init для получения вакансии из runner'а.
    Закомментированная часть используется при работе через google colab, т.к. 
    в этом случае не требуется runner.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

	# строка для запуска через IDE или терминал
        self.start_urls = [f'https://spb.hh.ru/search/vacancy?text={kwargs.get("search")}&area=2&items_on_page=20']

	# 3 строки для запуска через Google Colab
        # search = 'data analyst'
        # city = '2' # Спб на сайте hh
        # self.start_urls = [f'https://spb.hh.ru/search/vacancy?text={search}&area={city}&items_on_page=20&page=0']

    '''При парсинге данных проверяем наличие следующей страницы и переходим на
    нее тем самым парсим все вакансии по заданному условию поиска, а также 
    парсим все вакансии и передаем внутреннюю ссылку в следующую функцию'''
    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='serp-item__title']")
        for link in links:
          yield response.follow(link, callback=self.parse_ads)

    '''По внутренней ссылке парсим все данные о вакансии и передаем их через 
    ItemLoader на обработку в items, чтобы разгрузить процессы.'''
    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=VacancyParserItem(), response=response)
        loader.add_xpath('name', "//h1[@data-qa='vacancy-title']/text()")
        loader.add_xpath('salary', "//div[@data-qa='vacancy-salary']/span/text()")
        loader.add_xpath('company', "//a[@data-qa='vacancy-company-name']/span/span/text() | //a[@data-qa='vacancy-company-name']/span/text()")
        loader.add_xpath('location', "//p[@data-qa='vacancy-view-location']/text() | //span[@data-qa='vacancy-view-raw-address']/text()")
        loader.add_xpath('experience', "//span[@data-qa='vacancy-experience']/text()")
        loader.add_xpath('description', "//div[@data-qa='vacancy-description']//p/text() | //div[@data-qa='vacancy-description']//li/text()")
        loader.add_xpath('date', "//p[@class='vacancy-creation-time-redesigned']/span/text()")
        loader.add_value('url', response.url)
        yield loader.load_item()
