# Seating & Duty Records Dataset

This dataset contains 100 realistic exam seating and duty records, which map student seating details to their exam sessions, halls, subjects, and supervising invigilators. It is designed to be used for search indexing, UI rendering, and machine learning prediction tasks.

## File Location
- **CSV Data File**: [seating_duty_records.csv](file:///C:/Users/lenovo/Desktop/exam_seating_system/data/seating_duty_records.csv)

---

## Schema and Data Dictionary

The table below describes each field in the dataset, its data type, and the permissible values it can take.

| Column Name | Data Type | Description | Permissible/Example Values |
| :--- | :--- | :--- | :--- |
| `record_id` | String | A unique alphanumeric identifier for each seating and duty record. | `REC001` to `REC100` |
| `exam_date` | String | The date the exam was administered, represented in `YYYY-MM-DD` format. | `2026-05-01` to `2026-07-20` (plus outlier `2026-12-25`) |
| `session` | String | The session block of the exam. | `Morning` (usually 09:00 AM) or `Afternoon` (usually 02:00 PM) |
| `hall` | String | The examination hall or room where the exam took place. | `Hall A`, `Hall B`, `Hall C`, `Gymnasium` (plus outlier `Storage Room C`) |
| `seat_no` | String | The specific seat identifier assigned to the student. Blank if unassigned. | Alphanumeric (e.g., `A-01`, `B-12`, `G-35`) or `""` (missing value) |
| `student_id` | String | The unique identifier of the student. | `STU101` to `STU120` (plus outlier `STU999`) |
| `subject` | String | The course/subject code or name of the exam. | `Mathematics`, `Computer Science`, `Physics`, `Chemistry`, `Biology` (plus outlier `Astrology`) |
| `invigilator` | String | The full name of the academic staff member supervising the exam session. | e.g., `Dr. Ashwini Sekar`, `Dr. Ashwani Sekar`, or `""` (missing value) |
| `student_attendance` | String | The target prediction variable, indicating if the student was present or absent. | `Present` or `Absent` |

---

## Injected Awkward Cases

To test UI edge cases, search capabilities, and validation rules in subsequent phases, we have deliberately injected three types of anomalies:

### 1. Missing Values (Blank Fields)
These are blank strings (`""`) in the CSV, representing unrecorded or unassigned attributes:
- **`REC098`**: The `invigilator` field is missing/blank. This tests how the UI renders when an exam is unstaffed or when the coordinator has not yet assigned a duty.
- **`REC099`**: The `seat_no` field is missing/blank. This tests how the system handles unassigned seating records and whether it displays a placeholder.

### 2. Extremely Similar Names
These test the search functionality's precision and query handling (e.g., soundex, fuzzy matching, or strict filtering):
- **Invigilators**:
  - `Dr. Ashwini Sekar` (Multiple records)
  - `Dr. Ashwani Sekar` (Multiple records - very similar spelling)
  - `Dr. Robert Smith` (Multiple records)
  - `Dr. Rupert Smith` (Multiple records - very similar spelling)
- **Students**:
  - `John Smith` and `Jon Smith` (can be added as names if student details are queried, or mapped to test text search queries).

### 3. Isolated / Orphan Record
This tests search constraints, filtering logic, and how the dashboard behaves with isolated entities that have no relation to any other records:
- **`REC100`**:
  - **Date**: `2026-12-25` (Christmas Day, which is outside the active exam window of May-July 2026).
  - **Hall**: `Storage Room C` (Only appears in this record).
  - **Seat**: `Z-99` (Only appears in this record).
  - **Student ID**: `STU999` (Only student with this ID, does not exist in standard student rosters).
  - **Subject**: `Astrology` (Only exam for this subject).
  - **Invigilator**: `Dr. Orphan` (Only appears once).

---

## Target Prediction Variable: `student_attendance`

The `student_attendance` column records the outcome we intend to predict. To make the dataset suitable for machine learning, the generation script injects realistic statistical correlations:
1. **Student History**:
   - `STU105` has a high chronic absence rate (~65% absent).
   - `STU108` has a moderate chronic absence rate (~50% absent).
   - All other students are highly reliable (~95% present).
2. **Session Effects**:
   - `Morning` sessions suffer a 5% higher absence rate than `Afternoon` sessions due to oversleeping or transit delays.
   - `Afternoon` sessions have highly reliable attendance.
3. **Subject Difficulty**:
   - `Physics` has a 10% higher absence rate.
   - `Mathematics` has a 5% higher absence rate.
   
These statistical features ensure a classification model (e.g., Logistic Regression or Decision Trees) can learn from the historical records to predict student attendance outcomes based on student ID, session, and subject.
