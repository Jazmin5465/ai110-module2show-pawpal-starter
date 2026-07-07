"""
Tests for PawPal+ backend system.
"""

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
