import os

def replace_in_file(filepath, replacements):
    with open(filepath, 'r') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(content)

replacements = [
    ('OrganizationsListView', 'TeamProfilesListView'),
    ('organizationsListView', 'teamProfilesListView'),
    ('Organizations', 'Team Profiles'),
    ('organizations', 'teamProfiles'),
    ('CRM Organization', 'Team Profile'),
    ('OrganizationModal', 'TeamProfileModal'),
    ('showOrganizationModal', 'showTeamProfileModal'),
    ('organizationId', 'teamProfileId'),
    ('Organization', 'Team Profile'),
    ('organization', 'teamProfile'),
    ('crm_organization', 'team_profile'),
]

replace_in_file('frontend/src/pages/TeamProfiles.vue', replacements)
replace_in_file('frontend/src/components/ListViews/TeamProfilesListView.vue', replacements)
replace_in_file('frontend/src/components/Modals/TeamProfileModal.vue', replacements)
replace_in_file('frontend/src/pages/TeamProfile.vue', replacements)
replace_in_file('frontend/src/pages/MobileTeamProfile.vue', replacements)
