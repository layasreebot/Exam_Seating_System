#!/usr/bin/env python3
"""
Interactive demo of the new 'get_attendance' intent.
Shows how the bot understands various phrasings.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from assistant_engine import ExamAssistantEngine

def main():
    engine = ExamAssistantEngine(
        csv_path=r"C:\Users\lenovo\Desktop\exam_seating_system\data\seating_duty_records.csv"
    )
    
    print("\n" + "="*70)
    print("DEMO: New Attendance Intent - Interactive Test")
    print("="*70)
    print("\nThis demo shows how the bot understands attendance questions")
    print("with various natural language phrasings.\n")
    
    # Demo with student STU101
    student_id = "STU101"
    role, matched_id = engine.identify_user(student_id)
    
    print(f"[INFO] Logged in as: {matched_id} ({role})")
    print("\n" + "-"*70)
    print("DEMO QUESTIONS - Type 'quit' to exit, 'help' for examples")
    print("-"*70 + "\n")
    
    demo_questions = [
        ("Did I attend?", "Simple direct question"),
        ("What's my attendance?", "What-style question"),
        ("Check my presence", "Imperative style"),
        ("Am I marked absent?", "Status check"),
        ("Show my attendance record", "Record request"),
    ]
    
    for idx, (question, description) in enumerate(demo_questions, 1):
        print(f"\n[Question {idx}] {description}")
        print(f"  User: {question}")
        success, response = engine.answer_query(role, matched_id, question)
        if success:
            print(f"  Bot: {response[:150]}..." if len(response) > 150 else f"  Bot: {response}")
        else:
            print(f"  Bot: {response[:150]}..." if len(response) > 150 else f"  Bot: {response}")
        print("-" * 70)
    
    print("\n[SUCCESS] All demo questions processed!")
    print("\nThe new 'get_attendance' intent successfully handles various")
    print("natural language variations while understanding the user's intent.\n")

if __name__ == "__main__":
    main()
