import frappe

def execute():
    valid_roles = ["Management", "Project Manager", "Editor", "Executor", "Ops", "Finance"]
    profiles = frappe.get_all("Team Profile", fields=["name", "user", "role_type"])
    
    for p in profiles:
        user_roles = frappe.get_roles(p.user)
        # Find the first matching role
        assigned_role = None
        for vr in valid_roles:
            if vr in user_roles:
                assigned_role = vr
                break
                
        if assigned_role and p.role_type != assigned_role:
            frappe.db.set_value("Team Profile", p.name, "role_type", assigned_role)
            
    frappe.db.commit()
