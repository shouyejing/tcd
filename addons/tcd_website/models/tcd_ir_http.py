# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import os
import re
import traceback

import werkzeug
import werkzeug.routing
import werkzeug.utils

import odoo
from odoo import api, models
from odoo import SUPERUSER_ID
from odoo.http import request
from odoo.tools import config
from odoo.exceptions import QWebException
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base import ir
from odoo.addons.website.models.website import slug, url_for, _UNSLUG_RE

from odoo.addons.website.models.ir_http import ModelConverter

logger = logging.getLogger(__name__)


class ModelConverter(ModelConverter):

    def to_url(self, value):
        logger.info("_____________________Let's slugify!!!!" + repr(value))
        logger.info("slugged: " + str(value.id))
        return str(value.id)
