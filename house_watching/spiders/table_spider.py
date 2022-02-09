import scrapy
import json
import datetime


def retrieve_date(title):
    pre = title.split("日")[0]
    pre, day = pre.split("月")
    year, month = pre.split("年")
    return str(datetime.date(int(year), int(month), int(day)))


class Row:
    def __init__(self, cells):
        self.valid = True
        n_cells = len(cells)
        if n_cells != 11 and n_cells != 21:
            self.valid = False
            return
        self.district = cells[0].xpath(".//text()").get()
        if self.district == "合计":
            self.valid = False
            return

        try:
            if n_cells == 11:
                self.commercial_house_quantity = int(cells[1].xpath(".//text()").get())
                self.commercial_house_area = float(cells[2].xpath(".//text()").get())
                self.office_building_quantity = int(cells[3].xpath(".//text()").get())
                self.office_building_area = float(cells[4].xpath(".//text()").get())
                self.business_quantity = int(cells[5].xpath(".//text()").get())
                self.business_area = float(cells[6].xpath(".//text()").get())
                self.other_quantity = int(cells[7].xpath(".//text()").get())
                self.other_area = float(cells[8].xpath(".//text()").get())
            elif n_cells == 21:
                self.commercial_house_quantity = int(cells[3].xpath(".//text()").get())
                self.commercial_house_area = float(cells[4].xpath(".//text()").get())
                self.office_building_quantity = int(cells[7].xpath(".//text()").get())
                self.office_building_area = float(cells[8].xpath(".//text()").get())
                self.business_quantity = int(cells[11].xpath(".//text()").get())
                self.business_area = float(cells[12].xpath(".//text()").get())
                self.other_quantity = int(cells[15].xpath(".//text()").get())
                self.other_area = float(cells[16].xpath(".//text()").get())
        except Exception:
            self.valid = False

    def to_dict(self):
        return {
            "商品住房": [self.commercial_house_quantity, self.commercial_house_area],
            "写字楼": [self.office_building_quantity, self.office_building_area],
            "商业": [self.business_quantity, self.business_area],
            "其他": [self.other_quantity, self.other_area]
        }


class LinkSpider(scrapy.Spider):
    name = "table_spider"

    def start_requests(self):
        with open("links.jl", "r") as f:
            links = f.readlines()
        nlinks = len(links) - 1
        for idx, line in enumerate(links):
            link = json.loads(line)
            print(f"progress: {idx}/{nlinks}")
            yield scrapy.Request(url=link["url"], callback=self.parse)

    def parse(self, response):
        title = response.xpath("//div[@class='article downwrap']/h2/text()").get()
        date = retrieve_date(title)
        rows = response.xpath("//tbody/tr")
        data = {}
        for row in rows:
            cells = row.xpath(".//td")
            r = Row(cells)
            if r.valid:
                data[r.district] = r.to_dict()
                if not data[r.district]:
                    print("empty data")
        yield {
            "date": date,
            "table": data
        }
