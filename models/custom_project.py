from odoo import models,fields,api,exceptions,SUPERUSER_ID
from odoo import tools, _
from datetime import datetime,timedelta

class Customservices(models.Model):
    _inherit = 'services.services'
    @api.model
    def _default_stage_project(self):
        project_stage_default = self.env['services.services.stages'].sudo().search([('default_stage','=',"True")])
        return project_stage_default
    project_stage = fields.Many2one('services.services.stages', string='Stage', ondelete='restrict', index=True, copy=False, tracking=True,group_expand='_read_group_stage_ids',default=_default_stage_project)
    name_seq = fields.Char(string="Project Ref",required=True,cope=False,readonly=True,index=True,default=lambda self: _("New"))
    parent_opportunity = fields.Many2one('crm.lead')
    auto_create = fields.Selection([
        ('yes', 'yes'),
        ('no', 'no')
    ])
    # def getAction(self):
    #     action_id = self.env.ref('project.project.action_id').id
    #     return action_id
    # get_action = fields.Char(default=getAction)
    change_log = fields.One2many('services.services.change.log', 'project_id', string="Change log")
    issue_register = fields.One2many('services.services.issue.register', 'project_id', string="Issue Register")
    risk_register = fields.One2many('services.services.risk', 'project_id', string="Risk Register")
    account_manager = fields.Many2one('res.users')
    project_folder = fields.Char()
    assigned_resources = fields.Many2many('res.users','name_seq')
    when_moved_project_emails = fields.Text()
    project_esc_date = fields.Datetime(default=datetime.now())
    project_esc_send_email = fields.Boolean()
    day_off = fields.Char()
    is_repeted = fields.Boolean(default=False)
    users_esc_email = fields.Text()
    # def _get_default_note(self):
    #     get_project_menu_id =  self.env.ref('project.menu_main_pm').id
    #     get_project_action_id =  self.env.ref('project.open_view_project_all').id	
    #     get_services_menu_id = self.env.ref('services.menu_main_pm').id
    #     get_services_action_id = self.env.ref('services.open_view_services_all').id	
    #     tbody = ""
    #     services_ids = []
    #     if self.parent_opportunity.id != False:
    #         servicess = self.env['services.services'].sudo().search([('parent_opportunity','=',self.parent_opportunity.id)])
    #         for services in servicess:
    #             services_ids.append(services.id)
    #             tbody += ('<tr><th scope="row"><a  href="/web?&debug=#action=%s&active_id=%s&cids=1&id=%s&menu_id=%s&model=services.services&view_type=form" >%s</a></th><td>%s</td><td>services</td></tr>') % (get_services_action_id,self.id,services.id,get_services_menu_id,services.name_seq,services.name)
    #         projects = self.env['project.project'].sudo().search(['&','|',('default_access_emails','like','#'+str(self.env.uid)+'#'),'|',('stage_access_emails','like','#'+str(self.env.uid)+'#'),'|',('assigned_resources_access_emails','like','#'+str(self.env.uid)+'#'),('owner_ownerManager_emails','like','#'+str(self.env.uid)+'#'),('parent_opportunity','=',self.parent_opportunity.id),('id','!=',self.id)])
    #         for project in projects:
    #             tbody += ('<tr><th scope="row"><a  href="/web?&debug=#action=%s&active_id=%s&cids=1&id=%s&menu_id=%s&model=project.project&view_type=form" >%s</a></th><td>%s</td><td>Project</td></tr>') % (get_project_action_id,self.id,project.id,get_project_menu_id,project.name_seq,project.name)
    #     else:
    #          tbody = "" 
    #     for linked_project in self.linked_project:
    #         if linked_project.id not in services_ids:
    #             tbody += ('<tr><th scope="row"><a  href="/web?&debug=#action=%s&active_id=%s&cids=1&id=%s&menu_id=%s&model=services.services&view_type=form" >%s</a></th><td>%s</td><td>services</td></tr>') % (get_services_action_id,self.id,linked_project.id,get_services_menu_id,linked_project.name_seq,linked_project.name)
    #     if  tbody == "" or tbody == False:
    #         tbody += '<tr><td colspan="3" style="text-align: center;">There is No Data to display</td></tr>'
    #     result = """
    #         <table class="table table-hover table-bordered">
    #             <thead>
    #                 <tr>
    #                 <th scope="col">Reference</th>
    #                 <th scope="col">Name</th>
    #                 <th scope="col">Type</th>
    #                 </tr>
    #             </thead>
    #             <tbody>
    #              """
    #     result +=  tbody       
    #     result += """            
    #             </tbody>
    #         </table>
    #     """
    #     self.test_html = result
    # test_html = fields.Text(compute=_get_default_note)
    test_html = fields.Text()
    @api.model
    def _getProjectManager(self):
        all_emails = []
        all_pmo = self.env['hr.job'].sudo().search(['|','|',('internal_id','=',"PMO Manager"),('internal_id','=',"Senior Project Manager"),'|',('internal_id','=',"Project Manager"),('internal_id','=',"Project Coordinator")])
        for pmo in all_pmo:
            all_employee_pre = self.env['hr.employee'].sudo().search([('multi_job_id','=',pmo.id)])
            for employee_pre in all_employee_pre:
                if employee_pre.user_id != False:
                    user_email_pre = self.env['res.users'].sudo().search([('id','=',employee_pre.user_id.id)])
                    if user_email_pre.login != False:
                        all_emails.append(user_email_pre.id)
        return [('id', 'in', all_emails)]
    user_id = fields.Many2one('res.users',domain=_getProjectManager)
    # @api.model
    # def getAllRelatedProject(self):
    #     if self.parent_opportunity.id != False:
    #         projects = self.env['services.services'].sudo().search(['&','|',('default_access_emails','like','#'+str(self.env.uid)+'#'),'|',('stage_access_emails','like','#'+str(self.env.uid)+'#'),'|',('assigned_resources_access_emails','like','#'+str(self.env.uid)+'#'),('owner_ownerManager_emails','like','#'+str(self.env.uid)+'#'),('parent_opportunity','=',self.parent_opportunity.id),('id','!=',self.id)])
    #         self.related_project = projects
    #     else:
    #          self.related_project = []   
    # related_project = fields.Many2many('services.services','related_project','name_seq',compute='getAllRelatedProject')
    linked_project = fields.Many2many('services.services','linked_project','name_seq')
    @api.model 
    def calc_new_project_completed(self,id):
        project_id = id
        all_tasks  = self.env['services.task'].sudo().search([('services_id','=',project_id)])
        project  = self.env['services.services'].sudo().search([('id','=',project_id)])
        total_percentage = 0
        for task in all_tasks:
            total_percentage += self.percentage_complete
        if len(all_tasks) > 0: 
            res = total_percentage / len(all_tasks)
        else:
            res = 0    
        project.new_project_completed = res
    new_project_completed = fields.Float(string="Project Complete")
    max_rate = fields.Integer(string='Maximum rate', default=100)
    # @api.model
    # def _getAllLinkedProject(self):
    #     related_project_arr = []
    #     all_projects = self.env['project.project'].sudo().search([('parent_opportunity','=',self.parent_opportunity.id),('id','!=',self.id)])
    #     for related_project in all_projects:
    #         related_project_arr.append(related_project.id)
    #     return [('id', 'not in', related_project_arr)]
    # linked_project = fields.Many2many('services.services','related_project','name_seq')
    def get_resk_count(self):
        count_value = self.env['services.services.risk'].search_count([('project_id','=',self.id)])
        self.risk_project_account = count_value
    risk_project_account = fields.Integer(string="risk count",compute="get_resk_count")

    def get_issue_register_count(self):
        count_value = self.env['services.services.issue.register'].search_count([('project_id','=',self.id)])
        self.issue_register_account = count_value
    issue_register_account = fields.Integer(string="issue_register count",compute="get_issue_register_count")

    def get_change_log_count(self):
        count_value = self.env['services.services.change.log'].search_count([('project_id','=',self.id)])
        self.change_log_account = count_value
    change_log_account = fields.Integer(string="change_log count",compute="get_change_log_count")
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)        

    def open_services_risk(self):
        return{
            'name':"Project Risk",
            'domain':[('project_id','=',self.id)],
            'type':'form',
            'res_model':'services.services.risk',
            'view_id':False,
            'view_mode':'tree,form',
            'type':'ir.actions.act_window',
            'target':'list'
        }

    def open_issue_register(self):
        return{
            'name':"Issue Register",
            'domain':[('project_id','=',self.id)],
            'type':'form',
            'res_model':'services.services.issue.register',
            'view_id':False,
            'view_mode':'tree,form',
            'type':'ir.actions.act_window',
            'target':'list'
        }   

    def open_change_log(self):
        return{
            'name':"Change Log",
            'domain':[('project_id','=',self.id)],
            'type':'form',
            'res_model':'services.services.change.log',
            'view_id':False,
            'view_mode':'tree,form',
            'type':'ir.actions.act_window',
            'target':'list'
        }        
    
    @api.onchange('parent_opportunity')
    def onchange_parent_opportunity_value(self):
        for rec in self:
            lead = self.env['crm.lead'].sudo().search([('id','=',rec.parent_opportunity.id)])
            self.account_manager = lead.user_id
            self.partner_id = lead.partner_id  


    # @api.onchange('project_stage')
    # def onchange_value(self):
    #     current_stage =  self._origin.project_stage.internal_id
    #     current_field = self._origin
    #     for rec in self:
    #         rec.project_esc_date = datetime.today()    
    #         self.project_esc_send_email = False
    #         rec.is_repeted = False
    #         rec.day_off = False
    # default_access_emails = fields.Text()
    # stage_access_emails = fields.Text()
    # assigned_resources_access_emails = fields.Text()
    # owner_ownerManager_emails = fields.Text()
    # @api.model 
    # def custom_default_group(self,wh="all"):
    #     all_emails_default_access = False
    #     all_stages = self.env['services.services.stages'].sudo().search([])
    #     if wh == "all":
    #         #get default position
    #         all_default_position = self.env['hr.job'].sudo().search([('default_groub_project','=',True)])
    #         for default_position in all_default_position:
    #             all_employee = self.env['hr.employee'].sudo().search([('multi_job_id','in',default_position.id)])
    #             for employee in all_employee:
    #                 if employee.user_id != False:
    #                     user_email = self.env['res.users'].sudo().search([('id','=',employee.user_id.id)])
    #                     if user_email.login != False:
    #                         if all_emails_default_access != False:
    #                             if ("#"+str(user_email.id)+"#") not in all_emails_default_access:
    #                                 all_emails_default_access = all_emails_default_access + ("#"+str(user_email.id)+"#")
    #                         else:
    #                             all_emails_default_access = ("#"+str(user_email.id)+"#")
    #     for stage in all_stages:
    #         all_emails_default_stage = False
    #         if wh == "all" or wh == "stage":
    #             #get default pos stage 
    #             all_access_group = stage.access_group
    #             for access_group in all_access_group:  
    #                 all_employee_stage = self.env['hr.employee'].sudo().search([('multi_job_id','in',access_group.id)])
    #                 for employee_stage in all_employee_stage:
    #                     if employee_stage.user_id != False:
    #                         user_email_stage = self.env['res.users'].sudo().search([('id','=',employee_stage.user_id.id)])
    #                         if user_email_stage.login != False:
    #                             if all_emails_default_stage != False:
    #                                 if ("#"+str(employee_stage.user_id.id)+"#") not in all_emails_default_stage:
    #                                     all_emails_default_stage =  all_emails_default_stage+"#"+str(employee_stage.user_id.id)+"#"
    #                             else:
    #                                 all_emails_default_stage = "#"+str(employee_stage.user_id.id)+"#"
    #         all_projects = self.env['services.services'].sudo().search([('project_stage','=',stage.id)])
    #         for project in all_projects:
    #             all_emails_owner_ownerManager_emails = False
    #             all_emails_assigned_resources = False
    #             if wh == "all" or wh == "project":
    #                 # get project manager
    #                 if project.user_id != False:
    #                     user_project_manager_email = self.env['res.users'].sudo().search([('id','=',project.user_id.id)])
    #                     if user_project_manager_email.login != False:
    #                         if all_emails_owner_ownerManager_emails != False:
    #                             if ("#"+str(user_project_manager_email.id)+"#") not in all_emails_owner_ownerManager_emails:
    #                                 all_emails_owner_ownerManager_emails = all_emails_owner_ownerManager_emails + "#"+str(user_project_manager_email.id)+"#"
    #                         else:
    #                             all_emails_owner_ownerManager_emails = "#"+str(user_project_manager_email.id)+"#"
    #                 # get owner and owner manager
    #                 if project.account_manager.id != False:
    #                     user_owner_email = self.env['res.users'].sudo().search([('id','=',project.account_manager.id)])      
    #                     user_owner_manager_info = self.env['hr.employee'].sudo().search([('user_id','=',project.account_manager.id)])
    #                     # get owner
    #                     if user_owner_email.login != False:
    #                         if all_emails_owner_ownerManager_emails != False:
    #                             if ("#"+str(user_owner_email.id)+"#") not in all_emails_owner_ownerManager_emails:
    #                                 all_emails_owner_ownerManager_emails = all_emails_owner_ownerManager_emails + "#"+str(user_owner_email.id)+"#"
    #                         else:
    #                             all_emails_owner_ownerManager_emails = "#"+str(user_owner_email.id)+"#"
    #                     # get owner manager    
    #                     if user_owner_manager_info.parent_id != False:
    #                         employee_manager = self.env['hr.employee'].sudo().search([('id','=',user_owner_manager_info.parent_id.id)])
    #                         if employee_manager.user_id != False:
    #                             user_owner_manager_email = self.env['res.users'].sudo().search([('id','=',employee_manager.user_id.id)])
    #                             if user_owner_manager_email.login != False:
    #                                 if all_emails_owner_ownerManager_emails != False:
    #                                     if ("#"+str(user_owner_manager_email.id)+"#") not in all_emails_owner_ownerManager_emails:
    #                                         all_emails_owner_ownerManager_emails = all_emails_owner_ownerManager_emails + "#"+str(user_owner_manager_email.id)+"#"
    #                                 else:
    #                                     all_emails_owner_ownerManager_emails = "#"+str(user_owner_manager_email.id)+"#"
    #                 # get assigned resource
    #                 if stage.internal_id == 'External Kickoff Meeting' or stage.internal_id == 'Designing' or stage.internal_id == 'Execution' or stage.internal_id == 'On Hold' or  stage.internal_id == 'Closing': 
    #                     all_assigned_resources = project.assigned_resources
    #                     for assigned_resource in all_assigned_resources:
    #                         user_email_stage = self.env['res.users'].sudo().search([('id','=',assigned_resource.id)])
    #                         if user_email_stage.login != False:
    #                             if all_emails_assigned_resources != False:
    #                                 if ("#"+str(user_email_stage.id)+"#") not in all_emails_assigned_resources:
    #                                     all_emails_assigned_resources =  all_emails_assigned_resources+"#"+str(user_email_stage.id)+"#"
    #                             else:
    #                                 all_emails_assigned_resources = "#"+str(user_email_stage.id)+"#"
    #             if wh == "all" or wh == "project":
    #                 project.assigned_resources_access_emails = all_emails_assigned_resources
    #                 project.owner_ownerManager_emails = all_emails_owner_ownerManager_emails
    #             if wh == "all":
    #                 project.default_access_emails = all_emails_default_access
    #             if wh == "all" or wh == "stage":
    #                 project.stage_access_emails = all_emails_default_stage    

    def get_all_employee_position(self,pos_id,all_emails):
        job_position = self.env['hr.job'].sudo().search([('internal_id','=',pos_id)])
        for position in job_position:
            all_employee = self.env['hr.employee'].sudo().search([('multi_job_id','in',position.id)])
            for employee in all_employee:
                if employee.user_id != False:
                    user_email = self.env['res.users'].sudo().search([('id','=',employee.user_id.id)])
                    if user_email.login != False:
                        if all_emails != False:
                            if (str(user_email.login)) not in all_emails:
                                all_emails = all_emails + "," + (str(user_email.login))
                        else:
                            all_emails = (str(user_email.login))
        return  all_emails                   
            
    def getUserEmailById(self,id,all_emails):
        if id != False:
            user_email = self.env['res.users'].sudo().search([('id','=',id)])                      
            if user_email.login != False:
                if all_emails != False:
                    if (str(user_email.login)) not in all_emails:
                        all_emails = all_emails + "," + str(user_email.login)
                else:
                    all_emails = str(user_email.login)
        return all_emails            
    def custom_move_stage_notify(self,rec):
        stage = rec.project_stage.internal_id
        all_emails = False
        # get owner
        if stage == "Account Manager Review" or stage == "PMO Review" or stage == "Internal Kickoff Meeting" or stage == "On Hold" or stage == "Closed":
            all_emails = self.pool.get("services.services").getUserEmailById(self,rec.account_manager.id,all_emails)
        # get Assigned Project Manager
        all_emails = self.pool.get("services.services").getUserEmailById(self,rec.user_id.id,all_emails)         
        #get pmo manager
        if stage == "PMO Review" or stage == "On Hold" or stage == "Closed":
            all_emails = self.pool.get("services.services").get_all_employee_position(self,"PMO Manager",all_emails)
        #get Technical Manager
        if stage == "Resources Assignment" or stage == "Internal Kickoff Meeting":
            all_emails = self.pool.get("services.services").get_all_employee_position(self,"Technical Manager",all_emails)
        return all_emails            
    @api.model
    def create(self,vals):
        if vals.get('name_seq',_("New") == _("New")):
            seq = self.env['ir.sequence'].next_by_code('services.services.sequence')
            name_seq = 'OSP-'+seq
            vals['name_seq'] = name_seq
        res = super(Customservices,self).create(vals)
        return res
    def write(self,values):
        # before_edit_pm = self.user_id.id
        # before_edit_am = self.account_manager.id
        # befory_edit_assigned_resources = self.assigned_resources
        # befory_edit_stage = self.project_stage.internal_id
        rtn = super(Customservices,self).write(values)
        # after_edit_pm = self.user_id.id
        # after_edit_am = self.account_manager.id
        # after_edit_assigned_resources = self.assigned_resources
        # after_edit_stage = self.project_stage.internal_id
        # can_edit = False
        # if len(befory_edit_assigned_resources) != len(after_edit_assigned_resources):
        #     can_edit = True
        # else:
        #     result =  all(elem in befory_edit_assigned_resources  for elem in after_edit_assigned_resources)
        #     if not result:
        #         can_edit = True    
        # if(before_edit_pm != after_edit_pm or before_edit_am != after_edit_am or can_edit == True or befory_edit_stage != after_edit_stage):
        #     self.pool.get("services.services").custom_default_group(self,'project')
        # if(befory_edit_stage != after_edit_stage):
        #     all_emails_moved = self.pool.get("services.services").custom_move_stage_notify(self,self)
        #     self.when_moved_project_emails = all_emails_moved
        #     template_id = self.env.ref('custom_services.custom_update_services_email_tempalte').id
        #     self.env['mail.template'].browse(template_id).send_mail(self.id,force_send=True)        
        return rtn
    # def unlink(self):
    #     rtn = super(Customservices, self).unlink()
    #     self.pool.get("services.services").custom_default_group(self,"project")
    #     return rtn    
    # @api.model
    # def escalation_project(self):
    #     job_positions = self.env['hr.job'].search([('default_esc_project','=',True)])
    #     projects = self.env['services.services'].search([])
    #     for project in projects:
    #         if project.project_esc_send_email != True:
    #             date_now = datetime.today()
    #             project_stage = project.project_stage.internal_id
    #             arrivalـtime = project.project_esc_date
    #             stage_info = self.env['services.services.stages'].search([('internal_id','=',project_stage)])
    #             escalation_after = False
    #             if project.is_repeted != False:
    #                 escalation_after = stage_info.repet_escalation
    #             else:
    #                 escalation_after = stage_info.escalation_after    
    #             if  escalation_after != False and escalation_after > 0:
    #                 arrivalـtime = arrivalـtime + timedelta(days=escalation_after)
    #                 if date_now >= arrivalـtime :
    #                     year = date_now.date().strftime("%Y")
    #                     month = date_now.date().strftime("%m")
    #                     day = date_now.date().strftime("%d")
    #                     date_hour = date_now + timedelta(hours=3)
    #                     hour = date_hour.strftime("%H")
    #                     date_new = day + " " + month + " " + year
    #                     day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    #                     day = datetime.strptime(date_new, '%d %m %Y').weekday()
    #                     valid_day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday','Sunday']
    #                     day_off = ['Friday', 'Saturday']
    #                     valid_hour = ['09', '10', '11','12','13','14','15','16','17','18','19']
    #                     if day_name[day] in day_off and (project.day_off == False or project.day_off != day_name[day]):
    #                         project.day_off = day_name[day]
    #                         project_time = project.project_esc_date
    #                         project.opportunity_esc_date = project_time + timedelta(days=1)
    #                     if hour in valid_hour and day_name[day] in valid_day_name:
    #                         # get all default esc
    #                         all_user_emails = False
    #                         for pos in job_positions:
    #                             employee = self.env['hr.employee'].search([('multi_job_id','in',pos.id)])
    #                             for emp in employee:
    #                                 if emp.user_id != False:
    #                                     user_email = self.env['res.users'].search([('id','=',emp.user_id.id)])
    #                                     if user_email.login != False:
    #                                         if all_user_emails != False:
    #                                             if user_email.login not in all_user_emails:
    #                                                 all_user_emails = all_user_emails + "," + user_email.login
    #                                         else:
    #                                             all_user_emails = user_email.login
    #                         # get all position esc      
    #                         all_esc_groub = stage_info.escalation_group
    #                         for esc_groub in all_esc_groub:
    #                             employee_esc = self.env['hr.employee'].search([('multi_job_id','in',esc_groub.id)])               
    #                             for emp_esc in employee_esc:
    #                                 if emp_esc.user_id != False:
    #                                     user_email = self.env['res.users'].search([('id','=',emp_esc.user_id.id)])
    #                                     if user_email.login != False:
    #                                         if all_user_emails != False:
    #                                             if user_email.login not in all_user_emails:
    #                                                 all_user_emails = all_user_emails + "," + user_email.login
    #                                         else:
    #                                             all_user_emails = user_email.login
    #                                 # get manager for this employee
    #                                 if emp_esc.parent_id != False:
    #                                     employee_manager = self.env['hr.employee'].search([('id','=',emp_esc.parent_id.id)])
    #                                     if employee_manager.user_id != False:
    #                                         user_manager_email = self.env['res.users'].search([('id','=',employee_manager.user_id.id)])      
    #                                         if user_manager_email.login != False:
    #                                             if all_user_emails != False:
    #                                                 if user_manager_email.login not in all_user_emails:
    #                                                     all_user_emails = all_user_emails + "," + user_manager_email.login
    #                                             else:
    #                                                 all_user_emails = user_manager_email.login
    #                         # get owner
    #                         if project.account_manager.id != False:
    #                             if project.account_manager.login != False:
    #                                 if all_user_emails != False:
    #                                     if project.account_manager.login not in all_user_emails:
    #                                         all_user_emails = all_user_emails + "," + project.account_manager.login
    #                                 else:
    #                                         all_user_emails = project.account_manager.login
    #                         if project_stage == "Account Manager Review":
    #                             # get owner manager    
    #                             user_owner_manager_info = self.env['hr.employee'].sudo().search([('user_id','=',project.account_manager.id)])
    #                             if user_owner_manager_info.parent_id != False:
    #                                 employee_manager = self.env['hr.employee'].sudo().search([('id','=',user_owner_manager_info.parent_id.id)])
    #                                 if employee_manager.user_id != False:
    #                                     user_owner_manager_email = self.env['res.users'].sudo().search([('id','=',employee_manager.user_id.id)])
    #                                     if user_owner_manager_email.login != False:
    #                                         if all_user_emails != False:
    #                                             if (user_owner_manager_email.login) not in all_user_emails:
    #                                                 all_user_emails = all_user_emails + "," + user_owner_manager_email.login
    #                                         else:
    #                                             all_user_emails = user_owner_manager_email.login
    #                         if project_stage != "Closed":
    #                             # get project manager
    #                             if project.user_id.id != False:
    #                                 if project.user_id.login != False:
    #                                     if all_user_emails != False:
    #                                         if project.user_id.login not in all_user_emails:
    #                                             all_user_emails = all_user_emails + "," + project.user_id.login
    #                                     else:
    #                                             all_user_emails = project.user_id.login
    #                         project.users_esc_email = all_user_emails
    #                         print('all_project_user_emails')
    #                         print(all_user_emails)
    #                         # template_id = self.env.ref('custom_services.services_email_tempalte').id
    #                         # self.env['mail.template'].browse(template_id).send_mail(project.id,force_send=True)
    #                         project.project_esc_send_email = True  
    #         else:
    #             project_stage = project.project_stage.internal_id
    #             stage_info = self.env['services.services.stages'].search([('internal_id','=',project_stage)])
    #             if stage_info.repet_escalation != False and stage_info.repet_escalation > 0 :
    #                 project.project_esc_send_email = False
    #                 project.is_repeted = True 
    #                 project.project_esc_date = datetime.today()                           
 