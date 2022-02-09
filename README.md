# 房市监测

## 武汉

数据源：[每日新建商品房成交统计情况](http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/index.shtml)

```shell
docker run -p 8050:8050 scrapinghub/docker
scrapy crawl link_spider -O links.jl
scrapy crawl table_spider -O tables.jl
```
