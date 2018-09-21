# -*- coding: utf-8 -*-
# Created by crazyX on 2018/9/20
import logging

from django.contrib.auth import user_logged_in, user_login_failed
from django.dispatch import receiver

from account.models import User

from core.models import UserLoginActivity
from core.utils import get_client_ip

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    print("signal:", user)
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
        user_login_activity_log = UserLoginActivity(login_IP=get_client_ip(request),
                                                    login_username=user.username,
                                                    user_agent_info=user_agent_info,
                                                    status=UserLoginActivity.SUCCESS)
        user_login_activity_log.save()
        User.objects.filter(id=user.id).update(date_active=user_login_activity_log.login_datetime)
    except Exception as e:
        # log the error
        logger.error("log_user_logged_in request: %s, error: %s" % (request, e))


@receiver(user_login_failed)
def log_user_logged_in_failed(sender, credentials, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
        user_login_activity_log = UserLoginActivity(login_IP=get_client_ip(request),
                                                    login_username=credentials['username'],
                                                    user_agent_info=user_agent_info,
                                                    status=UserLoginActivity.FAILED)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        logger.error("log_user_logged_in request: %s, error: %s" % (request, e))
