import frappe

def run():
    doc = frappe.get_doc("DocType", "Team Profile")
    roles = [p.role for p in doc.permissions]
    
    changed = False
    if "Editor" not in roles:
        doc.append("permissions", {"role": "Editor", "read": 1, "write": 0})
        changed = True
    if "Executor" not in roles:
        doc.append("permissions", {"role": "Executor", "read": 1, "write": 0})
        changed = True
        
    if changed:
        doc.save()
        frappe.db.commit()
        print("Permissions added successfully")
    else:
        print("Permissions already exist")
