#!/usr/bin/env python3
"""Debug the attendance query issue"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from assistant_engine import normalise_text, ExamAssistantEngine

query = "Did I attend my exam?"
normalised = normalise_text(query)
print(f"Original: {query}")
print(f"Normalised: {normalised}")
words = normalised.split()
print(f"Words: {words}")
print(f"'attend' in words: {'attend' in words}")

engine = ExamAssistantEngine(
    csv_path=r"C:\Users\lenovo\Desktop\exam_seating_system\data\seating_duty_records.csv"
)

intent = engine.classify_intent(normalised, "Student")
print(f"Intent: {intent}")

# Test with simpler queries
simple_queries = [
    "attend?",
    "did attend?",
    "i attend",
    "did i attend",
    "attend my exam"
]

for q in simple_queries:
    normalised = normalise_text(q)
    intent = engine.classify_intent(normalised, "Student")
    print(f"'{q}' -> '{normalised}' -> {intent}")

# Test the full query
print("\nFull response:")
student_id = "STU101"
role, matched_id = engine.identify_user(student_id)
success, response = engine.answer_query(role, matched_id, query)
print(f"Success: {success}")
print(f"Response: {response}")
