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

During the design process, I utilized the planning mode in my AI tool to help give suggestions as we were building the initial class structure. I was able to have it scan through the README to see if there were any potential attributes that I may have missed in suggesting and would verify them throughout the building process as many were added to accommodate new features. I would also ask the AI for help debugging by having it list potential causes and solutions.

- What kinds of prompts or questions were most helpful?

The most helpful were by asking it to explain a design choice before implementing it so that I as the lead could best understand the direction it was heading in and making sure that it fulfilled the necessary requirements. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

When it came to suggesting how to output the schedule, I did not originally like how it was printing in the terminal. I knew that if I didn't address it early on, I would end up having more trouble fixing it in the UI later on during integration. I had the AI suggest different ways of formatting it and took the parts that I liked of its different suggestions.

- How did you evaluate or verify what the AI suggested?

I had both the AI run its test to verify that it worked but I also manually went and ran the necessary pytest commands after looking through the code to make sure that it was indeed working. I also made sure to read through its plan in implementing certain features such as when it came to optimizing the schedule to give my input on what aspects it should prioritize.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested the schedule making order on whether it was correctly sorting the tasks based on preferences, the completion of tasks and how they were marked, whether conflicting tasks were flagged with a message, and that recurring tasks were handled appropiately across the schedule and upcoming tasks sections.

- Why were these tests important?

They were important because the goal is to create an optimized schedule for pet owners which would not be possible if there were disorganized tasks that failed to give good planning suggestions and that are updated appropriately when marked completed to avoid confusion especially with reoccurring tasks.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I would say I was initially really confident. After optimizing the algorithm I was worried that it would overcomplicate things and confuse the program, however, it seems to pass all of the created tests so that boosts my confidence.

- What edge cases would you test next if you had more time?

I would definitely test with more pets and more tasks to see if it would in fact scale appropriately to a larger dataset.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I did have to use the AI a lot to get a good amount of the tedious work done, but it was done without fully taking away my decision making inputs.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I think I would mess around more with the UI if I had more time. I think that it may be a little buggy or could be better optimized for users since I feel like I prioritized the backend logic mainly for this project.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I liked the development process of the UML diagrams. I liked how I could have AI look over the README and my instructions to come up with the inital diagram, but it was also incredibly useful to ask it to look at the changes and create a final updated diagram to better reflect the project's final design.