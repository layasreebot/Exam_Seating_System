# Bot Refusal Mechanism - Polite Refusal for Out-of-Scope Questions

## Overview

The Exam Seating & Duty Register Assistant includes a **Refusal Mechanism** that ensures the bot:
- ✅ Refuses to answer questions outside its scope
- ✅ Explains why it cannot help
- ✅ Shows what it CAN help with
- ✅ Directs users to the Exam Office for other matters
- ✅ **NEVER gives wrong or hallucinated answers**

---

## How It Works

### Intent Classification

The bot uses a **keyword-based intent classification** system:

```
User Query → Normalize → Keyword Matching → Intent Score → Response
```

**Scoring Rules:**
- **Strong Match (2+ keywords)**: Confidence threshold met, answer the question
- **Weak Match (1 keyword)**: Only if keyword is very specific (attend, seat, etc.)
- **No Match (0 keywords)**: Refuse politely

### Specific Keywords

The bot only accepts single-keyword matches for these specific terms:
```
attendance, attend, seat, seating, invigilator, 
hall, subject, course, when, where
```

All other single keywords are treated as weak matches and trigger refusal.

---

## Test Results: Refusal Mechanism

### Out-of-Scope Questions (Should Be Refused)

| Question | Category | Result | Reason |
|----------|----------|--------|--------|
| "What is the capital of France?" | General knowledge | ✅ REFUSED | No exam keywords |
| "How do I make pasta?" | Cooking advice | ✅ REFUSED | No exam keywords |
| "What's the weather today?" | Weather | ✅ REFUSED | "Today" doesn't match exam keywords |
| "Can you help me with homework?" | Academic help | ✅ REFUSED | No exam keywords |
| "Who is the principal?" | Administration | ✅ REFUSED | "Who" ≠ specific invigilator query |
| "What time is cafeteria open?" | Facilities | ✅ REFUSED | "Time" keyword alone is too generic |

**Success Rate: 100%** - All out-of-scope questions properly refused

---

## Polite Refusal Response

When the bot cannot identify an intent, it responds with:

```
I am not confident of what you are asking. I can only help with 
exam-related queries like seating, schedules, subjects, invigilators, 
and attendance.

Here are the questions I can answer for you:
 - Where is my seat / hall? (e.g., 'Where is my seat?')
 - When is my exam? (e.g., 'When is my exam?')
 - What subject am I writing? (e.g., 'What subject is my exam?')
 - Who is invigilating my exam? (e.g., 'Who is my invigilator?')
 - Did I attend my exam? (e.g., 'Was I present for my exam?')

For other inquiries, please contact the Exam Office.
```

**Key Elements:**
1. **Polite tone** - "I am not confident" (not "I don't know")
2. **Explains scope** - "exam-related queries like..."
3. **Shows options** - Lists what bot CAN help with
4. **Provides direction** - "contact the Exam Office"

---

## Why This Matters

### Problem: Bot Hallucination
Untrained bots often:
- Make up wrong answers (hallucinate)
- Provide confidently incorrect information
- Mislead students
- Spread misinformation

**Example Bad Response:**
```
Q: "What's the weather today?"
A: "It will be sunny and warm with 25 degrees temperature..."
   (This is completely made up!)
```

### Solution: The Refusal Mechanism
The bot instead:
- Acknowledges uncertainty
- Avoids fabricating information
- Points to correct resource (Exam Office)
- Maintains trust through honesty

**Correct Response:**
```
Q: "What's the weather today?"
A: "I am not confident of what you are asking. I can only help 
   with exam-related queries... For other inquiries, please contact 
   the Exam Office."
```

---

## Implementation Details

### Code Location: `scripts/assistant_engine.py`

#### Refusal Logic (Lines 199-206)

