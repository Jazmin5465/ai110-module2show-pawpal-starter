"""
Tests for PawPal+ backend system.
"""

from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


class TestTaskCompletion:
    """Tests for task completion functionality."""

    def test_mark_complete(self):
        """Verify that mark_complete() changes task's completed status."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet = Pet("Buddy", "Golden Retriever", 3)
        owner.add_pet(pet)

        scheduler = Scheduler(owner, 600)
        task = Task("Morning walk", 30, "high", "exercise")
        scheduler.add_task(pet, task)

        assert task.completed is False
        scheduler.mark_complete(pet, task)
        assert task.completed is True

    def test_mark_incomplete(self):
        """Verify that mark_incomplete() reverts completed status."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet = Pet("Buddy", "Golden Retriever", 3)
        owner.add_pet(pet)

        scheduler = Scheduler(owner, 600)
        task = Task("Morning walk", 30, "high", "exercise")
        scheduler.add_task(pet, task)

        scheduler.mark_complete(pet, task)
        assert task.completed is True
        scheduler.mark_incomplete(pet, task)
        assert task.completed is False


class TestTaskAddition:
    """Tests for task addition functionality."""

    def test_add_task_increases_count(self):
        """Verify that adding a task increases the pet's task count."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet = Pet("Buddy", "Golden Retriever", 3)
        owner.add_pet(pet)

        scheduler = Scheduler(owner, 600)

        assert len(pet.tasks) == 0
        task = Task("Morning walk", 30, "high", "exercise")
        scheduler.add_task(pet, task)
        assert len(pet.tasks) == 1

    def test_add_multiple_tasks(self):
        """Verify that multiple tasks can be added to a pet."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet = Pet("Buddy", "Golden Retriever", 3)
        owner.add_pet(pet)

        scheduler = Scheduler(owner, 600)

        task1 = Task("Morning walk", 30, "high", "exercise")
        task2 = Task("Feeding", 10, "high", "nutrition")
        task3 = Task("Playtime", 20, "medium", "exercise")

        scheduler.add_task(pet, task1)
        scheduler.add_task(pet, task2)
        scheduler.add_task(pet, task3)

        assert len(pet.tasks) == 3


