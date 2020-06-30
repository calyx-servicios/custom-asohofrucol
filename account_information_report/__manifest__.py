# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Information Report",
    "summary": """
        Account report information custom.""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["Lolstalgia"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    "category": "Technical Settings",
    "version": "11.0.1.0.0",
    # see https://odoo-community.org/page/development-status
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    # any module necessary for this one to work correctly
    "depends": ["base", "account", "web_digital_sign", "res_partner_extend"],
    "data": [
        "wizard/account_information_report_view.xml",
        "report/account_information_template.xml",
        "report/account_report_information.xml",
        "view/account_res_bank_view.xml",
        "view/account_information_line_view.xml",
        "security/ir.model.access.csv",
    ],
}
