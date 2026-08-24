with open("frontend/src/components/Modals/TeamProfileModal.vue", "r") as f:
    content = f.read()

content = content.replace(
    "{ fieldname: 'role_type', fieldtype: 'Select', label: 'Role', options: ['Management', 'Project Manager', 'Editor', 'Executor', 'Ops', 'Finance'] },",
    "{ fieldname: 'role_type', fieldtype: 'Select', label: 'Role', options: ['Management', 'Project Manager', 'Editor', 'Executor', 'Ops', 'Finance'], reqd: 1 },"
)

with open("frontend/src/components/Modals/TeamProfileModal.vue", "w") as f:
    f.write(content)
