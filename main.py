"""
PawPal+ Demo Script

Creates a sample owner with multiple pets and tasks,
then generates and displays a daily schedule.
Demonstrates recurring tasks that auto-create next occurrences.
"""

from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    # Create an owner
    owner = Owner(
        name="Alice",
        availability={"start": "08:00", "end": "18:00"},
        preferences={"priority": "health", "min_breaks": 2}
    )
    print(f"Owner: {owner.name}")
    print(f"Availability: {owner.get_day_availability()}\n")

    # Create pets
    buddy = Pet(name="Buddy", species="Golden Retriever", age=3)
    whiskers = Pet(name="Whiskers", species="Tabby Cat", age=2)

    # Add pets to owner
    owner.add_pet(buddy)
    owner.add_pet(whiskers)
    print(f"Pets: {', '.join([pet.name for pet in owner.pets])}")
    print(f"  - {buddy.describe()}")
    print(f"  - {whiskers.describe()}\n")

    # Create a scheduler with 600 minutes (10 hours) available
    scheduler = Scheduler(owner=owner, total_minutes=600)

    # Use today's date for recurring tasks
    today = date.today()

    # Add tasks for Buddy
    buddy_walk = Task(
        description="Morning walk",
        duration=30,
        priority="high",
        category="exercise",
        frequency="daily",
        due_date=today,
        start_time="08:00"
    )
    buddy_feeding = Task(
        description="Feeding",
        duration=10,
        priority="high",
        category="nutrition",
        frequency="daily",
        due_date=today,
        start_time="09:00"
    )
    buddy_playtime = Task(
        description="Afternoon playtime",
        duration=20,
        priority="medium",
        category="exercise",
        frequency="daily",
        due_date=today,
        start_time="14:00"
    )
    buddy_training = Task(
        description="Training session",
        duration=15,
        priority="medium",
        category="enrichment",
        frequency="daily",
        due_date=today,
        start_time="14:00"  # CONFLICTS with playtime at same time
    )
    buddy_grooming = Task(
        description="Grooming",
        duration=45,
        priority="low",
        category="grooming",
        frequency="weekly",
        due_date=today
    )
    buddy_nail_trim = Task(
        description="Nail trim",
        duration=30,
        priority="low",
        category="grooming",
        frequency="weekly"  # Not included in daily schedule
    )

    scheduler.add_task(buddy, buddy_walk)
    scheduler.add_task(buddy, buddy_feeding)
    scheduler.add_task(buddy, buddy_playtime)
    scheduler.add_task(buddy, buddy_training)  # Conflicts with playtime at 14:00
    scheduler.add_task(buddy, buddy_grooming)
    scheduler.add_task(buddy, buddy_nail_trim)

    # Add tasks for Whiskers
    whiskers_feeding = Task(
        description="Cat feeding",
        duration=5,
        priority="high",
        category="nutrition",
        frequency="daily",
        due_date=today,
        start_time="09:00"
    )
    whiskers_litter = Task(
        description="Litter box cleaning",
        duration=15,
        priority="medium",
        category="hygiene",
        frequency="daily",
        due_date=today
    )
    whiskers_playtime = Task(
        description="Interactive play session",
        duration=25,
        priority="medium",
        category="enrichment",
        frequency="daily",
        due_date=today
    )

    scheduler.add_task(whiskers, whiskers_feeding)
    scheduler.add_task(whiskers, whiskers_litter)
    scheduler.add_task(whiskers, whiskers_playtime)

    # Validate and display schedule
    print()
    is_valid = scheduler.validate_schedule()
    print(f"Schedule valid (fits in {scheduler.total_minutes} min): {is_valid}\n")

    print(scheduler.format_schedule())

    # Demonstrate recurring tasks
    print("\n" + "=" * 60)
    print("DEMONSTRATING RECURRING TASKS")
    print("=" * 60)

    print(f"\n📋 Before marking tasks complete:")
    print(f"Buddy tasks: {len(buddy.tasks)}")
    print(f"Whiskers tasks: {len(whiskers.tasks)}")

    print(f"\n✓ Marking 'Morning walk' as complete...")
    print(f"  (frequency: daily) → Next occurrence auto-created for {(today + timedelta(days=1)).strftime('%Y-%m-%d')}")
    scheduler.mark_complete(buddy, buddy_walk)

    print(f"\n✓ Marking 'Feeding' (Buddy) as complete...")
    print(f"  (frequency: daily) → Next occurrence auto-created for {(today + timedelta(days=1)).strftime('%Y-%m-%d')}")
    scheduler.mark_complete(buddy, buddy_feeding)

    print(f"\n✓ Marking 'Grooming' as complete...")
    print(f"  (frequency: weekly) → Next occurrence auto-created for {(today + timedelta(weeks=1)).strftime('%Y-%m-%d')}")
    scheduler.mark_complete(buddy, buddy_grooming)

    print(f"\n📋 After marking tasks complete:")
    print(f"Buddy tasks: {len(buddy.tasks)}")
    print(f"Whiskers tasks: {len(whiskers.tasks)}")

    print(f"\n📅 Buddy's upcoming tasks:")
    for task in buddy.tasks:
        status = "✓" if task.completed else "○"
        due = task.get_due_date_str() if task.due_date else "No date"
        print(f"  {status} {task.description:<25} {due}")


if __name__ == "__main__":
    main()
