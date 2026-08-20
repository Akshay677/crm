# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.caching import request_cache

_OWNER_FIELD = {
	"CRM Lead": "lead_owner",
	"CRM Deal": "deal_owner",
}


def hierarchy_enabled() -> bool:
	return bool(frappe.db.get_single_value("FCRM Settings", "enable_sales_hierarchy"))


def _permission_query_conditions(user: str | None, doctype: str):
	if not user:
		user = frappe.session.user

	if user == "Administrator":
		return ""

	roles = frappe.get_roles(user)
	if "System Manager" in roles:
		return ""

	in_tree = hierarchy_enabled() and _in_hierarchy(user)

	# Sales Manager outside the tree retains the default ie sees everything
	if "Sales Manager" in roles and not in_tree:
		return ""

	if doctype == "CRM Task":
		DT = frappe.qb.DocType("CRM Task")
		Todo = frappe.qb.DocType("ToDo").as_("_todo")
		
		q1 = DT.assigned_to == user
		if in_tree:
			q1 = q1 | DT.assigned_to.isin(_team_mem_query(user))

		q2_where = (Todo.reference_type == doctype) & (Todo.status != "Cancelled")
		if in_tree:
			q2_where = q2_where & ((Todo.allocated_to == user) | Todo.allocated_to.isin(_team_mem_query(user)))
		else:
			q2_where = q2_where & (Todo.allocated_to == user)

		q2 = DT.name.isin(frappe.qb.from_(Todo).select(Todo.reference_name).where(q2_where))
		
		LeadDT = frappe.qb.DocType("CRM Lead")
		lead_cond = _permission_query_conditions(user, "CRM Lead")
		q_lead = (DT.reference_doctype == "CRM Lead")
		if lead_cond:
			q_lead = q_lead & DT.reference_docname.isin(frappe.qb.from_(LeadDT).select(LeadDT.name).where(lead_cond))
			
		DealDT = frappe.qb.DocType("CRM Deal")
		deal_cond = _permission_query_conditions(user, "CRM Deal")
		q_deal = (DT.reference_doctype == "CRM Deal")
		if deal_cond:
			q_deal = q_deal & DT.reference_docname.isin(frappe.qb.from_(DealDT).select(DealDT.name).where(deal_cond))
			
		return q1 | q2 | q_lead | q_deal

	owner_field = _OWNER_FIELD[doctype]
	DT = frappe.qb.DocType(doctype)
	Todo = frappe.qb.DocType("ToDo").as_("_todo")

	meta = frappe.get_meta(doctype)
	custom_fields = ["custom_project_manager", "custom_editor", "custom_executor"]

	if in_tree:
		# Owner is the user themselves or any member of their subtree
		q1 = (DT[owner_field] == user) | DT[owner_field].isin(_team_mem_query(user))
		# Assigned to the user or any member of their subtree by ToDo
		q2 = DT.name.isin(
			frappe.qb.from_(Todo)
			.select(Todo.reference_name)
			.where(
				(Todo.reference_type == doctype)
				& (Todo.status != "Cancelled")
				& ((Todo.allocated_to == user) | (Todo.allocated_to.isin(_team_mem_query(user))))
			)
		)
		q = q1 | q2
		for f in custom_fields:
			if meta.has_field(f):
				q = q | (DT[f] == user) | DT[f].isin(_team_mem_query(user))
		return q

	# Sales User default: own records and records directly assigned to them
	q1 = DT[owner_field] == user
	q2 = DT.name.isin(
		frappe.qb.from_(Todo)
		.select(Todo.reference_name)
		.where((Todo.reference_type == doctype) & (Todo.status != "Cancelled") & (Todo.allocated_to == user))
	)
	q = q1 | q2
	for f in custom_fields:
		if meta.has_field(f):
			q = q | (DT[f] == user)
	return q


def get_lead_permission_query_conditions(user=None):
	cond = _permission_query_conditions(user, "CRM Lead")
	return cond.get_sql(with_namespace=True, quote_char="`", secondary_quote_char="'") if cond else ""


def get_deal_permission_query_conditions(user=None):
	cond = _permission_query_conditions(user, "CRM Deal")
	return cond.get_sql(with_namespace=True, quote_char="`", secondary_quote_char="'") if cond else ""


def get_task_permission_query_conditions(user=None):
	cond = _permission_query_conditions(user, "CRM Task")
	return cond.get_sql(with_namespace=True, quote_char="`", secondary_quote_char="'") if cond else ""


def _has_permission(doc, ptype, user, doctype: str) -> bool | None:
	if not user:
		user = frappe.session.user

	if user == "Administrator":
		return True

	roles = frappe.get_roles(user)
	if "System Manager" in roles:
		return True

	if ptype == "create" or not doc.name:
		return True

	in_tree = hierarchy_enabled() and _in_hierarchy(user)
	if "Sales Manager" in roles and not in_tree:
		return True

	conditions = _permission_query_conditions(user, doctype)
	DT = frappe.qb.DocType(doctype)
	return bool(
		frappe.qb.from_(DT).select(DT.name).where(DT.name == doc.name).where(conditions).limit(1).run()
	)


def has_lead_permission(doc, ptype, user):
	return _has_permission(doc, ptype, user, "CRM Lead")


def has_deal_permission(doc, ptype, user):
	return _has_permission(doc, ptype, user, "CRM Deal")


def has_task_permission(doc, ptype, user):
	return _has_permission(doc, ptype, user, "CRM Task")


def _in_hierarchy(user: str) -> bool:
	return bool(frappe.db.exists("CRM Sales Hierarchy", {"user": user}))


def _team_mem_query(user: str):
	Mgr = frappe.qb.DocType("CRM Sales Hierarchy").as_("_sqmgr")
	Member = frappe.qb.DocType("CRM Sales Hierarchy").as_("_sqmem")
	return (
		frappe.qb.from_(Mgr)
		.join(Member)
		.on((Member.lft >= Mgr.lft) & (Member.lft <= Mgr.rgt))
		.select(Member.user)
		.where(Mgr.user == user)
	)
