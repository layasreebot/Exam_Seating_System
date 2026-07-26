# Exam Seating & Duty Register Query Assistant

## Problem Statement (2-Line Summary)
Manual prep of exam seating and invigilator duties often leads to double-booking and layout errors that are only caught on exam mornings when time is short.
This project builds an automated database register and natural language query assistant that securely restricts users to their own schedules while checking that rooms aren't overloaded and invigilators aren't double-assigned.

---

## How to Run the Project Step-by-Step

This project supports a **Standalone Web App (No Install Required)**, a **Terminal CLI**, and a **Streamlit Dashboard**.

### Option A: Standalone Web App (Recommended — Zero Prerequisites)
Simply double-click the [index.html](file:///c:/Users/lenovo/Desktop/exam_seating_system/index.html) file inside the project directory to open it in any modern browser (Chrome, Edge, Safari, Firefox). 
- Runs 100% client-side.
- Zero installation or command-line setup required.
- High-performance animations and glassmorphic UI.

---

### Option B: Terminal CLI
1. Open your terminal in the project directory.
2. Execute:
   ```bash
   python scripts/assistant_cli.py
   ```

---

### Option C: Streamlit Web Dashboard
1. Install Streamlit in your Python environment:
   ```bash
   pip install streamlit
   ```
2. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## Technical Setup & Script Executions

### 1. Regenerate Sample Data (Optional)
If you wish to programmatically regenerate the CSV dataset, run:
```bash
python scripts/generate_data.py
```
This updates the dataset at `data/seating_duty_records.csv`. To sync it with the HTML App, compile the JS data file:
```bash
# This converts the CSV back to js/data.js
python -c "import csv, json, os; f_in = open('data/seating_duty_records.csv', 'r', encoding='utf-8'); r = list(csv.DictReader(f_in)); f_in.close(); os.makedirs('js', exist_ok=True); f_out = open('js/data.js', 'w', encoding='utf-8'); f_out.write('const examRecords = '); json.dump(r, f_out, indent=2); f_out.write(';\n'); f_out.close()"
```

### 2. Run the Automated Test Suite
To run the automated validation test cases (verifying user isolation, misspellings, short/empty queries, out-of-scope queries, and edge cases) and compile a test transcript, execute:
```bash
python scripts/run_tests.py
```
This generates the transcript at `data/test_transcripts.md`.

---

## Data Schema & Field Definitions

The register reads from `data/seating_duty_records.csv`. Below is what each field represents:

*   **`record_id`**: Alphanumeric unique identifier for each seating and duty pairing (e.g., `REC001` to `REC100`).
*   **`exam_date`**: The date of the exam, in `YYYY-MM-DD` format.
*   **`session`**: The block of the day the exam takes place (`Morning` or `Afternoon`).
*   **`hall`**: The room where the exam is held (`Hall A`, `Hall B`, `Hall C`, `Gymnasium`, plus outlier `Storage Room C`).
*   **`seat_no`**: The specific seat code assigned to the student (e.g., `A-12`, `B-05`, or empty `""` for unassigned).
*   **`student_id`**: The student ID (e.g., `STU101` to `STU120`, plus outlier `STU999`).
*   **`subject`**: The exam subject course (e.g., `Mathematics`, `Computer Science`, `Physics`, `Chemistry`, `Biology`, plus outlier `Astrology`).
*   **`invigilator`**: The academic supervisor's full name (e.g., `Dr. Ashwini Sekar`, `Dr. Ashwani Sekar`, or empty `""` for unassigned).
*   **`student_attendance`** *(Outcome)*: The outcome status indicating whether the student was `Present` or `Absent`.

---

## How Derived Figures are Calculated

### 1. Attendance Outcome (`student_attendance`)
The attendance status is a derived outcome calculated using statistical rules to make it learnable for prediction models:
- **Base Attendance**: Every student starts with a `95%` probability of being `Present`.
- **Student Factor**:
  - `STU105` is chronic: base probability drops to `35%`.
  - `STU108` is chronic: base probability drops to `50%`.
- **Session Factor**: Morning slots (`Morning`) suffer a `5%` drop in attendance probability (oversleeping, commute delays).
- **Subject Factor**:
  - `Physics` exams drop attendance probability by `10%`.
  - `Mathematics` exams drop attendance probability by `5%`.
- **Formula**:
  $$\text{Probability} = \text{Base} - \text{Student\_Factor} - \text{Session\_Factor} - \text{Subject\_Factor}$$
  The script then generates a random value between 0 and 1; if it is less than the calculated Probability, the status is set to `Present`, otherwise `Absent`.

### 2. Seat Letter Code
The prefix of the `seat_no` is automatically derived from the last word of the `hall` name (e.g. `Hall A` maps to `A-` seat prefix; `Gymnasium` maps to `G-`).

---

## What is Not Finished / Next Steps

1. **Auto-Allocation Algorithm**: Currently, the dataset is programmatically pre-generated. The next task would involve building the constraint solver (using back-tracking or linear programming) to automatically schedule students and staff while actively avoiding hall over-allocations and invigilator double-bookings.
2. **Machine Learning Model Integration**: In the next phase, we will train a Scikit-Learn classifier on the historical `student_attendance` outcomes to predict the attendance status of future seating schedules.
3. **Database backend integration**: Moving the data layer from static CSV files to a database like SQLite or MongoDB Compass (which is installed on the user's desktop) for production concurrency.
