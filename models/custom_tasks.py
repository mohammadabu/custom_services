from odoo import models,fields,api,exceptions,SUPERUSER_ID
from odoo import tools, _
class CustomTasks(models.Model):
    _inherit = 'services.task'
    # @api.model
    # def _getUserTask(self):
    #     assigned_arr = []
    #     active_ids = self.env.context.get('active_ids', [])
    #     for active_id in active_ids: 
    #         project = self.env['services.services'].sudo().search([('id','=',active_id)])
    #         for assigned in project.assigned_resources:
    #             assigned_arr.append(assigned.id)     
    #     return [('id', 'in', assigned_arr)]
    # assigned_res = fields.Many2many('res.users','assigned_res',domain=_getUserTask)
    assigned_res = fields.Many2many('res.users','assigned_res')
    duration_1 = fields.Float()
    start_date = fields.Datetime()
    end_date = fields.Datetime()
    percentage_complete = fields.Float()
    def calc_work(self):
        try:
            assigned_len = len(self.assigned_res)
            duration = self.duration_1
            res = assigned_len * duration
            self.work = res
        except:
            print("An exception occurred")     
    work = fields.Float(compute="calc_work")
    def calc_work_complete(self):
        try:
            percentage = self.percentage_complete
            work = self.work
            res = (percentage/ 100) * work
            self.work_complete = res
        except:
            print("An exception occurred")      
    work_complete = fields.Float(compute="calc_work_complete")
    def write(self,values):
        # before_edit_user = self.user_id.id
        rtn = super(CustomTasks,self).write(values)
        active_ids = self.env.context.get('active_ids', [])
        for active_id in active_ids: 
            self.pool.get("services.services").calc_new_project_completed(self,active_id) 
        return rtn

    def unlink(self):
        rtn = super(CustomTasks, self).unlink()
        active_ids = self.env.context.get('active_ids', [])
        for active_id in active_ids: 
            self.pool.get("services.services").calc_new_project_completed(self,active_id) 
        return rtn     