#-*- coding:utf -*-
from odoo import api,models
class PaymentSession(models.Model):
    _inherit = 'account.payment'
    pos_session = fields.Many2one('pos.session')

class PosPaymentSession(models.AbstractModel):
    _name = "report.pos_report_session_summary.report_session_summary"
    _description = "Mostrar los pagos extras del POS"

    @api.model
    def _get_report_values(self,docids,data=None):
        docs = self.env['pos.session'].browse(docids[0])
        payments = self.env['account.payment'].search([('pos_session','=',docids[0])])
        statements = self.env['account.bank.statement'].search([('pos_session_id','=',docids[0])]) 

        journal = []
        journal_list = []
        journal_statement = []
        list_payment = []
        list_invoice = []
        for st in statements:
            for inv in st.line_ids:
                journal_statement.append(inv.journal_id.id)
                invs = {'journal_id':inv.journal_id.id,
                        'journal_name':inv.journal_id.name,
                        'partner_id':inv.partner_id,
                        'ref':inv.ref,
                        'account_id':inv.account_id,
                        'date':inv.date,
                        'amount':inv.amount}
                #list_invoice.append(invs)

        for pp in payments:
            journal_list.append(pp.journal_id.id)
            add_payment = True
            for inv in pp.invoice_ids:
                invs = {'journal_id':pp.journal_id.id,
                        'journal_name':pp.journal_id.name,
                        'partner_id':inv.partner_id.name,
                        'ref':inv.reference,
                        'account_id':inv.account_id.name,
                        'date':inv.date_invoice,
                        'amount':pp.amount}
                list_invoice.append(invs)
                add_payment = False

            if add_payment:
                invs = {'journal_id':pp.journal_id.id,
                        'journal_name':pp.journal_id.name,
                        'partner_id':pp.partner_id.name,
                        'ref':'Pago POS sin Factura',
                        'account_id':pp.partner_id.property_account_receivable_id.name,
                        'date':pp.payment_date,
                        'amount':pp.amount}
                list_invoice.append(invs)
                
        #Elimate the journal duplicate
        journal = list(set(journal_list))

        #Sum the journal amount total
        missing_journal = []
        for jj in journal:
            suma = 0
            missing = True
            journal_missing_name = ""
            for pp in payments:
                if pp.journal_id.id == jj:
                    suma += pp.amount 
                    journal_missing_name = pp.journal_id.name
                    
            vals = {'journal':jj,
                    'amount':suma}

            list_payment.append(vals)
            for aux in journal_statement:
                if jj == aux:
                    missing = False

            if missing:
                vals = {'journal':jj,
                        'name':journal_missing_name}
                print("missing",journal_missing_name)
                missing_journal.append(vals)
            

        return{'doc_model': 'pos.session',
               'data':data,
               'docs':docs,
               'list_payment':list_payment,
               'list_invoice':list_invoice,
               'missing_journal':missing_journal} 


