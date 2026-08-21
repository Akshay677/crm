import frappe

frappe.init(site="music-crm.local")
frappe.connect()

try:
    tp = frappe.get_doc("Team Profile", "aditya123@gmail.com")
    tp.role_type = "Project Manager"
    tp.save()
    frappe.db.commit()
    print("Success")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

