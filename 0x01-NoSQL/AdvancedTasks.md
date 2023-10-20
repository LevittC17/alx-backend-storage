13. Regex filter
#advanced

Write a script that lists all `documents` with name starting by `Holberton` in the collection `school`:

The database name will be passed as option of `mongo` command

```bash
guillaume@ubuntu:~/0x01$ cat 100-find | mongo my_db
MongoDB shell version v3.6.3
connecting to: mongodb://127.0.0.1:27017/my_db
MongoDB server version: 3.6.3
{ "_id" : ObjectId("5a90731fd4321e1e5a3f53e3"), "name" : "Holberton school" }
{ "_id" : ObjectId("5a90731fd4321e1e5a3f53e3"), "name" : "Holberton School" }
{ "_id" : ObjectId("5a90731fd4321e1e5a3f53e3"), "name" : "Holberton-school" }
bye
guillaume@ubuntu:~/0x01$
```

**Repo:**
  **GitHub repository: `alx-backend-storage`**
  **Directory: `0x01-NoSQL`**
  **File: `100-find`**


14. Top students
#advanced

Write a Python function that returns all students sorted by average score:
  Prototype: `def top_students(mongo_collection):`
  `mongo_collection` will be the `pymongo` collection object
  The top must be ordered
  The average score must be part of each item returns with key = `averageScore`

```bash
guillaume@ubuntu:~/0x01$ cat 101-main.py
#!/usr/bin/env python3
""" 101-main """
from pymongo import MongoClient
list_all = __import__('8-all').list_all
insert_school = __import__('9-insert_school').insert_school
top_students = __import__('101-students').top_students

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students

    j_students = [
        { 'name': "John", 'topics': [{ 'title': "Algo", 'score': 10.3 },{ 'title': "C", 'score': 6.2 }, { 'title': "Python", 'score': 12.1 }]},
        { 'name': "Bob", 'topics': [{ 'title': "Algo", 'score': 5.4 },{ 'title': "C", 'score': 4.9 }, { 'title': "Python", 'score': 7.9 }]},
        { 'name': "Sonia", 'topics': [{ 'title': "Algo", 'score': 14.8 },{ 'title': "C", 'score': 8.8 }, { 'title': "Python", 'score': 15.7 }]},
        { 'name': "Amy", 'topics': [{ 'title': "Algo", 'score': 9.1 },{ 'title': "C", 'score': 14.2 }, { 'title': "Python", 'score': 4.8 }]},
        { 'name': "Julia", 'topics': [{ 'title': "Algo", 'score': 10.5 },{ 'title': "C", 'score': 10.2 }, { 'title': "Python", 'score': 10.1 }]}
    ]
    for j_student in j_students:
        insert_school(students_collection, **j_student)

    students = list_all(students_collection)
    for student in students:
        print("[{}] {} - {}".format(student.get('_id'), student.get('name'), student.get('topics')))

    top_students = top_students(students_collection)
    for student in top_students:
        print("[{}] {} => {}".format(student.get('_id'), student.get('name'), student.get('averageScore')))

guillaume@ubuntu:~/0x01$
guillaume@ubuntu:~/0x01$ ./101-main.py
[5a90776bd4321e1ec94fc408] John - [{'title': 'Algo', 'score': 10.3}, {'title': 'C', 'score': 6.2}, {'title': 'Python', 'score': 12.1}]
[5a90776bd4321e1ec94fc409] Bob - [{'title': 'Algo', 'score': 5.4}, {'title': 'C', 'score': 4.9}, {'title': 'Python', 'score': 7.9}]
[5a90776bd4321e1ec94fc40a] Sonia - [{'title': 'Algo', 'score': 14.8}, {'title': 'C', 'score': 8.8}, {'title': 'Python', 'score': 15.7}]
[5a90776bd4321e1ec94fc40b] Amy - [{'title': 'Algo', 'score': 9.1}, {'title': 'C', 'score': 14.2}, {'title': 'Python', 'score': 4.8}]
[5a90776bd4321e1ec94fc40c] Julia - [{'title': 'Algo', 'score': 10.5}, {'title': 'C', 'score': 10.2}, {'title': 'Python', 'score': 10.1}]
[5a90776bd4321e1ec94fc40a] Sonia => 13.1
[5a90776bd4321e1ec94fc40c] Julia => 10.266666666666666
[5a90776bd4321e1ec94fc408] John => 9.533333333333333
[5a90776bd4321e1ec94fc40b] Amy => 9.366666666666665
[5a90776bd4321e1ec94fc409] Bob => 6.066666666666667
guillaume@ubuntu:~/0x01$
```

**Repo:**
  **GitHub repository: `alx-backend-storage`**
  **Directory: `0x01-NoSQL`**
  **File: `101-students.py`**


15. Log stats - new version
#advanced

Improve `12-log_stats.py` by adding the top 10 of the most present IPs in the collection `nginx` of the database `logs`:

  - The IPs top must be sorted (like the example below)

```bash
guillaume@ubuntu:~/0x01$ ./102-log_stats.py
94778 logs
Methods:
    method GET: 93842
    method POST: 229
    method PUT: 0
    method PATCH: 0
    method DELETE: 0
47415 status check
IPs:
    172.31.63.67: 15805
    172.31.2.14: 15805
    172.31.29.194: 15805
    69.162.124.230: 529
    64.124.26.109: 408
    64.62.224.29: 217
    34.207.121.61: 183
    47.88.100.4: 166
    45.249.84.250: 160
    216.244.66.228: 150
guillaume@ubuntu:~/0x01$
```

**Repo:**
  **GitHub repository: `alx-backend-storage`**
  **Directory: `0x01-NoSQL`**
  **File: `102-log_stats.py`**
