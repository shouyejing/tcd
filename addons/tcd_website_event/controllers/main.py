import babel.dates
import time
import re
import werkzeug.urls
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from openerp import http
from openerp import tools, SUPERUSER_ID
from openerp.addons.website.models.website import slug
from openerp.http import request
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class website_event(http.Controller):
    @http.route([
        '/event/<model("event.event"):event>/partner/<model("res.partner"):partner>/register',
        '/event/<model("event.event"):event>/partner/<model("res.partner"):partner>/register/m/<int:mail>',
        '/event/<model("event.event"):event>/partner_id/<model("res.partner"):partner>/register/m/<int:mail>',

    ], type='http', auth="public", website=True)
    def event_register(self, event, partner="null", mail=0):
        cr, uid, context = request.cr, request.uid, request.context
        invitation_answered_obj = http.request.env['event.invitee']
        if invitation_answered_obj.search_count([('event_id','=',event.id),('partner_id','=',partner.id)]) > 0:
            invitation_answered = invitation_answered_obj.search([('event_id','=',event.id),('partner_id','=',partner.id)])[0]
        else:
            invitation_answered = False
        _logger.debug("Invitation answered : " + repr(invitation_answered))

        values = {
            'partner': partner,
            'event': event,
            'main_object': event,
            'range': range,
            'invitation_answered': invitation_answered,
        }
        return request.website.render("website_event.event_description_full", values)

    @http.route(['/event/<model("event.event"):event>/partner/<model("res.partner"):partner>/invitation/confirm'], type='http', auth="public",
                methods=['POST'], website=True)
    def invitation_confirm(self, event, partner, **post):
        for a in post:
            _logger.debug("current post: " + str(a) + "    " + str(post[a]))
        cr, uid, context, params = request.cr, request.uid, request.context, request.params
        _logger.debug("current comments: "+ repr(params))

        Invitation = request.registry['event.invitee']
        registration = post
        registration['event_id'] = event.id
        registration['partner_id'] = partner.id
        _logger.debug("current registration: " + repr(registration))
        Invitation.create(cr, uid, registration, context=context)

        return request.redirect('/event/' + str(event.id) + '/partner/' + str(partner.id) + '/register')


