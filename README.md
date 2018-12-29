# MongoStructure.py
Scan MongoDB Collection Structure

## Usage
```shell
$ python MongoStructure.py --help
usage: MongoStructure.py [-h] [-v] [-p PORT] [-o {tree,path}]
                         host database collection

Scan MongoDB Collection Structure

positional arguments:
  host                  mongoDB Server host
  database              mongoDB Database name
  collection            mongoDB Collection name

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -p PORT, --port PORT  mongoDB Server host
  -o {tree,path}, --out_type {tree,path}
                        default is value: tree

```

## Exsample
### db.getCollection('Human').find({})
```js
/* 1 */
{
    "_id" : ObjectId("5c27107a29c1889ae83291f6"),
    "tag" : "student",
    "birthday" : ISODate("2017-08-04T06:38:11.480Z"),
    "girlfriend" : {
        "name" : "mari",
        "age" : 21.0
    },
    "scores" : {
        "math" : 98.0,
        "chemical" : 95.0
    }
}

/* 2 */
{
    "_id" : ObjectId("5c27118829c1889ae83291f7"),
    "tag" : "python-man",
    "birthday" : null,
    "girlfriend" : null,
    "salary" : {
        "work" : "¥5000/month",
        "other" : "¥5/year"
    }
}
```

```
$ python MongoStructure.py  10.188.188.22 test Human
Collection Structure: 100%|█████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 756.75it/s]
Done!
========== test.Human ==========
|____ _id : bson.objectid.ObjectId
|____ birthday : NoneType, datetime.datetime
|____ girlfriend : NoneType, dict
|	|____ age : float
|	|____ name : str
|____ salary : dict
|	|____ other : str
|	|____ work : str
|____ scores : dict
|	|____ chemical : float
|	|____ math : float
|____ tag : str
========== test.Human ==========

```
```
$ python MongoStructure.py  10.188.188.22 test Human -o path
Collection Structure: 100%|█████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 814.98it/s]
Done!
========== test.Human ==========
_id
birthday
girlfriend
girlfriend.age
girlfriend.name
salary
salary.other
salary.work
scores
scores.chemical
scores.math
tag
========== test.Human ==========

```
