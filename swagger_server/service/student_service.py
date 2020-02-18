import json
import logging
import os
import tempfile

from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from functools import reduce
import uuid

from swagger_server.models import Student

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)
#student_db.purge_tables()

def add_student(student):
    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        raise ValueError

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id


def get_student_by_id(student_id, subject):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        raise ValueError
    student = Student.from_dict(student)
    
    if student:
        if subject:
            if student.grades and not subject in student.grades.keys():
                raise ValueError("subject not in grades")

    return student
    

def get_student_by_query(first_name=None, last_name=None, subject=None, student_id=None):
    if student_id:
        student = student_db.get(doc_id=int(student_id))
        if not student:
            raise ValueError
        if student:
            try:
                if check_sanity(student,first_name,last_name,subject,student_id):      
                    return student
                else: 
                    raise ValueError
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                raise ValueError
                    
    
    query = Query()
    queries = []
    if first_name:
        queries.append(query.first_name == first_name)
    if last_name:
        queries.append(query.last_name == last_name)
    
    #it is impossible to identify students based on first and last name only as they are not unique keys. The test 14 is therefore not really to be used but only for this lab.
    if first_name and last_name:
        query = reduce(lambda a,b: a & b)
        res = student_db.search(query)
    else:
        res = student_db.search(queries[0])
    if res:
        return res[0]
    else:
        raise ValueError





def check_sanity(student, first_name=None, last_name=None, subject=None, student_id=None):
    result = True
    
    if first_name:
        result = result and student.first_name == first_name
    if last_name:
        result = result and student.last_name == last_name
    if subject:
        result = result and subject in student.grades.keys()
    if student_id:
        result = result and student.student_id == student_id
    return result



def delete_student(student_id):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        raise ValueError
    student_db.remove(doc_ids=[int(student_id)])
    return student