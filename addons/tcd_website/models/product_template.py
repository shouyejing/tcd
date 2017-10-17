# -*- encoding: utf-8 -*-
# ############################################################################
#
#    Copyright Mars & Moore (C) 2016
#    Author: Mars & Moore
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import fields, models, api,tools, _
from openerp.exceptions import Warning
from odoo.modules.module import get_module_resource
import binascii
from odoo.tools.translate import html_translate


import logging
_logger = logging.getLogger(__name__)


def isodd(x):
    return bool(x % 2)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    name_product = fields.Char('Name Product', index=True, translate=True)
    name_generic = fields.Char('Name Generic', index=True, translate=True)
    teasing_description = fields.Html('Website Teasing Description', sanitize_attributes=False, translate=html_translate)

    # image: all image fields are base64 encoded and PIL-supported
    image_generic = fields.Binary(
        "Image Generic", attachment=True, default=lambda self:self._get_default_generic_image(),
        help="This field holds the image used as image for the product, if the user is not logged in, limited to 1024x1024px.")
    image_generic_medium = fields.Binary(
        "Medium-sized generic image", attachment=True,default=lambda self:self._get_default_generic_image_medium(),
        help="Medium-sized image of the product. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved, "
             "only when the image exceeds one of those sizes. Use this field in form views or some kanban views.")
    image_generic_small = fields.Binary(
        "Small-sized image", attachment=True,default=lambda self:self._get_default_generic_image_small(),
        help="Small-sized image of the product. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")

    @api.model
    def _get_default_generic_image(self, colorize=False):
        image = open(get_module_resource('tcd_website','static/img', 'sails.png')).read()

        return tools.image_resize_image_big(image.encode('base64'))

    @api.model
    def _get_default_generic_image_medium(self, colorize=False):
        image = open(get_module_resource('tcd_website','static/img', 'sails.png')).read()

        return tools.image_resize_image_medium(image.encode('base64'))

    @api.model
    def _get_default_generic_image_small(self, colorize=False):
        image = open(get_module_resource('tcd_website','static/img', 'sails.png')).read()

        return tools.image_resize_image_small(image.encode('base64'))

    @api.multi
    @api.onchange('image_generic')
    def _resize_image_generic(self):
        for image in self:
            try:
                image_64 = image.read().encode('base64')
                self.image_generic_medium = tools.image_resize_image_medium(image_64)
                self.image_generic_small = tools.image_resize_image_small(image_64)
            except binascii.Error:
                print "no correct base64"

    @api.one
    @api.depends("name_product","name_generic")
    def _calculate_name(self):
        _logger.info("current uid: " + str(self.env.uid))
        self.name = self.name_product if self.env.uid and self.env.uid !=3 else self.name_generic