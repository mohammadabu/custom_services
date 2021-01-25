from odoo import models,fields,api
class Custom_services_Stages(models.Model):
    _name = "services.services.stages"
    name = fields.Char(string='Name')
    default_stage = fields.Boolean()
    internal_id = fields.Char()
    # access_group = fields.Many2many(
    #     'hr.job',
    #     'access_group',
    #     string='Access Group'
    # )
    # escalation_group = fields.Many2many(
    #     'hr.job',
    #     'escalation_group',
    #     string='Escalation Group'
    # )
    # escalation_after = fields.Integer(string='Escalation after (Business Days)')
    # repet_escalation = fields.Integer(string='Repet escalation after (Business Days)')
    # def write(self,values):
    #     befory_edit_access_group = self.access_group
    #     rtn = super(Custom_services_Stages,self).write(values)
    #     after_edit_access_group = self.access_group
    #     can_edit = False
    #     if len(befory_edit_access_group) != len(after_edit_access_group):
    #         can_edit = True
    #     else:
    #         result =  all(elem in befory_edit_access_group  for elem in after_edit_access_group)
    #         if not result:
    #             can_edit = True    
    #     if(can_edit == True):
    #         self.pool.get("services.services").custom_default_group(self,"stage")
    #     return rtn