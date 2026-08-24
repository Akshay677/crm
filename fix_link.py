with open("frontend/src/components/Controls/Link.vue", "r") as f:
    content = f.read()

old_label = """    <label v-if="attrs.label" class="block" :class="labelClasses">
      {{ __(attrs.label) }}
    </label>"""
new_label = """    <label v-if="attrs.label" class="block" :class="labelClasses">
      {{ __(attrs.label) }}
      <span v-if="attrs.reqd" class="text-red-500" title="Required">*</span>
    </label>"""
content = content.replace(old_label, new_label)

with open("frontend/src/components/Controls/Link.vue", "w") as f:
    f.write(content)
