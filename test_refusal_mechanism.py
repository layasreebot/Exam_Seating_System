#!/usr/bin/env python3
"""
Test the bot's polite refusal mechanism for out-of-scope questions.
Demonstrates that the bot refuses gracefully instead of giving wrong answers.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from assistant_engine import ExamAssistantEngine

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"[{title}]")
    print("="*70)

def test_refusal():
    """Test the bot's refusal mechanism with out-of-scope questions."""
    
    engine = ExamAssistantEngine(
        csv_path=r"C:\Users\lenovo\Desktop\exam_seating_system\data\seating_duty_records.csv"
    )
    
    student_id = "STU101"
    role, matched_id = engine.identify_user(student_id)
    
    print_section("BOT REFUSAL MECHANISM TEST")
    print(f"\nLogged in as: {matched_id} ({role})")
    print("\nTesting out-of-scope questions that should trigger polite refusal...")
    
    # Define out-of-scope questions
    out_of_scope_questions = [
        ("What is the capital of France?", "General knowledge"),
        ("How do I make pasta?", "Cooking advice"),
        ("What's the weather today?", "Weather query"),
        ("Can you help me with my homework?", "Academic help"),
        ("What time is the cafeteria open?", "Cafeteria info"),
        ("Do you speak Spanish?", "Language capability"),
        ("What's the meaning of life?", "Philosophical question"),
        ("How do I reset my password?", "IT support"),
        ("When are my classes?", "Class schedule (not exam schedule)"),
        ("Who is the principal?", "Administrative staff"),
    ]
    
    print_section("OUT-OF-SCOPE QUESTION TESTS")
    print("\nThese questions are OUTSIDE the bot's scope of exam-related queries.")
    print("The bot should refuse politely and point to the office.\n")
    
    results = {"refused": 0, "understood": 0}
    
    for idx, (question, category) in enumerate(out_of_scope_questions, 1):
        print(f"[Test {idx}] Category: {category}")
        print(f"  Q: {question}")
        
        success, response = engine.answer_query(role, matched_id, question)
        
        if not success:  # Bot refused (success=False)
            print(f"  Status: REFUSED (politely)")
            print(f"  Response: {response[:120]}..." if len(response) > 120 else f"  Response: {response}")
            results["refused"] += 1
        else:
            print(f"  Status: ANSWERED (might be wrong!)")
            print(f"  Response: {response[:120]}..." if len(response) > 120 else f"  Response: {response}")
            results["understood"] += 1
        
        print()
    
    # Show in-scope questions for comparison
    print_section("IN-SCOPE QUESTION TESTS (For Comparison)")
    print("\nThese questions ARE within the bot's scope.")
    print("The bot should answer them confidently.\n")
    
    in_scope_questions = [
        ("Where is my seat?", "Exam seating"),
        ("When is my exam?", "Exam schedule"),
        ("What subject am I writing?", "Exam subject"),
        ("Who is my invigilator?", "Invigilator info"),
        ("Did I attend my exam?", "Attendance status"),
    ]
    
    for idx, (question, category) in enumerate(in_scope_questions, 1):
        print(f"[Test {idx}] Category: {category}")
        print(f"  Q: {question}")
        
        success, response = engine.answer_query(role, matched_id, question)
        
        if success:
            print(f"  Status: ANSWERED (confidently)")
            print(f"  Response: {response.split(chr(10))[0]}..." if chr(10) in response else f"  Response: {response}")
            results["understood"] += 1
        else:
            print(f"  Status: REFUSED")
            print(f"  Response: {response[:120]}..." if len(response) > 120 else f"  Response: {response}")
            results["refused"] += 1
        
        print()
    
    print_section("TEST RESULTS SUMMARY")
    print(f"\nOut-of-Scope Questions: {len(out_of_scope_questions)}")
    print(f"  - Successfully Refused: {results['refused']} / {len(out_of_scope_questions)}")
    print(f"\nIn-Scope Questions: {len(in_scope_questions)}")
    print(f"  - Successfully Answered: {results['understood']} / {len(in_scope_questions)}")
    
    refusal_success_rate = (results["refused"] / len(out_of_scope_questions)) * 100
    answer_success_rate = (results["understood"] / len(in_scope_questions)) * 100
    
    print(f"\nRefusal Accuracy: {refusal_success_rate:.1f}%")
    print(f"Answer Accuracy: {answer_success_rate:.1f}%")
    
    if refusal_success_rate == 100 and answer_success_rate >= 80:
        print("\n[RESULT] EXCELLENT - Bot refuses out-of-scope questions and answers in-scope ones!")
    else:
        print("\n[RESULT] NEEDS IMPROVEMENT")

if __name__ == "__main__":
    test_refusal()
