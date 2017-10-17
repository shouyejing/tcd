from openerp import api, fields, models

import logging
_logger = logging.getLogger(__name__)

ANSWERS = [
    ('0', 'No'),
    ('1', 'Yes'),
    ('2', 'Yes, Accompanied by'),
]
TITLES = [
    ('Mrs', 'Mrs'),
    ('Miss', 'Miss'),
    ('Mr', 'Mr'),
]

class Event(models.Model):
    _inherit = 'event.event'

    invitee_ids=fields.One2many('event.invitee',"partner_id","Participants")
    invitee_count = fields.Integer('Number of participants',
                                   compute='_count_invitee')
    @api.depends('invitee_ids')
    def _count_invitee(self):
        invitees = self.env['event.invitee'].search([('event_id','=',self.id)])
        total_participants = 0
        for invitee in invitees:
            total_participants += int(invitee.answer)
            self.invitee_count = total_participants


class EventInvitee(models.Model):
    _name = 'event.invitee'

    website_form_access = True

    event_id = fields.Many2one('event.event', string="Event", required=True)
    partner_id = fields.Many2one('res.partner', string="Invitee", required=True)
    answer = fields.Selection(ANSWERS, required = True)
    guest_title = fields.Selection(TITLES, string="Guest Appellation")
    guest_firstname = fields.Char(string="Guest First Name")
    guest_lastname = fields.Char(string="Guest Last Name")
    guest_email = fields.Char(string="Guest Email")
    comments = fields.Char(string="Comments")
    nbr_participants = fields.Integer('Number participants', compute="_nbr_participants")
    participant_id = fields.Many2one('res.partner', string="Participant", compute="_compute_participant_id", store=True)

    @api.one
    def _nbr_participants(self):
        self.nbr_participants = int(self.answer)

    @api.depends("partner_id","answer")
    def _compute_participant_id(self):
        for participant in self:
            if participant.answer != "0":
                _logger.debug("answer is not no!")
                participant.participant_id = participant.partner_id


    # @api.multi
    # def button_reg_cancel(self):
    #     if self.env.context.get('bypass_reason'):
    #         return super(EventRegistration, self).button_reg_cancel()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Cancellation reason',
    #         'res_model': 'event.registration.cancel.log.reason',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'target': 'new',
    #     }
    #
    # @api.multi
    # def do_draft(self):
    #     super(EventRegistration, self).do_draft()
    #     self.write({'cancel_reason_id': False})

class link_tracker(models.Model):
    _inherit = "link.tracker"

    @api.model
    def convert_links(self, html, vals, blacklist=None):
        return html

class ResPartner(models.Model):
    _inherit = 'res.partner'

    event_invitee_ids = fields.One2many('event.invitee', 'participant_id', string="Events")
