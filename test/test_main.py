from fastapi.testclient import TestClient
from main import app, students

client = TestClient(app)


def setup_function():
    """Reset the in-memory 'database' before every test."""
    students.clear()


VALID_STUDENT = {
    "id": 1,
    "name": "Ayesha Rahman",
    "department": "CSE",
    "semester": 5,
    "cgpa": 3.75,
}


# ---------- POST ----------

def test_create_student_success():
    response = client.post("/students", json=VALID_STUDENT)
    assert response.status_code == 201
    assert response.json()["name"] == "Ayesha Rahman"


def test_create_student_duplicate_id_fails():
    client.post("/students", json=VALID_STUDENT)
    response = client.post("/students", json=VALID_STUDENT)
    assert response.status_code == 400


def test_create_student_invalid_cgpa_fails():
    # Invalid scenario 1: cgpa out of allowed range (>4.0)
    bad_student = {**VALID_STUDENT, "id": 2, "cgpa": 5.5}
    response = client.post("/students", json=bad_student)
    assert response.status_code == 422


def test_create_student_invalid_semester_fails():
    # Invalid scenario 2: semester out of allowed range (>8)
    bad_student = {**VALID_STUDENT, "id": 3, "semester": 10}
    response = client.post("/students", json=bad_student)
    assert response.status_code == 422


def test_create_student_missing_field_fails():
    # Invalid scenario 3: required field missing
    bad_student = {"id": 4, "name": "No Department"}
    response = client.post("/students", json=bad_student)
    assert response.status_code == 422


# ---------- GET ----------

def test_get_all_students_success():
    client.post("/students", json=VALID_STUDENT)
    response = client.get("/students")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_single_student_success():
    client.post("/students", json=VALID_STUDENT)
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_single_student_not_found_fails():
    response = client.get("/students/999")
    assert response.status_code == 404


# ---------- PUT ----------

def test_update_student_success():
    client.post("/students", json=VALID_STUDENT)
    updated = {**VALID_STUDENT, "cgpa": 3.9}
    response = client.put("/students/1", json=updated)
    assert response.status_code == 200
    assert response.json()["cgpa"] == 3.9


def test_update_student_not_found_fails():
    updated = {**VALID_STUDENT, "id": 42}
    response = client.put("/students/42", json=updated)
    assert response.status_code == 404


def test_update_student_id_mismatch_fails():
    client.post("/students", json=VALID_STUDENT)
    mismatched = {**VALID_STUDENT, "id": 2}
    response = client.put("/students/1", json=mismatched)
    assert response.status_code == 400


# ---------- DELETE ----------

def test_delete_student_success():
    client.post("/students", json=VALID_STUDENT)
    response = client.delete("/students/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Student 1 deleted successfully"


def test_delete_student_not_found_fails():
    response = client.delete("/students/999")
    assert response.status_code == 404
