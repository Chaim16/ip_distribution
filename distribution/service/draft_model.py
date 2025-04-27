import os
import time
import uuid

from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.forms import model_to_dict

from ip_distribution.utils.exception_util import BusinessException
from ip_distribution.utils.log_util import get_logger
from ip_distribution import settings
from distribution.models import User, Draft
from distribution.service.user_model import UserModel

logger = get_logger("ip_distribution")


class DraftModel(object):

    def publish(self, title, description, image, price, category_id, username):
        user = User.objects.get(username=username)
        user_id = user.id

        # 保存画稿图片
        image_name = image.name
        image_suffix = image_name.split('.')[-1]
        if image_suffix not in ["png", "jpg"]:
            raise BusinessException("图片格式不支持，请上传png或jpg格式图片")
        new_image_name = "{}.{}".format(str(uuid.uuid4()), image_suffix)
        image_url = os.path.join(settings.design_images_dir, new_image_name)
        with open(os.path.join(settings.design_images_dir, new_image_name), "wb") as f:
            for chunk in ContentFile(image.read()).chunks():
                f.write(chunk)
        logger.info("图片已保存至{}".format(image_url))
        params = {
            "title": title,
            "description": description,
            "image_url": image_url,
            "image_name": new_image_name,
            "price": price,
            "category_id": category_id,
            "designer_id": user_id,
            "online_time": int(time.time())
        }
        draft = Draft.objects.create(**params)
        logger.info("画稿已发布")
        return {"id": draft.id}

    def draft_list(self, page, size, **kwargs):
        draft_list = Draft.objects.filter().order_by("-id")
        if kwargs.get("category_id"):
            draft_list = draft_list.filter(category_id=kwargs.get("category_id"))
        if kwargs.get("designer_id"):
            draft_list = draft_list.filter(designer_id=kwargs.get("designer_id"))
        if kwargs.get("title"):
            draft_list = draft_list.filter(title__icontains=kwargs.get("title"))
        count = draft_list.count()
        paginator = Paginator(draft_list, size)
        draft_list = paginator.get_page(page)

        # 获取用户列表
        res = UserModel().user_list(1, 9999)
        user_list = res.get("list", [])
        user_map = {}
        for user in user_list:
            user_map[str(user.get("id"))] = user.get("username")

        data_list = []
        for item in draft_list:
            info = model_to_dict(item)
            info["designer"] = user_map.get(str(item.designer_id), "")
            data_list.append(info)
        return {"count": count, "list": data_list}


