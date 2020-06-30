# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import xlwt
import base64
import calendar
from datetime import datetime

import logging

_logger = logging.getLogger(__name__)


class AccountReportCustom(models.TransientModel):
    _name = "account.information.report"

    start_date = fields.Date(
        string="Period Start",
        # required=True,
        default=datetime.today().replace(day=1),
    )
    periodo_mes = fields.Selection(
        [
            (1, "ENERO"),
            (2, "FEBRERO"),
            (3, "MARZO"),
            (4, "ABRIL"),
            (5, "MAYO"),
            (6, "JUNIO"),
            (7, "JULIO"),
            (8, "AGOSTO"),
            (9, "SEPTIEMBRE"),
            (10, "OCTUBRE"),
            (11, "NOVIEMBRE"),
            (12, "DICIEMBRE"),
        ],
        string="Period Month",
        required=True,
        default=1,
    )
    periodo_year = fields.Selection(
        [(num, str(num)) for num in range(2018, (datetime.now().year) + 1)],
        string="Period Year",
        required=True,
        default=datetime.now().year,
    )

    report_bank = fields.Many2one("res.bank", string="Bank")
    report_sign = fields.Boolean(string="¿Sign pdf?", default=False)

    @api.multi
    def generated_excel_report(self, record):

        date = str(self.periodo_year) + "-" + str(self.periodo_mes) + "-01"
        date_start, date_end = self._format_dates(date)

        # actual_date = datetime.today()

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(
            "Reporte de información", cell_overwrite_ok=True
        )
        accounts = self.env["account.invoice"].search(
            [
                ("date_invoice", ">=", date_start),
                ("date_invoice", "<=", date_end),
                ("journal_id.type", "=", "purchase"),
            ]
        )

        user = self.env["res.users"].browse(self._uid)

        # #########
        # FORMATOS
        # #########
        formatR = xlwt.easyxf(
            "font:bold True, height 190;align: horiz center;"
            "pattern: pattern solid, fore_color light_green;"
            "borders: top_color black, bottom_color black, right_color black,"
            "left_color black,left thin, right thin, top thin, bottom thin;"
        )
        format2 = xlwt.easyxf(
            "font:bold True, height 190;align: horiz left;"
            "pattern: pattern solid, fore_color light_green;"
            "borders: top_color black, bottom_color black, right_color black,"
            "left_color black,left thin, right thin, top thin, bottom thin;"
        )
        format3 = xlwt.easyxf(
            "font:height 190;align: horiz right;"
            "borders: top_color black, bottom_color black, right_color black,"
            "left_color black,left thin, right thin, top thin, bottom thin;"
        )
        format4 = xlwt.easyxf(
            "font:height 190;align: horiz right;"
            "borders: top_color black, bottom_color black, right_color black,"
            "left_color black,left thin, right thin, top thin, bottom thin;",
            num_format_str="'$#,##0.00'",
        )
        format_content = xlwt.easyxf(
            "font:height 180;align: horiz left;"
            "borders: top_color black, bottom_color black, right_color black,"
            "left_color black,left thin, right thin, top thin, bottom thin;",
        )

        # #########
        # CABECERA
        ###########
        sheet.write(0, 0, "NIT", format2)
        sheet.write(0, 1, "DV", format2)
        sheet.write(0, 2, "NOMBRE", format2)
        sheet.write(0, 3, "DIRECCIÓN", format2)
        sheet.write(0, 4, "TELÉFONO", format2)
        sheet.write(0, 5, "DEPARTAMENTO", format2)
        sheet.write(0, 6, "MUNICIPIO", format2)
        sheet.write(0, 7, "PRODUCTO", format2)
        sheet.write(0, 8, "KILOS", format2)
        sheet.write(0, 9, "VALOR", format2)

        # ###############
        # COLUMNAS ANCHO
        # ###############
        sheet.col(0).width = 700 * (len("NIV") + 1)
        sheet.col(1).width = 500 * (len("DV") + 1)
        sheet.col(2).width = 700 * (len("NOMBRE") + 1)
        sheet.col(3).width = 700 * (len("DIRECCION") + 1)
        sheet.col(4).width = 700 * (len("TELÉFONO") + 1)
        sheet.col(5).width = 700 * (len("DEPARTAMENTO") + 1)
        sheet.col(6).width = 700 * (len("MUNICIPIO") + 1)
        sheet.col(7).width = 700 * (len("PRODUCTO") + 1)
        sheet.col(8).width = 500 * (len("KILOS") + 1)
        sheet.col(9).width = 500 * (len("VALOR") + 1)

        row = 1
        total_consig = 0

        # ###################################
        # INSERCION DE VALORES EN LAS CELDAS
        # ###################################

        for account in accounts:
            for line in account.invoice_line_ids:
                sheet.write(
                    row,
                    0,
                    account.partner_id.partner_nit or "",
                    format_content,
                )
                sheet.write(
                    row, 1, account.partner_id.partner_dv or "", format_content
                )
                sheet.write(
                    row, 2, account.partner_id.name or "", format_content
                )
                sheet.write(
                    row, 3, account.partner_id.street or "", format_content
                )
                sheet.write(
                    row, 4, account.partner_id.phone or "", format_content
                )
                sheet.write(
                    row,
                    5,
                    account.partner_id.state_id.name or "",
                    format_content,
                )
                sheet.write(
                    row, 6, account.partner_id.city or "", format_content
                )
                sheet.write(row, 7, line.product_id.name or "", format_content)
                sheet.write(row, 8, line.quantity or "", format_content)
                sheet.write(row, 9, line.price_unit or "", format4)
                total_consig += line.price_unit
                row += 1

        row += 2

        # ######################
        # CUADRO DE INFORMACION
        # ######################

        # TOTALES
        sheet.write(row, 7, "TOTAL CONSIGNACIÓN", formatR)
        sheet.write(row, 8, total_consig, format4)
        row += 1

        # FECHA CONSIGNACION
        actual_date = datetime.strftime(datetime.today(), "%d/%m/%Y")
        sheet.write(row, 7, "FECHA CONSIGNACIÓN", formatR)
        sheet.write(row, 8, actual_date, format3)
        row += 1

        # BANCO
        sheet.write(row, 7, "BANCO", formatR)
        sheet.write(row, 8, self.report_bank.name or "", format3)
        row += 1

        # NIT
        sheet.write(row, 7, "NIT", formatR)
        sheet.write(row, 8, user.company_id.main_id_number or "", format3)
        row += 1

        # NOMBRE RECAUDADOR
        sheet.write(row, 7, "NOMBRE RECAUDADOR", formatR)
        sheet.write(row, 8, user.company_id.name or "", format3)
        row += 1

        # PERIODO
        periodo = dict(self._fields["periodo_mes"].selection).get(
            self.periodo_mes
        )
        sheet.write(row, 7, "PERIODO", formatR)
        sheet.write(row, 8, periodo, format3)

        # ##################
        # CREACION DE EXCEL
        # ##################

        workbook.save("/tmp/reporte_informacion.xls")
        result_file = open("/tmp/reporte_informacion.xls", "rb").read()
        attachment_id = self.env["wizard.account.information.report"].create(
            {
                "name": "Reporte_Informacion.xls",
                "report": base64.encodestring(result_file),
            }
        )

        return {
            "name": _("Reporte de Informacion"),
            "context": self.env.context,
            "view_type": "form",
            "view_mode": "form",
            "res_model": "wizard.account.information.report",
            "res_id": attachment_id.id,
            "data": None,
            "type": "ir.actions.act_window",
            "target": "new",
        }

    @api.multi
    def print_account_information_report(self):
        self.ensure_one()
        data = {}
        # ##################
        # VALIDACION FIRMA
        # ##################
        user = self.env["res.users"].browse(self._uid)
        if self.report_sign:
            if user.digital_signature is None:
                raise UserError("You have to set a sign")

        # #######
        # FECHAS
        # #######
        date = str(self.periodo_year) + "-" + str(self.periodo_mes) + "-01"
        date_start, date_end = self._format_dates(date)

        # ###################
        # LINEAS DE FACTURAS
        # ###################
        accounts = self.env["account.invoice"].search(
            [
                ("date_invoice", ">=", date_start),
                ("date_invoice", "<=", date_end),
                ("journal_id.type", "=", "purchase"),
            ]
        )

        # ##########################
        # CONSTRUCCION DE DATA FORM
        # ##########################
        total_consig = 0
        for account in accounts:
            for line in account.invoice_line_ids:
                total_consig += line.price_subtotal

        periodo = dict(self._fields["periodo_mes"].selection).get(
            self.periodo_mes
        )

        actual_date = datetime.strftime(datetime.today(), "%d/%m/%Y")

        data.update(
            {
                "total": total_consig,
                "periodo": periodo,
                "actual_date": actual_date,
                "signature": self.report_sign,
                "banco": self.report_bank.name,
            }
        )
        datas = {"account_ids": accounts.ids, "form": data}

        # ############
        # CALL REPORT
        # ############
        return self.env.ref(
            "account_information_report.action_account_information_report"
        ).report_action(self, data=datas)

    @api.multi
    def generated_account_information_line(self):
        """
            Account SQL Information Report
        """

        # #######
        # FECHAS
        # #######
        date = str(self.periodo_year) + "-" + str(self.periodo_mes) + "-01"
        date_start, date_end = self._format_dates(date)

        view_tree = self.env.ref(
            "account_information_report.view_account_information_report_tree"
        ).id

        ctx = {
            "date_start": date_start,
            "date_end": date_end,
        }

        return {
            "type": "ir.actions.act_window",
            "name": "Account Information Report",
            "views": [[view_tree, "tree"]],
            "res_model": "account.information.line.report",
            "target": "current",
            "context": ctx,
        }

    def _format_dates(self, start_date):

        # #####################
        # FORMATO FECHA INICIO
        # #####################
        my_time_start = datetime.min.time()
        date1 = datetime.strptime(start_date, "%Y-%m-%d")
        dateest = datetime.combine(date1, my_time_start)
        date_start = datetime.strftime(dateest, "%Y-%m-%d %H:%M:%S.%f")

        # ##################
        # FORMATO FECHA FIN
        # ##################
        last_day = calendar.monthrange(date1.year, date1.month)[1]
        # _logger.debug("*------------ACA--------*")
        # _logger.debug("aqui: %s", last_day)
        end_date = date1.replace(day=last_day)

        my_time = datetime.max.time()
        datee = datetime.combine(end_date, my_time)
        date_end = datetime.strftime(datee, "%Y-%m-%d %H:%M:%S.%f")

        return date_start, date_end


class WizardReportedeInformacion(models.TransientModel):
    _name = "wizard.account.information.report"

    name = fields.Char("File Name", size=64)
    report = fields.Binary("Prepared File", filters=".xls", readonly=True)
