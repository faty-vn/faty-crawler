from pathlib import PurePosixPath
from urllib.parse import urlparse
from itemadapter import ItemAdapter
import scrapy

from scrapy.pipelines.files import FilesPipeline


class MyFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return 'files/washington_law/' + PurePosixPath(urlparse(request.url).path).name

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        for file_url in adapter['file_urls']:
            yield scrapy.Request(file_url)
