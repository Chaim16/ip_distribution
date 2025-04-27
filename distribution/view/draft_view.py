import random
import traceback

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from ip_distribution.utils.constants_util import Role
from ip_distribution.utils.exception_util import BusinessException
from ip_distribution.utils.log_util import get_logger
from ip_distribution.utils.response import setResult
from ip_distribution.utils.validate import TransCoding
from distribution.service.draft_model import DraftModel
from distribution.service.user_model import UserModel
from distribution.view.serilazer import PublishDraftSerializer

logger = get_logger("home")


class DraftViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="发布画稿",
        request_body=PublishDraftSerializer,
        tags=["画稿中心"],
    )
    def publish(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = request.POST
        image = request.FILES.get("image", "")
        title = params.get("title", "")
        description = params.get("description", "")
        price = params.get("price", "")
        category_id = params.get("category_id", "")

        user_model = UserModel()
        draft_model = DraftModel()
        try:
            username = user.username
            user_dict = user_model.detail(username)
            if user_dict.get('role') == Role.GENERAL.value:
                raise BusinessException("权限不足")
            data = draft_model.publish(title, description, image, price, category_id, username)
            return setResult(data)
        except Exception as e:
            logger.error("发布画稿失败：{}".format(traceback.format_exc()))
            raise BusinessException("发布画稿失败")

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(
        operation_description="画稿列表",
        tags=['画稿中心']
    )
    def draft_list(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = TransCoding().transcoding_dict(dict(request.GET.items()))
        title = params.get("title", "")
        page = int(params.get('page', 1))
        size = int(params.get('size', 10))
        draft_model = DraftModel()
        try:
            data = draft_model.draft_list(page, size, title=title)
            return setResult(data)
        except Exception as e:
            logger.error("获取画稿列表失败：{}".format(traceback.format_exc()))
            raise BusinessException("获取画稿列表失败")

