import csv
import random
from datetime import datetime, timedelta

def generate_dataset():
    # Set random seed for reproducibility
    random.seed(42)
    
    # Define student names mapping
    student_names = {
        "STU101": "Arun Kumar",
        "STU102": "Ashwin Raja",
        "STU103": "Bhalaji S",
        "STU104": "Divya Bharathi",
        "STU105": "Layasree S",  # Main test student
        "STU106": "Harish R",
        "STU107": "Kavitha M",
        "STU108": "Manoj Prabhakar",
        "STU109": "Naveen Kumar",
        "STU110": "Pooja Sri",
        "STU111": "Praveen Raj",
        "STU112": "Ramya Devi",
        "STU113": "Sanjay Kumar",
        "STU114": "Sneha S",
        "STU115": "Surya Prakash",
        "STU116": "Swetha R",
        "STU117": "Tharun Kumar",
        "STU118": "Vijay Anand",
        "STU119": "Yuvashree K",
        "STU120": "Zakir Hussain",
        "STU999": "Orphan Student"
    }
    
    students = list(student_names.keys())[:-1] # Exclude orphan
    subjects = ["Mathematics", "Computer Science", "Physics", "Chemistry", "Biology"]
    halls = ["Hall A", "Hall B", "Hall C", "Gymnasium"]
    sessions = ["Morning", "Afternoon"]
    
    # Invigilators (including very similar names as requested)
    invigilators = [
        "Dr. Ashwini",   # Standard
        "Dr. Ashwani",   # Similar name to Dr. Ashwini
        "Prof. Robert",    # Standard
        "Dr. Rupert",    # Similar name to Prof. Robert
        "Dr. Jane",
        "Prof. Charles"
    ]
    
    # Start date and date range (80 days)
    start_date = datetime(2026, 5, 1)
    
    records = []
    
    # Generate 97 normal records (we will append 3 specific awkward/outlier cases later to make exactly 100)
    for i in range(1, 98):
        record_id = f"REC{i:03d}"
        
        # Select date
        days_offset = random.randint(0, 80)
        exam_date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        
        session = random.choice(sessions)
        hall = random.choice(halls)
        
        # Seat number format: [Hall letter]-[number 1-40]
        hall_letter = hall.split()[-1] if "Hall" in hall else "G"
        seat_no = f"{hall_letter}-{random.randint(1, 40):02d}"
        
        student_id = random.choice(students)
        subject = random.choice(subjects)
        invigilator = random.choice(invigilators)
        
        # Determine attendance (outcome) based on features to make it learnable
        # Base probability is 95%
        prob = 0.95
        
        # Chronic absent students
        if student_id == "STU105":
            prob = 0.35  # High absence rate
        elif student_id == "STU108":
            prob = 0.50  # Moderate absence rate
            
        # Morning session makes students slightly more likely to be absent (oversleeping)
        if session == "Morning":
            prob -= 0.05
            
        # Difficult subjects lead to more absences
        if subject == "Physics":
            prob -= 0.10
        elif subject == "Mathematics":
            prob -= 0.05
            
        # Bound probability between 0 and 1
        prob = max(0.05, min(0.99, prob))
        
        attendance = "Present" if random.random() < prob else "Absent"
        
        records.append({
            "record_id": record_id,
            "exam_date": exam_date,
            "session": session,
            "hall": hall,
            "seat_no": seat_no,
            "student_id": student_id,
            "subject": subject,
            "invigilator": invigilator,
            "student_attendance": attendance
        })
        
    # Now, let's inject the awkward cases to bring the total to 100 records
    
    # 1. Record with a missing invigilator (Blank field)
    records.append({
        "record_id": "REC098",
        "exam_date": "2026-06-15",
        "session": "Morning",
        "hall": "Hall A",
        "seat_no": "A-15",
        "student_id": "STU112",
        "subject": "Chemistry",
        "invigilator": "",  # Missing invigilator
        "student_attendance": "Present"
    })
    
    # 2. Record with a missing seat number (Blank field)
    records.append({
        "record_id": "REC099",
        "exam_date": "2026-06-16",
        "session": "Afternoon",
        "hall": "Hall B",
        "seat_no": "",  # Missing seat number
        "student_id": "STU114",
        "subject": "Biology",
        "invigilator": "Dr. Jane Doe",
        "student_attendance": "Absent"
    })
    
    # 3. An isolated/orphan record with nothing related to the rest of the dataset
    records.append({
        "record_id": "REC100",
        "exam_date": "2026-12-25",  # Outlier date (Christmas)
        "session": "Morning",
        "hall": "Storage Room C",  # Unique/Orphan Hall
        "seat_no": "Z-99",  # Unique Seat
        "student_id": "STU999",  # Unique Student ID (does not exist in students list)
        "subject": "Astrology",  # Unique/Orphan Subject
        "invigilator": "Dr. Orphan",  # Unique/Orphan Invigilator
        "student_attendance": "Absent"
    })
    
    # Write to CSV
    import os
    output_path = "C:/Users/lenovo/Desktop/exam_seating_system/data/seating_duty_records.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Ensure headers match the requested columns plus student_attendance
    headers = [
        "record_id", "exam_date", "session", "hall", 
        "seat_no", "student_id", "subject", "invigilator", 
        "student_attendance"
    ]
    
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)
        
    print(f"Successfully generated {len(records)} records and saved to {output_path}")

if __name__ == "__main__":
    generate_dataset()
