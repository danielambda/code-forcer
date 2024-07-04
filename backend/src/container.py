from application.contests.contests_provider import IContestsProvider
from application.contests.contests_service import ContestsService
from application.students.students_repository import IStudentsRepository
from application.students.students_service import StudentsService
from application.moodle_grades.moodle_grades_file_creator import MoodleGradesFileCreator
from infrastructure.code_forces.requests_sending.code_forces_request_sender import CodeForcesRequestsSender
from infrastructure.storage.db_students_repository import DBStudentsRepository
from infrastructure.code_forces.code_forces_contests_provider import CodeForcesContestsProvider
from utils.dependencies_container import DependenciesContainer

container = DependenciesContainer()
container[IStudentsRepository] = DBStudentsRepository('students.db')
container[IContestsProvider] = CodeForcesContestsProvider(
    requests_sender_factory=lambda key, secret: CodeForcesRequestsSender(key, secret),
    anonymous_requests_sender_factory=lambda: CodeForcesRequestsSender()
)

container[StudentsService] = StudentsService(container[IStudentsRepository], container[IContestsProvider])
container[ContestsService] = ContestsService(container[IContestsProvider], container[IStudentsRepository])
container[MoodleGradesFileCreator] = MoodleGradesFileCreator()
