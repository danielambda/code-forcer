from datetime import datetime, timedelta

from fastapi import status

from src.features.contests.models import Contest, Problem, Submission
from src.features.students.models import Student
from tests.create_test_client import client

from src.features.moodle_grades.models import MoodleResultsData, LateSubmissionPolicyData


def test_get_moodle_grades_if_data_is_valid():
    moodle_result_data = MoodleResultsData(
        contest=Contest(
            id=1,
            name='test contest',
            start_time_utc=datetime.now(),
            duration=timedelta(days=3),
            problems=[
                Problem(
                    name='test problem 1',
                    index='A',
                    max_points=50,
                    submissions=[
                        Submission(
                            id=1,
                            author=Student(
                                email='a@a.a',
                                handle='a'
                            ),
                            is_successful=False,
                            passed_test_count=5,
                            points=20,
                            programming_language='Python',
                            submission_time_utc=datetime.now(),
                        ),
                        Submission(
                            id=3,
                            author=Student(
                                email='b@b.b',
                                handle='b'
                            ),
                            is_successful=False,
                            passed_test_count=8,
                            points=30,
                            programming_language='Java',
                            submission_time_utc=datetime.now() + timedelta(hours=2),
                        ),
                        Submission(
                            id=5,
                            author=Student(
                                email='c@c.c',
                                handle='c'
                            ),
                            is_successful=True,
                            passed_test_count=10,
                            points=50,
                            programming_language='C++',
                            submission_time_utc=datetime.now() + timedelta(hours=3),
                        )
                    ]
                ),
                Problem(
                    name='test problem 2',
                    index='B',
                    max_points=30,
                    submissions=[
                        Submission(
                            id=5,
                            author=Student(
                                email='c@c.c',
                                handle='c'
                            ),
                            is_successful=True,
                            passed_test_count=52,
                            points=30,
                            programming_language='C++',
                            submission_time_utc=datetime.now() + timedelta(days=5),
                        ),
                        Submission(
                            id=5,
                            author=Student(
                                email='a@a.a',
                                handle='a'
                            ),
                            is_successful=False,
                            passed_test_count=32,
                            points=18,
                            programming_language='Python',
                            submission_time_utc=datetime.now() + timedelta(days=1),
                        )
                    ]
                )
            ],
        ),
        problem_max_grade_by_index={'A': 100, 'B': 60},
        legal_excuses={},
        late_submission_policy=LateSubmissionPolicyData(
            penalty=0.2,
            extra_time=259200
        )
    )

    expected_output = 'Email,test contest Grade,test contest Feedback\r\na@a.a,76.0,\r\nb@b.b,60.0,\r\nc@c.c,148.0,\r\n'

    response = client.post("/moodle_grades", data=moodle_result_data.model_dump_json())

    assert response.status_code == status.HTTP_200_OK
    assert response.text == expected_output
