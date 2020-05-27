# -*- coding: utf-8 -*-
{
    "name": "Purchase Order Information Custom Report",
    "summary": """
        Information Purchase Order Report""",
    "description": """
        
    """,
    "author": "Calyx",
    "website": "http://www.calyxservicios.com.ar",
    "category": "Customs",
    "version": "11.0.1.0.0",
    "depends": [
        "base",
        "contacts",
        "purchase",
        "web_digital_sign",
        "custom_partner_col",
    ],
    "data": [
        "wizard/purchase_report_view.xml",
        "report/purchase_report_information_template.xml",
        "report/purchase_report_information.xml",
    ],
}
