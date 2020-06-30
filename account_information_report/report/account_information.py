# -*- coding: utf-8 -*-

from odoo import api, models


class AccountInformationReport(models.AbstractModel):
    _name = "report.account_information_report.report_account_information"

    @api.model
    def get_report_values(self, docids, data=None):

        return {
            "doc_ids": data["account_ids"],
            "doc_model": self.env["account.invoice"],
            "data": data,
            "docs": self.env["account.invoice"].browse(data["account_ids"]),
        }
