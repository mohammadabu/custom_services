from odoo import models,fields,api
from odoo import tools, _
class Custom_Issue_Register(models.Model):
    _name = "services.services.issue.register"
    issueID = fields.Char(string="Issue ID",required=True,cope=False,readonly=True,index=True,default=lambda self: _("New"))
    name = fields.Char(string="Issue")
    owner = fields.Many2one('res.users')
    project_id = fields.Many2one('services.services',default=lambda self: self.env.context.get('active_id', []))
    due_date = fields.Date()
    status = fields.Selection(
        [
            ("Resolved","Resolved"),
            ("Not resolved","Not resolved")
        ]
    )
    resolution = fields.Char()
    date_of_resolution = fields.Date(string="Date of resolution") 
    def get_active_id(self):
        self.active_id = self.env.context.get('active_id', [])
    active_id = fields.Integer(compute='get_active_id',default=lambda self: self.env.context.get('active_id', []))
    hide_report = fields.Boolean(string="Hide from external Report")
    @api.model
    def create(self,vals):
        if vals.get('issueID',_("New") == _("New")):
            active = self.env.context.get('active_id', [])
            project_seq = self.env['services.services'].sudo().search([('id','=',active)]).name_seq
            seq = self.env['ir.sequence'].next_by_code('services.services.issue.register.sequence')
            name_seq = project_seq+'-ISSUE-'+seq
            vals['issueID'] = name_seq
        res = super(Custom_Issue_Register,self).create(vals)
        return res   