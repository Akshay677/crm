with open("frontend/src/components/QuickFilterField.vue", "r") as f:
    content = f.read()

content = content.replace(
    'v-else-if="filter.fieldtype === \'Select\'"',
    'v-else-if="filter.fieldtype === \'Select\'"\n    class="quick-filter-autocomplete"'
)

style_block = """
<style>
.quick-filter-autocomplete button span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
"""

if "<style>" not in content:
    content += style_block

with open("frontend/src/components/QuickFilterField.vue", "w") as f:
    f.write(content)
