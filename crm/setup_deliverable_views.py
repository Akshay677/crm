import frappe
import json

def create_view(label, filters, dt="CRM Task", route_name="Tasks"):
    existing = frappe.db.get_value("CRM View Settings", {"label": label, "dt": dt})
    if not existing:
        doc = frappe.new_doc("CRM View Settings")
        doc.label = label
        doc.dt = dt
        doc.type = "list"
        doc.route_name = route_name
        doc.pinned = 0
        doc.public = 1
        doc.user = ""
        doc.load_default_columns = 1
        doc.filters = json.dumps(filters)
        doc.insert(ignore_permissions=True)
        print(f"Created view: {label} ({doc.name})")
    else:
        doc = frappe.get_doc("CRM View Settings", existing)
        doc.filters = json.dumps(filters)
        doc.public = 1
        doc.user = ""
        doc.save(ignore_permissions=True)
        print(f"Updated view: {label} ({doc.name})")

def setup():
    # Deliverables Views
    create_view("Total Deliverables", {})
    create_view("Posted Deliverables", {"status": "Done"})
    create_view("Pending Deliverables", {"status": ["not in", ["Done", "Canceled"]]})

    frappe.db.commit()
    print("Deliverable views setup complete.")

if __name__ == "__main__":
    setup()
