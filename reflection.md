# PawPal+ Project Reflection

## 1. System Design

Some core actions that a user should be able to perform: Add pet information, add pet tasks, determine pet tasks priority, see tasks listed out

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I included the following classes: Owner, Pet, Task, and Scheduler

Here are the following responsibilites:
Owner - Attributes: name, availability, preferences; Methods: get_day_availability()
Pet - Attributes: name, species, age; Methods: describe()
Task - Attributes: description, duration, priority, category; Methods: is_high_priority(), estimate_time()
Scheduler - Attributes: tasks, owner, pet, total_minutes; Methods: add_task(), remove_task(), generate_plan(), explain_plan()


**b. Design changes**

- Did your design change during implementation? Yes
- If yes, describe at least one change and why you made it.

I forgot to originally include the ability to edit tasks or mark them as a reoccuring event. The AI identified this and then made the edits to the neccessary classes.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers: total available time (hard limit), task priority (high/medium/low), task duration, category grouping, frequency (daily/weekly/once), due date (today only), pre-assigned time slots, and owner preferences (minimum breaks). Owner availability hours also constrain when tasks can be scheduled.

- How did you decide which constraints mattered most?

Priority was ranked first because feeding and health tasks are non-negotiables with time duration second because shorter high-priority tasks fill schedule gaps efficiently. Total available time is a hard ceiling that overrides all other constraints.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The scheduler prioritizes high-priority short tasks and defers lower-priority longer tasks if time runs out. Another tradeoff includes automatically creating recurring task instances increases task clutter but ensures pet care routines are never forgotten.

- Why is that tradeoff reasonable for this scenario?

For a busy pet owner, completing critical daily tasks (feeding, walks, medications) is more important than one-time maintenance tasks; deferred grooming can be rescheduled but a missed feeding harms the pet. Automatically including reoccuring ensures consistency in pet care even if it requires more task management.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
