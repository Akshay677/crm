import frappe

def run():
    doc = frappe.get_doc("DocType", "Team Profile")
    changed = False
    for p in doc.permissions:
        if p.role == "Project Manager":
            if not p.write:
                p.write = 1
                changed = True
    if changed:
        doc.save()
        frappe.db.commit()
        print("Write permission granted to Project Manager")
    else:
        print("Permission already granted")
