# Enterprise Student Record & Academic Management Platform

A Flask REST API and web dashboard for managing students, faculty, courses,
enrollments and academic marks. The project demonstrates a complete DevOps
delivery pipeline: Git/GitHub, Jenkins CI, Docker and Kubernetes (Minikube).

## Business rules
* A student may enroll in at most **18 credits** per semester.
* Two courses with the same timetable slot cannot be taken together.
* A course cannot exceed its capacity, and a student cannot enroll twice.
* Marks are 0-100 and map to grade points (A=4, B=3, C=2, D=1, F=0).
* GPA is credit-weighted.

## Run locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py            # http://localhost:5000
```

## Run the tests
```bash
pytest -v --cov=app --cov-report=term-missing --junitxml=reports/test-results.xml tests/
```

## API
| Method | Endpoint                    | Purpose                     |
|--------|-----------------------------|-----------------------------|
| GET    | /api/health                 | Liveness / readiness probe  |
| POST   | /api/students               | Register a student          |
| GET    | /api/students/<id>          | Fetch a student             |
| GET    | /api/students/<id>/gpa      | Credit-weighted GPA         |
| GET    | /api/courses?q=             | Search the course catalog   |
| POST   | /api/courses                | Add a course                |
| POST   | /api/enroll                 | Enroll a student            |
| POST   | /api/drop                   | Drop a course               |
| POST   | /api/marks                  | Record marks                |

## Container
```bash
docker build -t student-academic-platform:v1.0.0 .
docker run -d -p 5000:5000 --name student-container student-academic-platform:v1.0.0
```

## Kubernetes (Minikube)
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml      # NodePort 30090
```