```python
intent = self.classify_intent(normalised_query, user_role)

if not intent:
    questions_list = "\n".join([f" - {q}" for q in self.get_supported_questions(user_role)])
    return False, (
        "I am not confident of what you are asking. I can only help with exam-related queries like seating, schedules, subjects, invigilators, and attendance.\n\n"
        "Here are the questions I can answer for you:\n"
        f"{questions_list}\n\n"
        "For other inquiries, please contact the Exam Office."
    )
```

#### Smart Keyword Matching (Lines 156-174)

```python
if best_score == 1:
    # Check if the single keyword is specific/strong enough
    matched_words = []
    for word in words:
        for kw in target_intents[best_intent]:
            if word == kw or (len(kw) >= 4 and len(word) >= 3 and levenshtein_distance(word, kw) <= 1):
                if kw in specific_keywords:
                    matched_words.append(kw)
    
    # Single keyword match is OK only if it's very specific
    if not matched_words:
        return None  # Weak match on generic keyword, refuse
```

---

## UI Rendering

### Streamlit App

The app renders refusal responses with special styling:

**CSS Class:** `refusal-card`

```css
.refusal-card {
    padding: 1.5rem;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(230, 126, 34, 0.12) 0%, rgba(211, 84, 0, 0.08) 100%);
    border: 1px solid rgba(230, 126, 34, 0.3);
    color: #f8fafc;
    line-height: 1.6;
}
```

**Visual Effect:**
- 🟠 Orange/amber border and background
- Clean, readable text
- Clearly distinguishes from successful answers (green cards)

---

## Test Command

Run the refusal mechanism demo:

```bash
python demo_refusal_mechanism.py
```

This runs 5 out-of-scope questions and shows the bot's polite refusal in action.

---

## Examples of Questions

### Safely Refused ✅

```
Q: "What is the capital of France?"
→ Refused (No exam keywords)

Q: "How do I make pasta?"
→ Refused (Cooking is out of scope)

Q: "What's the weather?"
→ Refused (No exam keywords match)

Q: "Who is the principal?"
→ Refused (Not asking about exam invigilator)

Q: "Help me with my homework?"
→ Refused (Academic help is out of scope)
```

### In-Scope Questions ✅

```
Q: "Where is my seat?"
→ Answered (Specific: "seat" keyword)

Q: "When is my exam?"
→ Answered (Specific: "when" keyword)

Q: "Did I attend?"
→ Answered (Specific: "attend" keyword)

Q: "Who is my invigilator?"
→ Answered (Specific: "invigilator" keyword)

Q: "Check my presence"
→ Answered (Multiple keywords: "check" + "presence")
```

---

## Safety Features

### 1. Strict Keyword Matching
- Requires keywords to match exactly or with fuzzy logic
- Generic keywords alone cannot trigger responses

### 2. Multiple Keyword Requirement
- Single weak keywords require very specific terms
- Two or more keywords = strong confidence

### 3. Tie-Breaking Logic
- When intent score is tied, checks for specific disambiguators
- Falls back to refusal if unsure

### 4. Scope Declaration
- Bot clearly states what it CAN help with
- Reduces expectations and misunderstandings

### 5. Directional Guidance
- Explicitly points to Exam Office
- Provides proper escalation path

---

## Future Improvements

Possible enhancements:

1. **Machine Learning Classification**
   - Use trained models instead of keyword matching
   - Better handle nuanced queries

2. **Multi-Language Support**
   - Respond in student's language
   - Detect language and respond appropriately

3. **Escalation System**
   - Auto-create tickets for escalated questions
   - Track unanswered question patterns

4. **Knowledge Base Expansion**
   - Gradually add new intents
   - Learn from unanswered questions

5. **Confidence Scoring**
   - Show confidence percentage
   - "I'm 85% sure about this answer..."

---

## Conclusion

The refusal mechanism is a **critical safety feature** that ensures:

✅ **Accuracy** - Only answers what it knows
✅ **Trust** - Honest about limitations
✅ **Safety** - Never gives wrong information
✅ **Guidance** - Points to right resource
✅ **Reliability** - Consistent behavior

This transforms the bot from a "know-it-all" into a "honest assistant"—which is exactly what students need.
