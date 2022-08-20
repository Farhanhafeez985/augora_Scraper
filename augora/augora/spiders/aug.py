import json

from scrapy import Request, Spider


class AugoraSpider(Spider):
    name = "aug"

    base_url = "https://www.augora.at"
    api_url = 'https://www.augora.at/_api/wix-ecommerce-storefront-web/api'
    # start_urls=['https://www.augora.at/kaufen']
    headers = {
        'x-wix-linguist': 'de|de-at|true|0ef05f09-4a35-4c25-9041-3b03ae3e40ef',
        'Authorization': 'D8Wlj5LLAkuztPfuqZ7s0K4Ab5bTrXVC4uQWzzA-T9U.eyJpbnN0YW5jZUlkIjoiMGVmMDVmMDktNGEzNS00YzI1LTkwNDEtM2IwM2FlM2U0MGVmIiwiYXBwRGVmSWQiOiIxMzgwYjcwMy1jZTgxLWZmMDUtZjExNS0zOTU3MWQ5NGRmY2QiLCJtZXRhU2l0ZUlkIjoiNjVmZTY4NmMtYzNmMy00YTM0LWFkMTktZjY3YWE1YmI3MThkIiwic2lnbkRhdGUiOiIyMDIyLTA3LTIxVDA4OjM0OjAyLjE0NFoiLCJ2ZW5kb3JQcm9kdWN0SWQiOiJzdG9yZXNfYnJvbnplIiwiZGVtb01vZGUiOmZhbHNlLCJhaWQiOiI0NzZhZTg1Mi0xZmNjLTRmYzEtODZjZC1iNjhkNzAxYjAwMzgiLCJiaVRva2VuIjoiNmIwZTM3NjUtODljNi0wNjExLTNkNTgtY2Q3OTBiODUzMTYyIiwic2l0ZU93bmVySWQiOiJlMjVjNDg5Zi1iZmZhLTQwNzEtOThiOC1kNDFmYjk2YWYxZDUifQ',
        'Referer': 'https://www.augora.at/_partials/wix-thunderbolt/dist/clientWorker.2533056c.bundle.min.js',
        'X-XSRF-TOKEN': '1658392442|P1l-dDXoN-xg',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Content-Type': 'application/json; charset=utf-8'
    }
    custom_settings = {

        'FEED_EXPORT_ENCODING': 'UTF-8',
        # 'FEEDS': {
        #     f"{name}.csv": {"format": "csv"}
        # },
        'FEED_URI': f"{name}.xlsx",
        'FEED_FORMAT': 'xlsx',
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},

        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.102 Safari/537.36",

        'CONCURRENT_REQUESTS': 32,
        # "DOWNLOAD_DELAY": 3,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_crawlera.CrawleraMiddleware': 610,

        },

    }

    def start_requests(self):
        payload = self.get_request_parms({'offset': 0})
        yield Request(f'{self.api_url}{payload}', callback=self.parse, headers=self.headers, meta={"offset": 0})

    def get_request_parms(self, data):

        payload = """?o=getData&s=WixStoresWebClient&q=query,getData($externalId:String!,$compId:String!,$limit:Int!,$sort:ProductSort,$filters:ProductFilters,$offset:Int,$withOptions:Boolean,=,false,$withPriceRange:Boolean,=,false){appSettings(externalId:$externalId){widgetSettings}catalog{category(compId:$compId){id,name,productsWithMetaData(limit:$limit,onlyVisible:true,sort:$sort,filters:$filters,offset:$offset){list{id,options{id,key,title,@include(if:$withOptions),optionType,@include(if:$withOptions),selections,@include(if:$withOptions){id,value,description,key,linkedMediaItems{url,fullUrl,thumbnailFullUrl:fullUrl(width:50,height:50),mediaType,width,height,index,title,videoFiles{url,width,height,format,quality}}}}productItems,@include(if:$withOptions){id,optionsSelections,price,formattedPrice,formattedComparePrice,inventory{status,quantity}isVisible,pricePerUnit,formattedPricePerUnit}customTextFields(limit:1){title}productType,ribbon,price,comparePrice,sku,isInStock,urlPart,formattedComparePrice,formattedPrice,pricePerUnit,formattedPricePerUnit,pricePerUnitData{baseQuantity,baseMeasurementUnit}digitalProductFileItems{fileType}name,media{url,index,width,mediaType,altText,title,height}isManageProductItems,isTrackingInventory,inventory{status,quantity}subscriptionPlans{list{id,visible}}priceRange(withSubscriptionPriceRange:true),@include(if:$withPriceRange){fromPriceFormatted}discount{mode,value}}totalCount}}}}&v=%7B%22externalId%22%3A%22671377a0-a8bf-482c-97ae-73f5d316dd4e%22%2C%22compId%22%3A%22comp-klr0hifu%22%2C%22limit%22%3A80%2C%22sort%22%3Anull%2C%22filters%22%3Anull%2C%22offset%22%3A0%2C%22withOptions%22%3Afalse%2C%22withPriceRange%22%3Afalse%7D"""

        return payload

    def parse(self, response):

        data = json.loads(response.text)
        products = data['data']['catalog']['category']['productsWithMetaData']['list']
        total = data['data']['catalog']['category']['productsWithMetaData']['totalCount']

        for product in products:
            obj = {}
            obj['id'] = product['id']
            obj['title'] = product['name']
            obj['description'] = ''
            obj['link'] = f"https://www.augora.at/product-page/{product['urlPart']}"
            obj['price'] = f"{product['price']} EUR"
            obj['availability'] = "in_stock"
            # if product['isInStock'] == True:
            #
            #     obj['availability'] = "in_stock"
            # else:
            #     obj['availability'] = "out_of_stock"

            obj['image_link'] = f'https://static.wixstatic.com/media/{product["media"][0]["url"]}'
            obj['gtin'] = ''
            obj['mpn'] = ''
            obj['brand'] = 'Augora'
            obj['update_type'] = ''
            yield Request(url=f"https://www.augora.at/product-page/{product['urlPart']}", callback=self.product_page,
                          meta={"obj": obj})

    def product_page(self, response):

        text = response.css("script[type='application/ld+json']::text").get()
        obj = response.meta['obj']
        try:
            data = json.loads(text)
            obj['description'] = data['description']
        except:
            obj['description'] = ""

        yield obj
