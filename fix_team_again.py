with open("frontend/src/components/Modals/TeamProfileModal.vue", "r") as f:
    content = f.read()

# Pass :required to Link
content = content.replace(
    ':label="__(field.label)"\n            :onCreate=',
    ':label="__(field.label)"\n            :required="field.reqd"\n            :onCreate='
)

# Replace :reqd with :required in FormControl and Password
content = content.replace(':reqd="field.reqd"', ':required="field.reqd"')

# Add validation logic to submit
old_submit = """  if (!doc.password) {
    error.value = __('Password is required')
    isSubmitting.value = false
    return
  }"""
new_submit = """  if (!doc.user) {
    error.value = __('User is required')
    isSubmitting.value = false
    return
  }
  if (!doc.role_type) {
    error.value = __('Role is required')
    isSubmitting.value = false
    return
  }
  if (!doc.password) {
    error.value = __('Password is required')
    isSubmitting.value = false
    return
  }"""
content = content.replace(old_submit, new_submit)

with open("frontend/src/components/Modals/TeamProfileModal.vue", "w") as f:
    f.write(content)

# Now fix Link.vue
with open("frontend/src/components/Controls/Link.vue", "r") as f:
    link = f.read()

link = link.replace('v-if="attrs.reqd"', 'v-if="attrs.required"')
with open("frontend/src/components/Controls/Link.vue", "w") as f:
    f.write(link)
