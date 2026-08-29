import frappe
from crm.fcrm.doctype.crm_fields_layout.crm_fields_layout import get_fields_layout
frappe.init(site="music-crm.local")
frappe.connect()
print(get_fields_layout("CRM Task", "Quick Entry"))
