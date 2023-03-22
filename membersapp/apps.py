# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models import BigAutoField

class MembersappConfig(AppConfig):
    default_auto_field = BigAutoField
    name = 'membersapp'

