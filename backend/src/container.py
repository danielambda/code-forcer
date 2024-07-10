from src.application.contests.contests_provider import IContestsProvider
from src.application.contests.contests_service import ContestsService
from src.application.students.students_repository import IStudentsRepository
from src.application.students.students_service import StudentsService
from src.application.moodle_grades.moodle_grades_file_creator import MoodleGradesFileCreator
from src.infrastructure.code_forces.code_forces_request_sender import CodeForcesRequestsSender
from src.infrastructure.storage.db_students_repository import DBStudentsRepository
from src.infrastructure.code_forces.code_forces_contests_provider import CodeForcesContestsProvider
from src.utils.dependencies_container import DependenciesContainer

container = DependenciesContainer()

container[IContestsProvider] = lambda: CodeForcesContestsProvider(
    requests_sender_factory=CodeForcesRequestsSender,
    anonymous_requests_sender_factory=CodeForcesRequestsSender
)
container[IStudentsRepository] = lambda: DBStudentsRepository('students.db')

container[StudentsService] = lambda: StudentsService(container[IStudentsRepository], container[IContestsProvider])
container[ContestsService] = lambda: ContestsService(container[IContestsProvider], container[IStudentsRepository])
container[MoodleGradesFileCreator] = MoodleGradesFileCreator
