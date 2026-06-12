STUDENT = {
    "reg_no": "TEST-001",
    "name": "Test Student",
    "semester": 6,
    "section": "A",
}


def test_create_student_returns_201(client):
    response = client.post("/students", json=STUDENT)
    assert response.status_code == 201


def test_create_student_returns_correct_data(client):
    response = client.post("/students", json={**STUDENT, "reg_no": "TEST-002"})
    data = response.json()
    assert data["name"] == "Test Student"
    assert data["semester"] == 6


def test_create_student_has_id(client):
    response = client.post("/students", json={**STUDENT, "reg_no": "TEST-ID"})
    data = response.json()
    assert "id" in data


def test_get_all_students_returns_list(client):
    response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_student_by_reg_no(client):
    client.post("/students", json={**STUDENT, "reg_no": "TEST-003"})
    response = client.get("/students/TEST-003")
    assert response.status_code == 200
    assert response.json()["reg_no"] == "TEST-003"


def test_get_nonexistent_student_returns_404(client):
    response = client.get("/students/DOES-NOT-EXIST")
    assert response.status_code == 404


def test_duplicate_reg_no_returns_409(client):
    client.post("/students", json={**STUDENT, "reg_no": "TEST-DUP"})
    response = client.post("/students", json={**STUDENT, "reg_no": "TEST-DUP"})
    assert response.status_code == 409
