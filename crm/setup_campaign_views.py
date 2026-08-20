import frappe
import json

def create_view(label, filters):
    if not frappe.db.exists("CRM View Settings", {"label": label, "dt": "CRM Lead"}):
        doc = frappe.new_doc("CRM View Settings")
        doc.label = label
        doc.dt = "CRM Lead"
        doc.type = "list"
        doc.route_name = "Leads"
        doc.pinned = 0
        doc.public = 1
        doc.user = ""
        doc.load_default_columns = 1
        doc.filters = json.dumps(filters)
        doc.insert(ignore_permissions=True)
        print(f"Created view: {label}")
    else:
        # update existing view
        doc = frappe.get_doc("CRM View Settings", {"label": label, "dt": "CRM Lead"})
        doc.filters = json.dumps(filters)
        doc.public = 1
        doc.user = ""
        doc.save(ignore_permissions=True)
        print(f"Updated view: {label}")

def setup():
    frappe.init(site="music-crm.local")
    frappe.connect()

    # Total Campaigns
    create_view("Total Campaigns", {})

    # Active Campaigns (Not Completed and Not Cancelled)
    create_view("Active Campaigns", {
        "status": ["not in", ["Completed", "Cancelled"]]
    })

    # Completed Campaigns
    create_view("Completed Campaigns", {
        "status": "Completed"
    })

    # Pending Campaigns
    create_view("Pending Campaigns", {
        "status": "Pending"
    })

    frappe.db.commit()
    print("Campaign views setup complete.")

if __name__ == "__main__":
    setup()
