# Test Transcript - Exam Seating & Duty Query Assistant
This file contains the complete test run transcript, showing the evaluation of natural language intent matching, user identity isolation, spelling tolerance, and awkward/edge case handling.

## Scenario 1: Identity Verification & Suggestions
Input: 'STU105' | Authenticated Role: Student | Authenticated Identity: STU105
Input: 'Dr. Ashwini Sekar' | Authenticated Role: Invigilator | Authenticated Identity: Dr. Ashwini Sekar
Input: 'Dr. Ashwani Sekar' | Authenticated Role: Invigilator | Authenticated Identity: Dr. Ashwani Sekar
Input: 'Dr. Ashwini Sakar' | Authenticated Role: None
Suggestions: ['Invigilator: Dr. Ashwani Sekar', 'Invigilator: Dr. Ashwini Sekar']

## Scenario 2: Testing Phrasings for Student 'STU105'
Question: 'Where is my seat?' (Normal)
Matched: True
Response:
Exam 1: Your seat number is 'C-07' in 'Hall C' for the 'Physics' exam.
Exam 2: Your seat number is 'B-13' in 'Hall B' for the 'Mathematics' exam.
Exam 3: Your seat number is 'A-28' in 'Hall A' for the 'Chemistry' exam.

Question: 'where is mi seet' (Misspelling)
Matched: True
Response:
Exam 1: Your seat number is 'C-07' in 'Hall C' for the 'Physics' exam.
Exam 2: Your seat number is 'B-13' in 'Hall B' for the 'Mathematics' exam.
Exam 3: Your seat number is 'A-28' in 'Hall A' for the 'Chemistry' exam.

Question: 'seat' (Very Short)
Matched: True
Response:
Exam 1: Your seat number is 'C-07' in 'Hall C' for the 'Physics' exam.
Exam 2: Your seat number is 'B-13' in 'Hall B' for the 'Mathematics' exam.
Exam 3: Your seat number is 'A-28' in 'Hall A' for the 'Chemistry' exam.

Question: '' (Empty)
Matched: False
Response:
I cannot answer an empty message. Please ask a valid question.
Here are the questions I can answer for you:
 - Where is my seat / hall? (e.g., 'Where is my seat?')
 - When is my exam? (e.g., 'When is my exam?')
 - What subject am I writing? (e.g., 'What subject is my exam?')
 - Who is invigilating my exam? (e.g., 'Who is my invigilator?')

Question: 'what is the weather today?' (Out of Scope)
Matched: False
Response:
I am not confident of what you are asking. Please rephrase your question.
Here are the questions I can answer for you:
 - Where is my seat / hall? (e.g., 'Where is my seat?')
 - When is my exam? (e.g., 'When is my exam?')
 - What subject am I writing? (e.g., 'What subject is my exam?')
 - Who is invigilating my exam? (e.g., 'Who is my invigilator?')

## Scenario 3: Asker Records Isolation (Task 3 & 5)
Querying as Student 'STU105':
Response: Exam 1: Your seat number is 'C-07' in 'Hall C' for the 'Physics' exam.
Exam 2: Your seat number is 'B-13' in 'Hall B' for the 'Mathematics' exam.
Exam 3: Your seat number is 'A-28' in 'Hall A' for the 'Chemistry' exam.

Querying as Student 'STU112':
Response: Exam 1: Your seat number is 'B-10' in 'Hall B' for the 'Computer Science' exam.
Exam 2: Your seat number is 'A-15' in 'Hall A' for the 'Chemistry' exam.

Isolation Check: SUCCESS. Students receive only their own records.

## Scenario 4: Awkward Cases Resolution (Task 1 & 5)
User: STU112 (REC098 - Missing Invigilator) | Question: 'who is my invigilator'
Response: Exam 1: The invigilator for your 'Computer Science' exam is 'Dr. Jane Doe'.
Exam 2: The invigilator for your 'Chemistry' exam is '[Not Assigned Yet]'.

User: STU114 (REC099 - Missing Seat No) | Question: 'where is my seat'
Response: Exam 1: Your seat number is 'B-35' in 'Hall B' for the 'Computer Science' exam.
Exam 2: Your seat number is 'A-39' in 'Hall A' for the 'Physics' exam.
Exam 3: Your seat number is '[Not Assigned Yet]' in 'Hall B' for the 'Biology' exam.

User: STU999 (REC100 - Orphan Christmas Student) | Question: 'where is my seat'
Response: Exam 1: Your seat number is 'Z-99' in 'Storage Room C' for the 'Astrology' exam.

User: Dr. Orphan (REC100 - Orphan Christmas Invigilator) | Question: 'where is my duty'
Response: Duty 1: You are supervising in 'Storage Room C' for the 'Astrology' exam (Session: Morning).
