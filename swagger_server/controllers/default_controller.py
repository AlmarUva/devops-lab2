import connexion
import six

from swagger_server.models.student import Student  # noqa: E501
from swagger_server import util
import swagger_server.service.student_service as student_service

def add_student(body):  # noqa: E501
    """Add a new student

     # noqa: E501

    :param body: Student object that needs to be added
    :type body: dict | bytes

    :rtype: int
    """

    if connexion.request.is_json:

        json = connexion.request.get_json()

        if not json:
            return 'Invalid input', 405

        if "first_name" not in json.keys() or "last_name" not in json.keys():
            return 'Invalid input', 405

        student = Student.from_dict(json)  # noqa: E501
        #raise Exception(str(student)) #use this as inband debugger
        try:
            s_id = student_service.add_student(student)
            return s_id, 200
        except ValueError:
            return 'already exists',409
    
    return 'Invalid input', 405



def delete_student(student_id):  # noqa: E501
    """delete_student

     # noqa: E501

    :param student_id: ID of student to return
    :type student_id: int

    :rtype: Student
    """
    try:
        student = student_service.delete_student(student_id)
        return student
    except ValueError:
        return 'invalid id', 404

def get_student_by_id(student_id, subject=None):  # noqa: E501
    """Find student by ID

    Returns a single student # noqa: E501

    :param student_id: ID of student to return
    :type student_id: int
    :param subject: The subject name
    :type subject: str

    :rtype: Student
    """
    try:
        student = student_service.get_student_by_id(student_id, subject)
        return student
        
    except ValueError:
        return 'invalid id',404

def get_student_by_query(student_id=None, subject=None, first_name=None, last_name=None):  # noqa: E501
    """Find student by query

    Returns a single student # noqa: E501

    :param student_id: ID of student to return
    :type student_id: int
    :param subject: The subject name
    :type subject: str
    :param first_name: The first name
    :type first_name: str
    :param last_name: The last name
    :type last_name: str

    :rtype: Student
    """
    try:
        student = student_service.get_student_by_query(student_id=student_id, subject=subject, first_name=first_name, last_name=last_name)
        return student
    except ValueError:
        return 'student not found',404