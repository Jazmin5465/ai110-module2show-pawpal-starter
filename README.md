# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Owner: Alice
Availability: Available from 08:00 to 18:00

Pets: Buddy, Whiskers
  - Buddy is a 3-year-old Golden Retriever
  - Whiskers is a 2-year-old Tabby Cat


Schedule valid (fits in 600 min): True

DAILY SCHEDULE FOR ALICE
Available from 08:00 to 18:00
Available: 600 minutes

SCHEDULED TASKS:
  ○ 08:00  🐕 Buddy        - Morning walk           (30 min) [high]
  ○ 08:30  🐱 Whiskers     - Litter box cleaning    (15 min) [medium]
  ○ 09:00  🐱 Whiskers     - Cat feeding            (5 min) [high]
  ○ 09:00  🐕 Buddy        - Feeding                (10 min) [high]
  ○ 09:10  🐱 Whiskers     - Interactive play session (25 min) [medium]
  ○ 09:35  🐕 Buddy        - Grooming               (45 min) [low]
  ○ 14:00  🐕 Buddy        - Afternoon playtime     (20 min) [medium]

Scheduled: 150/600 minutes (25%)
Not scheduled: 0 minutes

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `generate_plan()` | Multi-factor: priority (high first) → duration (short first) → category (grouped) for efficient packing |
| Filtering | `generate_plan()` | Only includes tasks due today; skips non-daily/weekly tasks; removes tasks that exceed time budget |
| Conflict handling | Time slot detection in frontend | Detects and displays warning when 2+ tasks are scheduled at same time; shows affected pets and tasks |
| Recurring tasks | `mark_complete()` | Auto-creates next occurrence: daily tasks recur tomorrow, weekly tasks recur next week; maintains consistency |
| Break insertion | `generate_scheduled_plan()` | Automatically inserts 10-min breaks after every 2 tasks based on owner preferences (min_breaks) |
| Time slot assignment | `generate_scheduled_plan()` | Places pre-assigned tasks in fixed slots, then fills remaining gaps with untimed tasks using best-fit strategy |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
