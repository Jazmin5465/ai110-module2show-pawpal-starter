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
python -m pytest

```

The tests cover core scheduling behaviors including task completion toggling, multi-factor sorting correctness (priority → duration → category), recurring task auto-creation for daily/weekly frequencies, time-conflict detection, and edge cases like one-time tasks that don't recur.

Sample test output:

```
================================= test session starts ==================================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\jazmi\OneDrive\Codepath\Proj 2\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 13 items                                                                      

tests\test_pawpal.py .............                                                [100%]

================================== 13 passed in 0.11s ==================================
```

confidence level: 5 stars!

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `generate_plan()` | Multi-factor: priority (high first) → duration (short first) → category (grouped) for efficient packing |
| Filtering | `generate_plan()` | Only includes tasks due today; skips non-daily/weekly tasks; removes tasks that exceed time budget |
| Conflict handling | Time slot detection in frontend | Detects and displays warning when 2+ tasks are scheduled at same time; shows affected pets and tasks |
| Recurring tasks | `mark_complete()` | Auto-creates next occurrence: daily tasks recur tomorrow, weekly tasks recur next week; maintains consistency |
| Break insertion | `generate_scheduled_plan()` | Automatically inserts 10-min breaks after every 2 tasks based on owner preferences (min_breaks) |
| Time slot assignment | `generate_scheduled_plan()` | Places pre-assigned tasks in fixed slots, then fills remaining gaps with untimed tasks using best-fit strategy |

## ✨ Features

- **Multi-factor task sorting**: Prioritizes by importance (high → medium → low), then by duration (short first) to pack the schedule efficiently
- **Time-based filtering**: Shows only tasks due today; excludes future/past tasks and non-daily/weekly frequencies from daily schedules
- **Capacity-aware scheduling**: Respects owner's available time and skips lower-priority tasks when time budget is exceeded
- **Chronological time slot assignment**: Auto-assigns times to tasks, respecting pre-assigned slots and filling gaps with untimed tasks
- **Conflict detection & warnings**: Identifies when 2+ tasks are scheduled for the same time and displays warnings with affected pet/task info
- **Recurring task automation**: Auto-creates next occurrence when marking daily/weekly tasks complete (daily → next day, weekly → next week)
- **Break insertion**: Automatically inserts 10-minute breaks after every 2 tasks to prevent burnout
- **Task completion tracking**: Marks tasks as complete/incomplete with persistent state across sessions
- **Human-readable formatting**: Displays schedules with emoji indicators, due dates (Today, Tomorrow, In X days), and task priority/category

## 📸 Demo Walkthrough

Follow these steps to see PawPal+ in action:

1. **Create an owner profile** — Enter your name and set your availability hours (e.g., 8am–6pm). The app calculates your total available time in minutes.

2. **Add pets** — Create one or more pets with their species and age. Each pet will have its own task list that the scheduler manages together.

3. **Add tasks with details** — For each pet, add tasks by specifying: description, duration (minutes), priority (high/medium/low), category (exercise, nutrition, grooming, etc.), and frequency (once, daily, or weekly). Optionally set a specific start time.

4. **View today's schedule** — The app generates an optimized daily plan using multi-factor sorting (high priority first, short duration next) and respects your available time. If tasks conflict (2+ at same time), a warning appears. Breaks are automatically inserted after every 2 tasks.

5. **Check upcoming tasks** — Switch to the "Upcoming" tab to see all future occurrences of recurring tasks (daily and weekly), grouped by date with human-readable labels (Today, Tomorrow, In X days).

6. **Mark tasks complete** — In the Task Manager tab, click "Mark Complete" on any daily or weekly task. The app instantly creates the next occurrence (tomorrow for daily, next week for weekly) and removes the completed task from view.

7. **Monitor scheduling stats** — The Stats tab shows totals (tasks, completion rate, time allocation by pet) and a breakdown of task priorities per pet.

### Sample CLI Output

Running `main.py` demonstrates the scheduler in action:

```
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
  ☕ 08:50                - Break                  (10 min)
  ○ 09:00  🐱 Whiskers     - Cat feeding            (5 min) [high]
  ○ 09:00  🐕 Buddy        - Feeding                (10 min) [high]
  ○ 09:10  🐱 Whiskers     - Interactive play session (25 min) [medium]
  ☕ 09:15                - Break                  (10 min)
  ○ 14:00  🐕 Buddy        - Training session       (15 min) [medium]
  ○ 14:00  🐕 Buddy        - Afternoon playtime     (20 min) [medium]

NOT SCHEDULED:
  🐕 Buddy        - Grooming               (45 min) [low]
  🐕 Buddy        - Nail trim              (30 min) [low]

Scheduled: 120/600 minutes (20%)
Not scheduled: 75 minutes

============================================================
DEMONSTRATING RECURRING TASKS
============================================================

📋 Before marking tasks complete:
Buddy tasks: 6
Whiskers tasks: 3

✓ Marking 'Morning walk' as complete...
  (frequency: daily) → Next occurrence auto-created for 2026-07-08

✓ Marking 'Feeding' (Buddy) as complete...
  (frequency: daily) → Next occurrence auto-created for 2026-07-08

✓ Marking 'Grooming' as complete...
  (frequency: weekly) → Next occurrence auto-created for 2026-07-14

📋 After marking tasks complete:
Buddy tasks: 9
Whiskers tasks: 3

📅 Buddy's upcoming tasks:
  ✓ Morning walk              Today
  ✓ Feeding                   Today
  ○ Afternoon playtime        Today
  ○ Training session          Today
  ✓ Grooming                  Today
  ○ Nail trim                 No date
  ○ Morning walk              Tomorrow
  ○ Feeding                   Tomorrow
  ○ Grooming                  In 7 days (2026-07-14)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
