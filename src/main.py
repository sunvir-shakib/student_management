from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Student Management API")

# ---------- Data Model ----------

class Student(BaseModel):
    id: int
    name: str
    department: str
    semester: int = Field(..., gt=0, le=8)
    cgpa: float = Field(..., ge=0.0, le=4.0)


# ---------- In-memory "database" ----------

students: dict[int, Student] = {}


# ---------- Routes ----------

@app.get("/")
def root():
    return {"message": "Student Management API is running"}


@app.get("/students", response_model=list[Student])
def get_all_students():
    return list(students.values())


@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]


@app.post("/students", response_model=Student, status_code=201)
def create_student(student: Student):
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student with this ID already exists")
    students[student.id] = student
    return student


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    if updated_student.id != student_id:
        raise HTTPException(status_code=400, detail="Path ID and body ID must match")
    students[student_id] = updated_student
    return updated_student


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": f"Student {student_id} deleted successfully"}
