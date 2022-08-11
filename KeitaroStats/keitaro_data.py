import os

import requests

token = os.environ.get('API_TOKEN')


def get_report(date_from, date_to, name='bogdan'):
    data = requests.post(
        'http://136.244.93.168/admin_api/v1/report/build',
        headers={'Api-Key': token},
        json={"range": {
            "from": date_from.strftime('%Y-%m-%d'),
            "to": date_to.strftime('%Y-%m-%d'),
            "timezone": "GMT+3"
        },
            "filters": [
                {
                    "name": "sub_id_6",
                    "operator": "EQUALS",
                    "expression": name
                }
            ]
        })
    return data.json()
