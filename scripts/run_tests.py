import sys
import os

# Include current directory in search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant_engine import ExamAssistantEngine

def run_test_suite():
    engine = ExamAssistantEngine()
    transcript_lines = []
    
    def log(text):
        print(text)
        transcript_lines.append(text)

    log("# Test Transcript - Exam Seating & Duty Query Assistant")
    log("This file contains the complete test run transcript, showing the evaluation of natural language intent matching, user identity isolation, spelling tolerance, and awkward/edge case handling.\n")

    # 1. Identity Verification Tests
    log("## Scenario 1: Identity Verification & Suggestions")
    
    # Valid Student
    role, name = engine.identify_user("STU105")
    log(f"Input: 'STU105' | Authenticated Role: {role} | Authenticated Identity: {name}")
    
    # Valid Invigilator
    role, name = engine.identify_user("Dr. Ashwini Sekar")
    log(f"Input: 'Dr. Ashwini Sekar' | Authenticated Role: {role} | Authenticated Identity: {name}")
    
    # Similar name (should NOT match)
    role, name = engine.identify_user("Dr. Ashwani Sekar")
    log(f"Input: 'Dr. Ashwani Sekar' | Authenticated Role: {role} | Authenticated Identity: {name}")
    
    # Unknown user with suggestions
    invalid_input = "Dr. Ashwini Sakar"
    role, name = engine.identify_user(invalid_input)
    log(f"Input: '{invalid_input}' | Authenticated Role: {role}")
    if not name:
        suggestions = engine.get_similar_identities(invalid_input)
        log(f"Suggestions: {suggestions}\n")

    # 2. Phrasings Tests (Student STU105)
    log("## Scenario 2: Testing Phrasings for Student 'STU105'")
    student_id = "STU105"
    
    # Normal query
    q1 = "Where is my seat?"
    success, ans = engine.answer_query("Student", student_id, q1)
    log(f"Question: '{q1}' (Normal)\nMatched: {success}\nResponse:\n{ans}\n")
    
    # Misspelling
    q2 = "where is mi seet"
    success, ans = engine.answer_query("Student", student_id, q2)
    log(f"Question: '{q2}' (Misspelling)\nMatched: {success}\nResponse:\n{ans}\n")
    
    # Very short
    q3 = "seat"
    success, ans = engine.answer_query("Student", student_id, q3)
    log(f"Question: '{q3}' (Very Short)\nMatched: {success}\nResponse:\n{ans}\n")
    
    # Empty message
    q4 = ""
    success, ans = engine.answer_query("Student", student_id, q4)
    log(f"Question: '{q4}' (Empty)\nMatched: {success}\nResponse:\n{ans}\n")
    
    # Out of scope
    q5 = "what is the weather today?"
    success, ans = engine.answer_query("Student", student_id, q5)
    log(f"Question: '{q5}' (Out of Scope)\nMatched: {success}\nResponse:\n{ans}\n")

    # 3. Asker Isolation Tests
    log("## Scenario 3: Asker Records Isolation (Task 3 & 5)")
    stu_a = "STU105"
    stu_b = "STU112"
    q_common = "Where is my seat?"
    
    log(f"Querying as Student '{stu_a}':")
    _, ans_a = engine.answer_query("Student", stu_a, q_common)
    log(f"Response: {ans_a}\n")
    
    log(f"Querying as Student '{stu_b}':")
    _, ans_b = engine.answer_query("Student", stu_b, q_common)
    log(f"Response: {ans_b}\n")
    
    # Assert isolation
    assert ans_a != ans_b, "Error: User isolation failed!"
    log("Isolation Check: SUCCESS. Students receive only their own records.\n")

    # 4. Awkward / Edge Cases
    log("## Scenario 4: Awkward Cases Resolution (Task 1 & 5)")
    
    # 4.1 Missing Invigilator (REC098 for STU112)
    q_inv = "who is my invigilator"
    success, ans = engine.answer_query("Student", "STU112", q_inv)
    log(f"User: STU112 (REC098 - Missing Invigilator) | Question: '{q_inv}'\nResponse: {ans}\n")
    
    # 4.2 Missing Seat Number (REC099 for STU114)
    q_seat = "where is my seat"
    success, ans = engine.answer_query("Student", "STU114", q_seat)
    log(f"User: STU114 (REC099 - Missing Seat No) | Question: '{q_seat}'\nResponse: {ans}\n")
    
    # 4.3 Isolated/Orphan Record (REC100 for STU999)
    success, ans = engine.answer_query("Student", "STU999", q_seat)
    log(f"User: STU999 (REC100 - Orphan Christmas Student) | Question: '{q_seat}'\nResponse: {ans}\n")
    
    # 4.4 Isolated Invigilator (REC100 for Dr. Orphan)
    q_duty = "where is my duty"
    success, ans = engine.answer_query("Invigilator", "Dr. Orphan", q_duty)
    log(f"User: Dr. Orphan (REC100 - Orphan Christmas Invigilator) | Question: '{q_duty}'\nResponse: {ans}\n")

    # Write transcript to markdown file
    output_path = r"C:\Users\lenovo\Desktop\exam_seating_system\data\test_transcripts.md"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(transcript_lines))
    log(f"Successfully wrote test transcript to {output_path}")

if __name__ == "__main__":
    run_test_suite()
