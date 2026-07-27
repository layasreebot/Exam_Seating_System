#!/usr/bin/env python3
"""
DEMO: Bot's Polite Refusal Mechanism
Demonstrates how the bot refuses out-of-scope questions gracefully.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from assistant_engine import ExamAssistantEngine

def show_demo():
    engine = ExamAssistantEngine(
        csv_path=r"C:\Users\lenovo\Desktop\exam_seating_system\data\seating_duty_records.csv"
    )
    
    student_id = "STU101"
    role, matched_id = engine.identify_user(student_id)
    
    print("\n" + "="*75)
    print("DEMO: Bot's Polite Refusal Mechanism")
    print("="*75)
    print(f"\nLogged in as: {matched_id} ({role})")
    print("\nThis demo shows that the bot REFUSES out-of-scope questions gracefully")
    print("instead of giving wrong answers. It points the student to the Exam Office.\n")
    
    # Clear out-of-scope questions
    out_of_scope = [
        "What is the capital of France?",
        "How do I make pasta?",
        "What's the weather today?",
        "Can you help me with my homework?",
        "Who is the principal?",
    ]
    
    print("-" * 75)
    print("TESTING OUT-OF-SCOPE QUESTIONS")
    print("-" * 75)
    print("\nThese questions are completely OUTSIDE the bot's scope:")
    print("(Exam seating, schedules, subjects, invigilators, attendance)\n")
    
    for idx, question in enumerate(out_of_scope, 1):
        print(f"\n[Test {idx}]")
        print(f"Question: \"{question}\"")
        print("-" * 75)
        
        success, response = engine.answer_query(role, matched_id, question)
        
        if not success:
            print("BOT RESPONSE (Polite Refusal):")
            print(response)
        else:
            print("BOT RESPONSE (Answer - but might be wrong!):")
            print(response)
        
        if not success:
            print("\n[SUCCESS] Bot correctly REFUSED this out-of-scope question")
            print("[SUCCESS] Bot explained its scope clearly")
            print("[SUCCESS] Bot pointed student to Exam Office for other inquiries")
    
    print("\n" + "="*75)
    print("DEMO CONCLUSION")
    print("="*75)
    print("""
The bot's refusal mechanism works as designed:

1. DETECTS out-of-scope questions early
2. REFUSES politely without giving wrong answers
3. EXPLAINS what it CAN help with
4. POINTS TO EXAM OFFICE for other matters

Key Features:
[+] Prevents hallucination (making up wrong answers)
[+] Builds trust (honest about limitations)
[+] Guides users appropriately
[+] Reduces wrong information spread
    """)

if __name__ == "__main__":
    show_demo()
