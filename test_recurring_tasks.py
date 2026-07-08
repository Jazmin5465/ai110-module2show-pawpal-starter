"""
Test script to demonstrate auto-creation of recurring tasks when marked complete.
"""

from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def test_daily_task_recurrence():
    """Test that daily tasks auto-create the next occurrence."""
    print("=" * 60)
    print("TEST: Daily Task Recurrence")
    print("=" * 60)

    owner = Owner(
        name="Bob",
        availability={"start": "08:00", "end": "18:00"},
        preferences={"priority": "health", "min_breaks": 1}
    )

    buddy = Pet(name="Buddy", species="Dog", age=3)
    owner.add_pet(buddy)

    scheduler = Scheduler(owner=owner, total_minutes=600)

    # Create a daily feeding task for today
    today = date.today()
    daily_feeding = Task(
        description="Daily feeding",
        duration=10,
        priority="high",
        category="nutrition",
        frequency="daily",
        due_date=today,
        completed=False
    )

    scheduler.add_task(buddy, daily_feeding)

    print(f"\nBefore marking complete:")
    print(f"  Tasks in Buddy's list: {len(buddy.tasks)}")
    for i, task in enumerate(buddy.tasks, 1):
        print(f"    {i}. {task.description} (due: {task.due_date}, completed: {task.completed})")

    # Mark the task as complete
    scheduler.mark_complete(buddy, daily_feeding)

    print(f"\nAfter marking complete:")
    print(f"  Tasks in Buddy's list: {len(buddy.tasks)}")
    for i, task in enumerate(buddy.tasks, 1):
        print(f"    {i}. {task.description} (due: {task.due_date}, completed: {task.completed})")

    # Verify the next occurrence was created
    assert len(buddy.tasks) == 2, "Should have 2 tasks after completion"
    assert buddy.tasks[0].completed == True, "Original task should be marked complete"
    assert buddy.tasks[1].completed == False, "New task should not be completed"
    assert buddy.tasks[1].due_date == today + timedelta(days=1), "Next task should be due tomorrow"
    print("\n✓ Daily task recurrence test PASSED")


def test_weekly_task_recurrence():
    """Test that weekly tasks auto-create the next occurrence."""
    print("\n" + "=" * 60)
    print("TEST: Weekly Task Recurrence")
    print("=" * 60)

    owner = Owner(
        name="Alice",
        availability={"start": "08:00", "end": "18:00"},
        preferences={"priority": "health"}
    )

    whiskers = Pet(name="Whiskers", species="Cat", age=2)
    owner.add_pet(whiskers)

    scheduler = Scheduler(owner=owner, total_minutes=600)

    # Create a weekly grooming task
    today = date.today()
    weekly_groom = Task(
        description="Weekly grooming",
        duration=45,
        priority="medium",
        category="grooming",
        frequency="weekly",
        due_date=today,
        completed=False
    )

    scheduler.add_task(whiskers, weekly_groom)

    print(f"\nBefore marking complete:")
    print(f"  Tasks in Whiskers's list: {len(whiskers.tasks)}")
    for i, task in enumerate(whiskers.tasks, 1):
        print(f"    {i}. {task.description} (due: {task.due_date}, completed: {task.completed})")

    # Mark the task as complete
    scheduler.mark_complete(whiskers, weekly_groom)

    print(f"\nAfter marking complete:")
    print(f"  Tasks in Whiskers's list: {len(whiskers.tasks)}")
    for i, task in enumerate(whiskers.tasks, 1):
        print(f"    {i}. {task.description} (due: {task.due_date}, completed: {task.completed})")

    # Verify the next occurrence was created
    assert len(whiskers.tasks) == 2, "Should have 2 tasks after completion"
    assert whiskers.tasks[0].completed == True, "Original task should be marked complete"
    assert whiskers.tasks[1].completed == False, "New task should not be completed"
    assert whiskers.tasks[1].due_date == today + timedelta(weeks=1), "Next task should be due in 1 week"
    print("\n✓ Weekly task recurrence test PASSED")


def test_one_time_task_no_recurrence():
    """Test that one-time tasks don't create new occurrences."""
    print("\n" + "=" * 60)
    print("TEST: One-Time Task (No Recurrence)")
    print("=" * 60)

    owner = Owner(
        name="Charlie",
        availability={"start": "08:00", "end": "18:00"},
        preferences={"priority": "health"}
    )

    dog = Pet(name="Rex", species="Dog", age=5)
    owner.add_pet(dog)

    scheduler = Scheduler(owner=owner, total_minutes=600)

    # Create a one-time vet appointment
    today = date.today()
    vet_visit = Task(
        description="Vet appointment",
        duration=60,
        priority="high",
        category="medical",
        frequency="once",
        due_date=today,
        completed=False
    )

    scheduler.add_task(dog, vet_visit)

    print(f"\nBefore marking complete:")
    print(f"  Tasks in Rex's list: {len(dog.tasks)}")

    # Mark the task as complete
    scheduler.mark_complete(dog, vet_visit)

    print(f"\nAfter marking complete:")
    print(f"  Tasks in Rex's list: {len(dog.tasks)}")

    # Verify no new occurrence was created
    assert len(dog.tasks) == 1, "Should still have only 1 task (one-time task)"
    assert dog.tasks[0].completed == True, "Task should be marked complete"
    print("\n✓ One-time task test PASSED")


if __name__ == "__main__":
    test_daily_task_recurrence()
    test_weekly_task_recurrence()
    test_one_time_task_no_recurrence()
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! ✓")
    print("=" * 60)
