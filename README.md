# tsschecker-django
A batch TSSChecker implemented in Django.

## Dependency
- Redis
- [rq](https://github.com/rq/rq)
- [tsschecker](https://github.com/encounter/tsschecker)

## Usage
Once deployed, create a super user, then access admin panel via `http://localhost:8000/admin/`.

## API
```python
#!/usr/bin/python

import os
import requests

flist = os.listdir('deviceinfo')
for i in range(0, len(flist)):
    path = os.path.join('deviceinfo', flist[i])
    if os.path.isfile(path):
        f = open(path)
        contents = f.read()
        carr = contents.split('-')
        f.close()
        print(carr)
        device_name = flist[i].split('.')[0]
        ecid = carr[0]
        hw_model = carr[1]
        product_type = carr[2]
        ios_version = carr[3]
        post_data = {
            'async': True,
            'name': device_name,
            'hw_model': hw_model,
            'product_type': product_type,
            'ios_version': ios_version,
            'ecid': ecid
        }
        response = requests.post('http://127.0.0.1:8000/api/register/', data=post_data)
        print(response.text)
        postData['ios_version'] = '11.4.1'  # the blob version to fetch, must be available to be signed by apple
        response = requests.post('http://127.0.0.1:8000/api/sign/', data=post_data)
        print(response.text)

```