class TestSortingCorrectness:
    """Tests for task sorting and chronological ordering."""

    def test_high_priority_before_low_priority(self):
        """Verify that high-priority tasks appear before low-priority tasks."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet = Pet("Buddy", "Golden Retriever", 3)
        owner.add_pet(pet)

        scheduler = Scheduler(owner, 600)
        today = date.today()

        high_task = Task("Feeding", 10, "high", "nutrition", due_date=today)
        low_task = Task("Grooming", 45, "low", "grooming", due_date=today)

        scheduler.add_task(pet, high_task)
        scheduler.add_task(pet, low_task)

        plan = scheduler.generate_plan()
        assert len(plan) == 2
        assert plan[0] == high_task
        assert plan[1] == low_task

    def test_shorter_duration_first_when_same_priority(self):
        """Verify that shorter tasks appear before longer tasks with same priority."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet = Pet("Buddy", "Golden Retriever", 3)
        owner.add_pet(pet)

        scheduler = Scheduler(owner, 600)
        today = date.today()

        long_task = Task("Long walk", 30, "high", "exercise", due_date=today)
        short_task = Task("Quick feeding", 10, "high", "nutrition", due_date=today)

        scheduler.add_task(pet, long_task)
        scheduler.add_task(pet, short_task)

        plan = scheduler.generate_plan()
        assert len(plan) == 2
        assert plan[0] == short_task
        assert plan[1] == long_task

    def test_scheduled_tasks_contain_both_timed_and_untimed(self):
        """Verify that both pre-assigned and auto-scheduled tasks appear in the plan."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet = Pet("Buddy", "Golden Retriever", 3)
        owner.add_pet(pet)

        scheduler = Scheduler(owner, 600)
        today = date.today()

        # One task with pre-assigned time, one without
        timed_task = Task("Morning walk", 30, "high", "exercise", due_date=today, start_time="08:00")
        untimed_task = Task("Afternoon playtime", 20, "medium", "exercise", due_date=today)

        scheduler.add_task(pet, timed_task)
        scheduler.add_task(pet, untimed_task)

        scheduled = scheduler.generate_scheduled_plan()
        # Filter to non-break tasks
        scheduled_tasks = [(task, time_str) for task, time_str, pet_obj in scheduled if pet_obj is not None]

        # Both tasks should be in the result
        assert len(scheduled_tasks) == 2, f"Expected 2 tasks, got {len(scheduled_tasks)}"
        task_descriptions = {desc for task, _ in scheduled_tasks for desc in [task.description]}
        assert "Morning walk" in task_descriptions
        assert "Afternoon playtime" in task_descriptions


class TestRecurringTasks:
    """Tests for recurring task auto-creation."""

    def test_daily_task_creates_next_occurrence(self):
        """Verify that marking a daily task complete auto-creates next occurrence."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet = Pet("Buddy", "Golden Retriever", 3)
        owner.add_pet(pet)

        scheduler = Scheduler(owner, 600)
        today = date.today()

        daily_task = Task("Morning walk", 30, "high", "exercise", frequency="daily", due_date=today)
        scheduler.add_task(pet, daily_task)

        assert len(pet.tasks) == 1
        scheduler.mark_complete(pet, daily_task)

        assert len(pet.tasks) == 2
        assert pet.tasks[1].due_date == today + timedelta(days=1)
        assert pet.tasks[1].completed is False

    def test_weekly_task_creates_next_occurrence(self):
        """Verify that marking a weekly task complete auto-creates next occurrence."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet = Pet("Buddy", "Golden Retriever", 3)
        owner.add_pet(pet)

        scheduler = Scheduler(owner, 600)
        today = date.today()

        weekly_task = Task("Bath day", 45, "medium", "grooming", frequency="weekly", due_date=today)
        scheduler.add_task(pet, weekly_task)

        assert len(pet.tasks) == 1
        scheduler.mark_complete(pet, weekly_task)

        assert len(pet.tasks) == 2
        assert pet.tasks[1].due_date == today + timedelta(weeks=1)
        assert pet.tasks[1].completed is False

    def test_once_task_does_not_recur(self):
        """Verify that marking a one-time task complete does NOT create a new occurrence."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet = Pet("Buddy", "Golden Retriever", 3)
        owner.add_pet(pet)

        scheduler = Scheduler(owner, 600)

        once_task = Task("Vet appointment", 60, "high", "medical", frequency="once")
        scheduler.add_task(pet, once_task)

        assert len(pet.tasks) == 1
        scheduler.mark_complete(pet, once_task)

        assert len(pet.tasks) == 1
        assert pet.tasks[0].completed is True

    def test_recurring_task_inherits_properties(self):
        """Verify that auto-created recurring tasks inherit all properties from the original."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet = Pet("Whiskers", "Cat", 2)
        owner.add_pet(pet)

        scheduler = Scheduler(owner, 600)
        today = date.today()

        original = Task(
            description="Cat feeding",
            duration=5,
            priority="high",
            category="nutrition",
            frequency="daily",
            due_date=today,
            start_time="09:00"
        )
        scheduler.add_task(pet, original)
        scheduler.mark_complete(pet, original)

        new_task = pet.tasks[1]
        assert new_task.description == original.description
        assert new_task.duration == original.duration
        assert new_task.priority == original.priority
        assert new_task.category == original.category
        assert new_task.frequency == original.frequency
        assert new_task.start_time == original.start_time


class TestConflictDetection:
    """Tests for time-slot conflict detection."""

    def test_two_tasks_same_start_time_both_appear(self):
        """Verify that tasks with identical start times both appear in scheduled plan."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet1 = Pet("Buddy", "Golden Retriever", 3)
        pet2 = Pet("Whiskers", "Cat", 2)
        owner.add_pet(pet1)
        owner.add_pet(pet2)

        scheduler = Scheduler(owner, 600)
        today = date.today()

        task1 = Task("Feeding", 10, "high", "nutrition", due_date=today, start_time="09:00")
        task2 = Task("Cat feeding", 5, "high", "nutrition", due_date=today, start_time="09:00")

        scheduler.add_task(pet1, task1)
        scheduler.add_task(pet2, task2)

        scheduled = scheduler.generate_scheduled_plan()
        # Extract times from non-break tasks
        task_times = [time_str for task, time_str, pet_obj in scheduled if pet_obj is not None]

        # Count how many times "09:00" appears
        conflict_count = sum(1 for t in task_times if t == "09:00")
        assert conflict_count >= 2, f"Expected at least 2 tasks at 09:00, got {conflict_count}"

    def test_no_conflict_with_different_start_times(self):
        """Verify that tasks with different start times don't create conflicts."""
        owner = Owner("Alice", {"start": "08:00", "end": "18:00"}, {})
        pet = Pet("Buddy", "Golden Retriever", 3)
        owner.add_pet(pet)

        scheduler = Scheduler(owner, 600)
        today = date.today()

        task1 = Task("Morning walk", 30, "high", "exercise", due_date=today, start_time="08:00")
        task2 = Task("Feeding", 10, "high", "nutrition", due_date=today, start_time="09:00")

        scheduler.add_task(pet, task1)
        scheduler.add_task(pet, task2)

        scheduled = scheduler.generate_scheduled_plan()
        # Extract times from non-break tasks
        task_times = [time_str for task, time_str, pet_obj in scheduled if pet_obj is not None]

        # Verify no time appears more than once
        for time_str in set(task_times):
            count = sum(1 for t in task_times if t == time_str)
            assert count == 1, f"Time {time_str} appears {count} times, expected exactly 1"
