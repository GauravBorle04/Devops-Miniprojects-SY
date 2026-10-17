import threading


class Database:
    """Thread-safe in-memory database store for the Student Record Platform."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._init_db()
            return cls._instance

    def _init_db(self):
        self.students = {}
        self.faculty = {}
        self.courses = {}
        self.enrollments = []
        self._seed_initial_data()

    def _seed_initial_data(self):
        # Seed default students
        self.students["S101"] = {
            "student_id": "S101",
            "name": "Alice Johnson",
            "email": "alice@university.edu",
            "semester": 1,
            "active_credits": 0
        }
        self.students["S102"] = {
            "student_id": "S102",
            "name": "Rahul Verma",
            "email": "rahul@university.edu",
            "semester": 1,
            "active_credits": 0
        }
        # Seed default faculty
        self.faculty["F201"] = {
            "faculty_id": "F201",
            "name": "Dr. Robert Smith",
            "department": "Computer Science"
        }
        # Seed default course catalog
        self.courses["C101"] = {
            "course_id": "C101",
            "title": "Cloud Computing and DevOps",
            "credits": 4,
            "faculty_id": "F201",
            "slot": "MON-09",
            "capacity": 30,
            "enrolled": 0
        }
        self.courses["C102"] = {
            "course_id": "C102",
            "title": "Data Structures and Algorithms",
            "credits": 4,
            "faculty_id": "F201",
            "slot": "TUE-09",
            "capacity": 30,
            "enrolled": 0
        }
        self.courses["C103"] = {
            "course_id": "C103",
            "title": "Database Management Systems",
            "credits": 3,
            "faculty_id": "F201",
            "slot": "MON-09",
            "capacity": 30,
            "enrolled": 0
        }

    def reset(self):
        """Helper to restore state during unit testing teardowns."""
        with self._lock:
            self.students.clear()
            self.faculty.clear()
            self.courses.clear()
            self.enrollments.clear()
            self._seed_initial_data()


db = Database()
