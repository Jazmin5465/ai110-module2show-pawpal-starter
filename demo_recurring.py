"""
Demo: Recurring Tasks with Auto-Creation

Shows how daily/weekly tasks automatically create next occurrences
when marked complete.
"""

from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    print("\n" + "=" * 70)
    print("PAWPAL+ RECURRING TASKS DEMO")
    print("=" * 70)

    # Create owner and pets
    owner = Owner(
        name="Sam",
        availability={"start": "07:00", "end": "19:00"},
        preferences={"priority": "health", "min_breaks": 2}
    )

    max_dog = Pet(name="Max", species="Golden Retriever", age=2)
    luna_cat = Pet(name="Luna", species="Tabby Cat", age=1)

    owner.add_pet(max_dog)
    owner.add_pet(luna_cat)

    scheduler = Scheduler(owner=owner, total_minutes=720)

    # Create recurring tasks with due dates
    today = date.today()
    tomorrow = today + timedelta(days=1)

    # Daily tasks
    max_morning_walk = Task(
        description="Morning walk",
        duration=30,
        priority="high",
        category="exercise",
        frequency="daily",
        due_date=today,
        start_time="07:00"
    )

    max_feeding = Task(
        description="Feeding",
        duration=10,
        priority="high",
        category="nutrition",
        frequency="daily",
        due_date=today,
        start_time="08:00"
    )

    luna_feeding = Task(
        description="Cat feeding",
        duration=5,
        priority="high",
        category="nutrition",
        frequency="daily",
        due_date=today,
        start_time="08:15"
    )

    # Weekly task
    max_bath = Task(
        description="Bath day",
        duration=45,
        priority="medium",
        category="grooming",
        frequency="weekly",
        due_date=today,
        start_time="15:00"
    )

    # One-time task (no recurrence)
    vet_checkup = Task(
        description="Vet checkup",
        duration=60,
        priority="high",
        category="medical",
        frequency="once",
        due_date=today,
        start_time="10:00"
    )

    # Add tasks to scheduler
    scheduler.add_task(max_dog, max_morning_walk)
    scheduler.add_task(max_dog, max_feeding)
    scheduler.add_task(max_dog, max_bath)
    scheduler.add_task(max_dog, vet_checkup)
    scheduler.add_task(luna_cat, luna_feeding)

    # Show initial state
    print(f"\n📅 INITIAL TASK LIST (Today: {today})")
    print("-" * 70)
    print(f"Max's tasks: {len(max_dog.tasks)}")
    for task in max_dog.tasks:
        print(f"  • {task.description:<25} [{task.frequency:6}] {task.get_due_date_str()}")
    print(f"\nLuna's tasks: {len(luna_cat.tasks)}")
    for task in luna_cat.tasks:
        print(f"  • {task.description:<25} [{task.frequency:6}] {task.get_due_date_str()}")

    # Show today's schedule
    print(f"\n📋 TODAY'S SCHEDULE (with breaks & optimization)")
    print("-" * 70)
    print(scheduler.format_schedule())

    # Simulate completing tasks
    print("\n" + "=" * 70)
    print("COMPLETING TASKS...")
    print("=" * 70)

    print(f"\n✓ Marking 'Morning walk' as complete...")
    scheduler.mark_complete(max_dog, max_morning_walk)
    print(f"  → New 'Morning walk' task created for {max_morning_walk.due_date + timedelta(days=1)}")

    print(f"\n✓ Marking 'Feeding' (Max) as complete...")
    scheduler.mark_complete(max_dog, max_feeding)
    print(f"  → New 'Feeding' task created for {max_feeding.due_date + timedelta(days=1)}")

    print(f"\n✓ Marking 'Bath day' as complete...")
    scheduler.mark_complete(max_dog, max_bath)
    print(f"  → New 'Bath day' task created for {max_bath.due_date + timedelta(weeks=1)}")

    print(f"\n✓ Marking 'Vet checkup' as complete...")
    scheduler.mark_complete(max_dog, vet_checkup)
    print(f"  → (No new task - this is a one-time task)")

    # Show updated task list
    print(f"\n📅 UPDATED TASK LIST (after marking complete)")
    print("-" * 70)
    print(f"Max's tasks: {len(max_dog.tasks)}")
    for i, task in enumerate(max_dog.tasks, 1):
        status = "✓" if task.completed else "○"
        print(f"  {status} {task.description:<22} [{task.frequency:6}] {task.get_due_date_str()}")

    # Show what's available for tomorrow
    print(f"\n📅 TASKS FOR TOMORROW ({tomorrow})")
    print("-" * 70)
    tomorrow_tasks = [t for t in max_dog.tasks if t.due_date == tomorrow]
    if tomorrow_tasks:
        for task in tomorrow_tasks:
            print(f"  • {task.description:<25} ({task.duration} min)")
    else:
        print(f"  No tasks scheduled for tomorrow yet")

    # Show what's available for next week
    next_week = today + timedelta(weeks=1)
    print(f"\n📅 TASKS FOR NEXT WEEK ({next_week})")
    print("-" * 70)
    next_week_tasks = [t for t in max_dog.tasks if t.due_date == next_week]
    if next_week_tasks:
        for task in next_week_tasks:
            print(f"  • {task.description:<25} ({task.duration} min)")
    else:
        print(f"  No tasks scheduled for next week yet")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
