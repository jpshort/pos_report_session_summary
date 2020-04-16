#-*- coding:utf -*-
from odoo import api,models

class PosPaymentSession(models.AbstracModel):
    _name = "report.pos_report_session_summary.report_session_summary"
    _description = "Mostrar los pagos extras del POS"

    @api.model
    def _get_report_values(self,docids,data=None):
        model = self.env.context.get('active_model')
        print("Acttive MODEL",model)
        print("Docids ",docids)
        docs = self.env[model].browse(self.env.context.get('active_id))


