from freshsalessdk import FreshsalesSDK

fs = FreshsalesSDK(
    domain='fyle',
    api_key='tst3pko-tbg0QU3BhYuMeg'
)

# print(fs.contacts.get_views())

# view_id = 227218
# leads = fs.leads.get_all(view_id=view_id, limit=1)
# print(leads)

# print()
# print(fs.contacts.get_all_generator(view_id=4306216, limit=1))

deal_id = 14333555
lead = fs.leads.get(id=deal_id)
print(lead)

# view_id = 616464
# leads = fs.leads.get_views()
# accounts = fs.accounts.get_all(view_id=view_id, limit=1)
# print(leads)