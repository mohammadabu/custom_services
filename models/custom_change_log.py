from odoo import models,fields,api,osv
from lxml import etree
from odoo import tools, _
class Custom_Change_Log(models.Model):
    _name = "services.services.change.log"
    name = fields.Char(string="Change ID",required=True,cope=False,readonly=True,index=True,default=lambda self: _("New"))
    requestor = fields.Many2one('res.users')
    date = fields.Date()
    status = fields.Selection(
        [
            ("Accepted","Accepted"),
            ("Rejected","Rejected"),
            ("Under Analysis","Under Analysis")
        ]
    )
    description = fields.Text()
    date_acceptence_rejection = fields.Date(string="Date of Acceptence/Rejection")
    date_of_implementation = fields.Date(string="Date of Implementation") 
    project_id = fields.Many2one('services.services',default=lambda self: self.env.context.get('active_id', []))
    def get_active_id(self):
        self.active_id = self.env.context.get('active_id', [])
    active_id = fields.Integer(compute='get_active_id',default=lambda self: self.env.context.get('active_id', []))
    hide_report = fields.Boolean(string="Hide from external Report")
    @api.model
    def create(self,vals):
        if vals.get('name',_("New") == _("New")):
            active = self.env.context.get('active_id', [])
            project_seq = self.env['services.services'].sudo().search([('id','=',active)]).name_seq
            seq = self.env['ir.sequence'].next_by_code('services.services.change.log.sequence')
            name_seq = project_seq+'-CHG-'+seq
            vals['name'] = name_seq
        res = super(Custom_Change_Log,self).create(vals)
        return res       
    
   

