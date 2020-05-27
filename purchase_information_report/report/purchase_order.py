# -*- coding: utf-8 -*-

from odoo import api, models


class PurchaseInformationReport(models.AbstractModel):
    _name = "report.purchase_information_report.report_purchase_information"

    @api.model
    def get_report_values(self, docids, data=None):

        return {
            "doc_ids": data["purchase_ids"],
            "doc_model": self.env["purchase.order"],
            "data": data,
            "docs": self.env["purchase.order"].browse(data["purchase_ids"]),
        }
