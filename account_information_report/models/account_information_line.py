from odoo import fields, models, tools, api
from datetime import datetime

import logging

_logger = logging.getLogger(__name__)


class AccountInformationReportLine(models.Model):
    """ Account SQL Information Report"""

    _name = "account.information.line.report"
    _auto = False
    _description = " Account SQL Information Report"
    _rec_name = "date"

    date = fields.Date(string="Date", readonly=True)

    partner_nit = fields.Char(string="Nit", readonly=True)
    partner_dv = fields.Char(string="Verification Digit", readonly=True)
    partner_name = fields.Char(string="Name", readonly=True)
    partner_street = fields.Char(string="Street", readonly=True)
    partner_phone = fields.Char(string="Phone", readonly=True)
    partner_state = fields.Char(string="State", readonly=True)
    partner_city = fields.Char(string="City", readonly=True)

    product_id = fields.Many2one(
        "product.product", string="Product", readonly=True
    )
    product_qty = fields.Float(
        string="Kg", readonly=True, digits=(16, 2), default=0
    )
    currency_id = fields.Many2one(
        "res.currency", string="Currency", readonly=True
    )
    amount = fields.Float(
        string="Total", store=True, digits=(16, 2), default=0, readonly=True
    )

    def _get_dates_context(self):
        date_start = datetime.today().strftime("%Y-%m-%d")
        date_end = datetime.today().strftime("%Y-%m-%d")

        if self._context.get("date_start"):
            date_start = self._context.get("date_start")
        if self._context.get("date_end"):
            date_end = self._context.get("date_end")
        return (date_start, date_end)

    def _select(self):
        query = """
        SELECT row_number() OVER ()::integer AS id,
    NULL::timestamp without time zone AS create_date,
    NULL::integer AS create_uid,
    NULL::timestamp without time zone AS write_date,
    NULL::integer AS write_uid,
    i.date_invoice AS date,
    rp.partner_nit AS partner_nit,
    rp.partner_dv AS partner_dv,
    rp.name as partner_name,
    rp.street AS partner_street,
    rp.phone AS partner_phone,
    rcs.name AS partner_state,
    rp.city as partner_city,
    l_1.product_id AS product_id,
    l_1.quantity AS product_qty,
    i.currency_id AS currency_id,
    l_1.price_subtotal AS amount
    FROM account_invoice i
        INNER JOIN account_invoice_line l_1 ON i.id = l_1.invoice_id
        INNER JOIN product_product p
        ON l_1.product_id = p.id
        INNER JOIN res_partner rp ON 
        i.partner_id = rp.id
        INNER JOIN account_journal acj
        ON i.journal_id = acj.id
        FULL JOIN res_country_state rcs ON
        rp.state_id = rcs.id
        WHERE acj.type = 'purchase' AND
        (i.state = 'open' OR i.state = 'paid') 
        -- AND i.date_invoice BETWEEN %s AND
        -- %s
                """
        return query

    def _init_account_information_line_view(self):
        tools.drop_view_if_exists(self.env.cr, self._table)

        # query_account_params = self._get_dates_context()
        self.env.cr.execute(
            """CREATE VIEW %s AS (
            %s
        )"""
            % (self._table, self._select()),
            # query_account_params,
        )

    @api.model_cr
    def init(self):
        self._init_account_information_line_view()

