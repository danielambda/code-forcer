import pytest

from src.container import container
from src.features.contests.interfaces import IContestsProvider
from src.features.students.interfaces import IStudentsRepository
from src.features.students.model import Student
from tests.mocks.data_generation import fake as outer_fake
from tests.mocks.contests_provider_mock import ContestsProviderMock
from tests.mocks.students_repository_mock import StudentRepositoryMock


@pytest.fixture()
def fake():
    return outer_fake


@pytest.fixture(autouse=True)
def setup_and_teardown(contests_provider_mock, students_repo_mock):
    yield
    contests_provider_mock.valid_handles = []
    students_repo_mock.db.clear()
    print('mocks cleared')


@pytest.fixture
def contests_provider_mock():
    contests_provider_mock = ContestsProviderMock()
    container[IContestsProvider] = contests_provider_mock
    return contests_provider_mock


@pytest.fixture
def students_repo_mock():
    students_repo_mock = StudentRepositoryMock()
    container[IStudentsRepository] = students_repo_mock
    return students_repo_mock


@pytest.fixture
def email(fake):
    return fake.email()


@pytest.fixture
def existing_email(students_repo_mock, fake):
    email = fake.email()
    handle = fake.word()

    if not students_repo_mock.db.get(email):
        students_repo_mock.db[email] = Student(email=email, handle=handle)

    return email


@pytest.fixture
def invalid_email(fake):
    return fake.email() + '!'


@pytest.fixture
def handle(contests_provider_mock, fake):
    handle = fake.word()
    contests_provider_mock.valid_handles = [handle]
    return handle


@pytest.fixture
def existing_handle(students_repo_mock, contests_provider_mock, fake):
    email = fake.email()
    handle = fake.word()

    contests_provider_mock.valid_handles = [handle]

    if not students_repo_mock.db.get(email):
        students_repo_mock.db[email] = Student(email=email, handle=handle)

    return handle


@pytest.fixture
def invalid_handle(fake):
    return fake.word()
