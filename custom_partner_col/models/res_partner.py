# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_nit = fields.Char(string="NIT")
    partner_dv = fields.Char(string="Digito de Verificacion")
