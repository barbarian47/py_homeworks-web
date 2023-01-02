import requests

response = requests.post('http://127.0.0.1:5000/advt',
                         json={
                             'title': 'ADVT #1',
                             'author': 'user1',
                             'description': 'sell old elephant'
                               })
print(response.status_code)
print(response.json())

response = requests.get('http://127.0.0.1:5000/advt/1')
print(response.status_code)
print(response.json())

response = requests.patch('http://127.0.0.1:5000/advt/1', json={
                                                            'title': 'TestTitle',
                                                            'description': '1111111111111111111111111',
                                                            'author': 'user3'
                                                            })

response = requests.get('http://127.0.0.1:5000/advt/1')
print(response.status_code)
print(response.json())

response = requests.delete('http://127.0.0.1:5000/advt/1')
print(response.status_code)
print(response.json())

response = requests.get('http://127.0.0.1:5000/advt/1')
print(response.status_code)
print(response.json())
