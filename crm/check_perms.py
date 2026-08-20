import frappe
from frappe.permissions import get_role_permissions
def run():
    perms = get_role_permissions(frappe.get_meta('CRM Lead'), user='namit1234@gmail.com')
    print("Computed Permissions:", perms)
