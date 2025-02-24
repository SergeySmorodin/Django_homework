import pytest

URL = '/api/v1/courses/'


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    """Проверка получения первого курса """
    # Создаем курс через фабрику
    course = course_factory(name="Python")

    url = URL + f"{course.id}/"
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == "Python"


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    """Проверка получения списка курсов """
    # Создаем несколько курсов через фабрику
    course_factory(name="Python")
    course_factory(name="Java")

    url = URL
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """Проверка фильтрации списка курсов по id"""
    # Создаем курсы через фабрику
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

    url = URL
    response = api_client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Java"


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Тест успешного обновления курса"""
    course = course_factory(name="Java")

    data = {"name": "Python"}

    # Делаем запрос на обновление курса
    url = URL + f"{course.id}/"
    response = api_client.patch(url, data, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Python"


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Тест успешного удаления курса"""
    course = course_factory(name="Python")

    # Делаем запрос на удаление курса
    url = URL + f"{course.id}/"
    response = api_client.delete(url)

    assert response.status_code == 204

    # Проверяем, что курс действительно удален
    response = api_client.get(url)
    assert response.status_code == 404
