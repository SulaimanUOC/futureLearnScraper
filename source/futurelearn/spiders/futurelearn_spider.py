import scrapy
from futurelearn.items import CourseItem

class RecetasSpider(scrapy.Spider):
    name = "futurelearn"

    allowed_domains = ["www.futurelearn.com"]

    start_urls = [
        "https://www.futurelearn.com/courses"
    ]

    def parse(self, response):
        for course_url in extract_courses_urls(response):
            yield scrapy.Request(course_url, callback=self.parse_course)

        next_url = extract_next_url(response)
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_course(self, response):
        course = CourseItem()

        course["name"] = extract_course_name(response)
        course["category"] = extract_course_category(response)
        course["organization"] = extract_course_organization(response)
        course["score"] = extract_course_score(response)
        course["reviews"] = extract_course_reviews(response)
        course["duration"] = extract_course_duration(response)
        course["weekly_study"] = extract_course_weekly_study(response)
        course["accreditation"] = extract_course_accreditation(response)
        course["subscription_type"], course["subscription_price"] = extract_course_subscription(response)

        yield course

def extract_course_name(response):
    return response.xpath('//div[@id="section-page-header"]//h1/text()').extract()[0]

def extract_course_category(response):
    return response.xpath('//li[@class="breadcrumbs-module_item__3SxlK"]//span/text()').extract()[1]

def extract_course_organization(response):
    return response.xpath('//section[@id="section-creators"]//h2/text()').extract()[1]

def extract_course_score(response):
    return response.xpath('//div[@id="section-page-header"]//div[contains(@class, "ReviewStars-text")]/text()').extract_first()

def extract_course_reviews(response):
    # the review text is divided in 3 sections, separated by HTML comments,
    # for example "(<!---->14<!---->reviews)", so we need to get all
    # the pieces of text and get the second one
    review_texts = response.xpath('//div[@id="section-page-header"]//div[contains(@class, "ReviewStars-text")]/span/text()').getall()
    if review_texts:
        return review_texts[1]

    return None

def extract_course_duration(response):
    return extract_from_course_metadata(response, "Duration")

def extract_course_weekly_study(response):
    return extract_from_course_metadata(response, "Weekly study")

def extract_course_accreditation(response):
    value = extract_from_course_metadata(response, "Accreditation")
    return value == "Available"

def extract_from_course_metadata(response, section):
    value = response.xpath('//div[@id="sticky-banner-start"]//p[text()="{}"]/following-sibling::span/text()'.format(section)).getall()

    if len(value) == 0:
        value = response.xpath('//div[@id="section-page-header"]//p[text()="{}"]/following-sibling::span/text()'.format(section)).getall()

    return "".join(value)

def extract_course_subscription(response):
    price = extract_from_course_metadata(response, "Unlimited subscription")
    if price:
        return "Unlimited subscription", price
    
    price = extract_from_course_metadata(response, "Premium course")
    if price:
        return "Premium course", price

    price = extract_from_course_metadata(response, "Digital upgrade")
    if price:
        return "Digital upgrade", price

    value = extract_from_course_metadata(response, "Included in an ExpertTrack")
    if value:
        price = extract_from_course_metadata(response, "Get full ExpertTrack access")
        return "Part of ExpertTrack", price

    return None

def extract_courses_urls(response):
    refs = response.xpath('//div[@class="cardGrid-wrapper_2TvtF cardGrid-hasSideNav_1sLqj"]//a[@class="index-module_anchor__24Vxj"]/@href').extract()

    for ref in refs:
        course_url = response.urljoin(ref)
        yield course_url

def extract_next_url(response):
    next_url_path = response.xpath('//li[@class="pagination-module_itemNext__2nfTV"]/a/@href').extract_first()
    if next_url_path:
        next_url = response.urljoin(next_url_path)
        return next_url
    return None
