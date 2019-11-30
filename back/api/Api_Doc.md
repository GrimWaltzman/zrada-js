Файл зі специфікацією API

get.py - Набір методів які дозволяють отримати дані. 
Доступні по методу GET і POST

post.py - Набір методів які змінюють дані в базі, добавляють нові
Доступні по методу POST

GET API:

Get laws: url - /api/laws
parameters "limit", "skip"

Example:

```json
GET /api/laws
Body:
{
    "limit":  5,
    "skip":   7
}
```
Response
200 OK
```json
[
    {
        "_id": {"$oid": "5db9ce80c7f00f185899b318"},
        "title": null, 
        "body": null, 
        "author": null, 
        "date": null, 
        "date_in_base": "2019-10-30 19:55:12.263862", 
        "editor": "test2@test.com"
    }, 
    {
        "_id": {"$oid": "5db9f65fbf4eeadf2f4c33a2"},
        "title": null, 
        "body": null, 
        "author": null, 
        "date": null, 
        "date_in_base": "2019-10-30 22:45:19.912484", 
        "editor": "test2@test.com"}, 
    {
        "_id": {"$oid": "5db9f6d25b556559e3e5b4cd"},
        "title": null, 
        "body": null, 
        "author": null, 
        "date": null, 
        "date_in_base": "2019-10-30 22:47:14.552525", 
        "editor": "test2@test.com"}, 
    {
        "_id": {"$oid": "5db9f74ebc580b0e3314db32"},
        "title": "test", 
        "body": "test", 
        "author": "test", 
        "date": "1111-11-11", 
        "date_in_base": "2019-10-30 22:49:18.429900", 
        "editor": "test2@test.com"}, 
    {
        "_id": {"$oid": "5db9f855e7e993992e0ab93e"},
        "title": "test", 
        "body": "test", 
        "author": "test", 
        "date": "1111-11-11", 
        "date_in_base": "2019-10-30 22:53:41.021322", 
        "editor": "test2@test.com"}
]




```
this skip first 7 laws in DB and returns next 5 (or less, if don`t exist)

default: limit=10, skip=0

limit=0 returns all laws after skipped

Get law: url - /api/law
parameters "_id"
```json
GET /api/laws
Body:
{
    "_id":"5db9c56edb7bdcb1fe78f8e5"
}
```
Response
200 OK
```json
{
    "_id": {"$oid": "5db9c56edb7bdcb1fe78f8e5"},
    "title": null,
    "body": null,
    "author": null,
    "date": null,
    "date_in_base": "2019-10-30 19:16:30.505834",
    "editor": "test2@test.com"
}
```

POST API

Delete law: url - /api/law_del
parameters "_id"
```json
POST /api/law_del
Body:
{
    "_id":"5db9c56edb7bdcb1fe78f8e5"
}
```

Response
200 OK
```json
{"result": "OK"}
```

Vote law: url - /api/vote
parameters "_id"
```json
POST /api/vote
Body:
{
  "_id":"5db9c56edb7bdcb1fe78f8e5"
}

```

Response
200 OK
```json
{"result": "OK"}
```