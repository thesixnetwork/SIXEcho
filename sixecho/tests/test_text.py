from sixecho import Client, Text

a = Text()
a.generate(txtpath="sample.txt")

meta_books = {
    "category_id": "1",
    "publisher_id": "1",
    "title": "100 คมธรรม พุทธทาสภิกขุ-2",
    "author": "บัญชา เฉลิมชัยกิจ",
    "country_of_origin": "THA",
    "language": "th",
    "paperback": "307",
    "publish_date": 1565252419
}

a.set_meta(meta_books)
client = Client(
    host_url=
    "https://mc64byvj0i.execute-api.ap-southeast-1.amazonaws.com/prod/",
    api_key="4S8Vps2d7t3FiYgt07lQL1i620JRR8Ena0DWhVmv",
)
client.upload('123456789theeratnon', a)
