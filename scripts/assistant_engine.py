import csv
import os
import string

def levenshtein_distance(s1, s2):
    """Calculate the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def normalise_text(text):
    """Trim whitespace, lowercase, and strip punctuation from a string."""
    if not text:
        return ""
    # Strip punctuation and lowercase
    text = text.strip().lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Remove extra spaces
    return " ".join(text.split())

class ExamAssistantEngine:
    def __init__(self, csv_path=None):
        if csv_path is None:
            csv_path = r"C:\Users\lenovo\Desktop\exam_seating_system\data\seating_duty_records.csv"
        self.csv_path = csv_path
        self.records = []
        self.load_data()
        
    def load_data(self):
        """Load records from the CSV file."""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Dataset file not found at {self.csv_path}")
            
        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.records = list(reader)

    def identify_user(self, identity_input):
        """
        Verify if the identity input matches a student or an invigilator.
        Returns: (role, exact_identity_name_or_id) or (None, None)
        """
        normalised_id = identity_input.strip()
        if not normalised_id:
            return None, None
            
        # Check if it looks like a student ID (STU...)
        # We perform case-insensitive lookup
        for r in self.records:
            if r["student_id"].strip().upper() == normalised_id.upper():
                return "Student", r["student_id"].strip()
                
        # Check if it is an invigilator name
        # We do case-insensitive exact matching
        invigilator_names = set(r["invigilator"].strip() for r in self.records if r["invigilator"].strip())
        for name in invigilator_names:
            if name.lower() == normalised_id.lower():
                return "Invigilator", name
                
        return None, None

    def get_similar_identities(self, identity_input):
        """If user identity is not found, suggest close matches from the dataset."""
        normalised_id = identity_input.strip().lower()
        if not normalised_id:
            return []
            
        suggestions = []
        
        # Collect all student IDs and invigilator names
        student_ids = set(r["student_id"].strip() for r in self.records if r["student_id"].strip())
        invigilator_names = set(r["invigilator"].strip() for r in self.records if r["invigilator"].strip())
        
        # Check student IDs
        for s_id in student_ids:
            if normalised_id in s_id.lower() or levenshtein_distance(normalised_id, s_id.lower()) <= 2:
                suggestions.append(f"Student ID: {s_id}")
                
        # Check invigilators
        for name in invigilator_names:
            if normalised_id in name.lower() or levenshtein_distance(normalised_id, name.lower()) <= 3:
                suggestions.append(f"Invigilator: {name}")
                
        return sorted(list(set(suggestions)))[:5]

    def match_word_to_keywords(self, word, target_keywords):
        """Check if a word matches any target keyword (allowing 1 char misspelling for long words)."""
        for kw in target_keywords:
            if word == kw:
                return True
            # Allow 1 typo for words of length >= 4
            if len(kw) >= 4 and len(word) >= 3:
                if levenshtein_distance(word, kw) <= 1:
                    return True
        return False

    def classify_intent(self, normalised_query, role):
        """
        Classifies the intent based on normalised query words and user role.
        Returns: intent_name (string) or None if unsure.
        """
        words = normalised_query.split()
        if not words:
            return None
            
        # Define keywords for intents
        student_intents = {
            "get_seat_and_hall": ["seat", "seating", "sit", "places", "chair", "number", "hall", "room", "classroom", "where", "location", "go"],
            "get_exam_schedule": ["when", "date", "time", "schedule", "day", "calendar", "session", "morning", "afternoon", "hour"],
            "get_exam_subject": ["subject", "course", "exam", "test", "class", "write", "writing", "registered"],
            "get_invigilator": ["invigilator", "teacher", "supervisor", "who", "staff", "monitoring", "supervising"]
        }
        
        invigilator_intents = {
            "get_duty_schedule": ["when", "date", "time", "schedule", "day", "calendar", "session", "shift", "duties", "duty", "invigilate", "supervise"],
            "get_duty_hall": ["where", "hall", "room", "classroom", "location", "place", "assigned", "supervising", "subject", "topic"]
        }
        
        target_intents = student_intents if role == "Student" else invigilator_intents
        
        # Calculate match scores for each intent
        intent_scores = {}
        for intent, keywords in target_intents.items():
            score = 0
            for word in words:
                if self.match_word_to_keywords(word, keywords):
                    score += 1
            if score > 0:
                intent_scores[intent] = score
                
        if not intent_scores:
            return None
            
        # Find the best matching intent
        sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
        best_intent, best_score = sorted_intents[0]
        
        # If there's a tie, let's check if the difference is clear or if we are unsure
        if len(sorted_intents) > 1 and sorted_intents[1][1] == best_score:
            # Tie case: if the query contains very strong indicators for one specific intent, prioritize
            # e.g., "where" vs "when"
            if role == "Student":
                if "where" in words or "seat" in words:
                    return "get_seat_and_hall"
                if "when" in words or "date" in words:
                    return "get_exam_schedule"
            else:
                if "where" in words or "hall" in words:
                    return "get_duty_hall"
                if "when" in words or "date" in words:
                    return "get_duty_schedule"
            return None  # Tie and cannot resolve confidently
            
        return best_intent

    def get_supported_questions(self, role):
        """Return a list of questions that the user's role can ask."""
        if role == "Student":
            return [
                "Where is my seat / hall? (e.g., 'Where is my seat?')",
                "When is my exam? (e.g., 'When is my exam?')",
                "What subject am I writing? (e.g., 'What subject is my exam?')",
                "Who is invigilating my exam? (e.g., 'Who is my invigilator?')"
            ]
        else:
            return [
                "When is my invigilation duty? (e.g., 'When is my duty?')",
                "Which hall am I invigilating? (e.g., 'Which hall am am I supervising?')"
            ]

    def answer_query(self, user_role, user_id_name, query):
        """
        Verify, normalise, classify intent, and retrieve the record answers.
        Returns: (success_boolean, answer_text)
        """
        normalised_query = normalise_text(query)
        
        if not normalised_query:
            questions_list = "\n".join([f" - {q}" for q in self.get_supported_questions(user_role)])
            return False, (
                "I cannot answer an empty message. Please ask a valid question.\n"
                f"Here are the questions I can answer for you:\n{questions_list}"
            )
            
        intent = self.classify_intent(normalised_query, user_role)
        
        if not intent:
            questions_list = "\n".join([f" - {q}" for q in self.get_supported_questions(user_role)])
            return False, (
                "I am not confident of what you are asking. Please rephrase your question.\n"
                f"Here are the questions I can answer for you:\n{questions_list}"
            )
            
        # Fetch only the records belonging to the logged-in user
        user_records = []
        for r in self.records:
            if user_role == "Student" and r["student_id"].strip() == user_id_name:
                user_records.append(r)
            elif user_role == "Invigilator" and r["invigilator"].strip() == user_id_name:
                user_records.append(r)
                
        if not user_records:
            return True, f"No records found in the database for {user_role} '{user_id_name}'."
            
        # Format answer based on intent
        answers = []
        for idx, r in enumerate(user_records, 1):
            # Safe values for awkward cases (missing fields)
            hall = r["hall"] if r["hall"] else "[Unknown/Unassigned Hall]"
            seat_no = r["seat_no"] if r["seat_no"] else "[Not Assigned Yet]"
            subject = r["subject"] if r["subject"] else "[Unknown Subject]"
            exam_date = r["exam_date"] if r["exam_date"] else "[TBD]"
            session = r["session"] if r["session"] else "[TBD]"
            invigilator = r["invigilator"] if r["invigilator"] else "[Not Assigned Yet]"
            attendance = r["student_attendance"] if r["student_attendance"] else "[Unknown]"
            
            # Format answers
            if intent == "get_seat_and_hall":
                answers.append(
                    f"Exam {idx}: Your seat number is '{seat_no}' in '{hall}' for the '{subject}' exam."
                )
            elif intent == "get_exam_schedule":
                answers.append(
                    f"Exam {idx}: Your '{subject}' exam is scheduled on '{exam_date}' in the '{session}' session."
                )
            elif intent == "get_exam_subject":
                answers.append(
                    f"Exam {idx}: You have a '{subject}' exam scheduled."
                )
            elif intent == "get_invigilator":
                answers.append(
                    f"Exam {idx}: The invigilator for your '{subject}' exam is '{invigilator}'."
                )
            elif intent == "get_duty_schedule":
                answers.append(
                    f"Duty {idx}: You are scheduled for invigilation duty on '{exam_date}' during the '{session}' session."
                )
            elif intent == "get_duty_hall":
                answers.append(
                    f"Duty {idx}: You are supervising in '{hall}' for the '{subject}' exam (Session: {session})."
                )
                
        return True, "\n".join(answers)
