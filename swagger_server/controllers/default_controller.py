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
        if "first_name" not in json.keys() or "last_name" not in json.keys():
            return 'Invalid input', 405

        student = Student.from_dict(connexion.request.get_json())  # noqa: E501

        try:
            student_service.add_student(student)
            return student.first_name
        except ValueError:
            return 'already exists',409




def delete_student(student_id):  # noqa: E501
    """delete_student

     # noqa: E501

    :param student_id: ID of student to return
    :type student_id: int

    :rtype: Student
    """
    return 'do some magic!'


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
        return student_service.get_student_by_id(student_id, subject)
    except ValueError:
        return 'invalid id',404
