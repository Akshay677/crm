import frappe
from crm.api.doc import get_data
import json

def execute():
    res = get_data(doctype='Team Profile', limit=1, view='List')
    print(json.dumps(res))
