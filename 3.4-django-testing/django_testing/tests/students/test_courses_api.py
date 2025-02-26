import pytest
from django.core.exceptions import ValidationError
from students.models import Student, Course

URL = '/api/v1/courses/'


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    """Проверка получения первого курса """
    # Создаем курс через фабрику
    course = course_factory(name="Python", _bulk_create=False)

    url = URL + f"{course.id}/"
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == "Python"


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    """Проверка получения списка курсов """
    course_factory(name="Python")
    course_factory(name="Java")

    response = api_client.get(URL)

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """Проверка фильтрации списка курсов по id"""
    course1 = course_factory(name="Python")
    course_factory(name="Java")

    url = URL + f"?id={course1.id}"
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Python"


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    """Проверка фильтрации списка курсов по name"""
    course_factory(name="Python")
    course_factory(name="Java")

    url = URL + "?name=Python"
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Python"


@pytest.mark.django_db
def test_create_course(api_client):
    """Тест успешного создания курса"""
    data = {"name": "Java", "description": "This is a new course"}

    response = api_client.post(URL, data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Java"


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Тест успешного обновления курса"""
    course = course_factory(name="Java")

    data = {"name": "Python"}

    url = URL + f"{course.id}/"
    response = api_client.patch(url, data, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Python"


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Тест успешного удаления курса"""
    course = course_factory(name="Python")

    url = URL + f"{course.id}/"
    response = api_client.delete(url)

    assert response.status_code == 204

    # Проверяем, что курс действительно удален
    response = api_client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    "max_students, num_students_to_add, should_succeed",
    [
        (5, 5, True),
        (5, 6, False),
        (10, 10, True),
        (10, 11, False)
    ],
    ids=[
        "add 5 students",
        "add 6 students",
        "add 10 students",
        "add 11 students"
    ]
)
def test_max_students_per_course(settings, max_students, num_students_to_add, should_succeed):
    settings.MAX_STUDENTS_PER_COURSE = max_students

    course = Course.objects.create(name="Python")
    students = [Student.objects.create(name=f"Student {i}") for i in range(num_students_to_add)]

    try:
        for student in students:
            course.add_student(student)

        assert should_succeed, "Ожидалась ошибка, но она не возникла"
        assert course.students.count() == num_students_to_add

    except ValidationError as e:
        assert not should_succeed, f"Не ожидалась ошибка, но возникла: {e}"
