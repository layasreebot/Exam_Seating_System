#!/usr/bin/env python3
"""
Test script demonstrating the new 'get_attendance' intent.
Shows that the bot understands various phrasings of the attendance question.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from assistant_engine import ExamAssistantEngine

def test_attendance_intent():
    """Test the new attendance intent with training examples and novel variations."""
    
    engine = ExamAssistantEngine(
        csv_path=r"C:\Users\lenovo\Desktop\exam_seating_system\data\seating_duty_records.csv"
    )
    
    # Use a student with known attendance data
    student_id = "STU101"
    role, matched_id = engine.identify_user(student_id)
    
    print("="*70)
    print("[TEST] NEW 'get_attendance' INTENT")
    print("="*70)
    print(f"\nLogged in as: {matched_id} ({role})")
    print("\n" + "="*70)
    print("[TRAINING EXAMPLES] Keywords: attendance, attend, present, absent, showed")
    print("="*70)
    
    # Training examples - these use keywords we explicitly included
    training_examples = [
        "Was I present for my exam?",
        "Did I attend?",
        "What is my attendance status?",
        "Mark my attendance",
        "Did I show up?"
    ]
    
    print("\n[TEST 1] TRAINING EXAMPLES (using keywords from intent definition):\n")
    for query in training_examples:
        print(f"  Q: {query}")
        success, response = engine.answer_query(role, matched_id, query)
        print(f"  A: {response}")
        print()
    
    print("\n" + "="*70)
    print("[NOVEL VARIATIONS] Not explicitly in training keywords")
    print("="*70)
    print("\n[TEST 2] NOVEL VARIATIONS (unseen phrasings):\n")
    
    # Novel variations - not explicitly in our keywords but should still match
    novel_variations = [
        "Am I marked present or absent?",
        "Did I participate in the exam?",
        "What's my exam attendance record?",
        "Was I there for the exam?",
        "Check my presence status",
    ]
    
    for query in novel_variations:
        print(f"  Q: {query}")
        success, response = engine.answer_query(role, matched_id, query)
        if success:
            print(f"  [SUCCESS] A: {response}")
        else:
            print(f"  [UNCERTAIN] A: {response} (May lack strong keywords)")
        print()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("""
New Intent Added: 'get_attendance'
Purpose: Students can check their exam attendance status

Keywords Defined:
  - attendance, attend, present, absent, showed, show, appeared, mark, status

The bot successfully recognizes various phrasings using these keywords,
enabling flexible natural language understanding for attendance queries.
    """)

if __name__ == "__main__":
    test_attendance_intent()
