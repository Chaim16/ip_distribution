import random

from ip_distribution.utils.exception_util import BusinessException
from ip_distribution.utils.log_util import get_logger
from ip_distribution import settings
from distribution.models import Crawler

logger = get_logger("user")


class HomeModel(object):

    def crawler(self, number):
        if number > 10:
            raise BusinessException("不能一次性获取超过10条数据")
        random_numbers = random.sample(range(0, 10), number)
        crawlers = Crawler.objects.filter(id__in=random_numbers)
        res = {"images": []}
        for item in crawlers:
            res["images"].append({
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "image_path": settings.STATIC_URL + item.image_path,
            })
        return res
