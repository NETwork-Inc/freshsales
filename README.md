# freshsales-sdk-py

Unofficial Python SDK for accessing [Freshsales](https://www.freshsales.io/api/).

*Warning*: This is undergoing active development and we will accept contributions once things are a little stable.

## Installation

1. Download this project and use it (copy it in your project, etc).
2. Install it from [pip](https://pypi.org).

```
pip install freshsalessdk
```

## Usage

To use this SDK you'll need these Freshsales credentials and your Freshsales domain (https://domain.freshsales.io). See [official documentation](https://www.freshsales.io/api/#intro) for steps. We'll assume these are available via environment variables thusly:

```
export FS_API_KEY=xxx
export FS_DOMAIN=yyy
```

The following snippet shows you how to initialize and use the SDK.

```python
from freshsalessdk import FreshsalesSDK
import os

fs = FreshsalesSDK(
    domain=os.getenv('FS_DOMAIN'),
    api_key=os.getenv('FS_API_KEY')
)

# get contact views
views = fs.contacts.get_views()

# get contacts in a view
view_id = 123
contacts = fs.contacts.get_all(view_id=view_id)
contacts = list(fs.contacts.get_all_generator(view_id=view_id))

# get specific contact
contact_id = 1232
contact = fs.contacts.get(id=contact_id)

# get contact activities
activities = fs.contacts.get_activities(id=contact_id)

# get account views
views = fs.accounts.get_views()

# get accounts in a view
view_id = 123
accounts = fs.accounts.get_all(view_id=view_id)
accounts = list(fs.accounts.get_all_generator(view_id=view_id))

# get one account
account_id = 1221
account = fs.accounts.get(id=account_id)

# get deal views
views = fs.deals.get_views()

# get deals in a view
view_id = 1212
deals = fs.deals.get_all(view_id=view_id)
deals = list(fs.deals.get_all_generator(view_id=view_id))

# get single deal
deal_id = 12121
deal = fs.deals.get(id=deal_id)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
