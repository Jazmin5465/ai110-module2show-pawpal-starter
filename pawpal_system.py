"""
PawPal+ Backend System

See diagrams/uml_draft.mmd for the class design.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Task:
    """Represents a pet care task with duration, priority, and category."""
    description: str
    duration: int
    priority: str
    category: str
    frequency: str = "once"
    start_time: Optional[str] = None
    completed: bool = False

    def is_high_priority(self) -> bool:
        """Check if this task has high priority."""
        return self.priority.lower() == "high"

    def estimate_time(self) -> int:
        """Estimate the time needed for this task."""
        return self.duration


@dataclass
class Pet:
    """Represents a pet with basic information and its tasks."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def describe(self) -> str:
        """Return a description of the pet."""
        return f"{self.name} is a {self.age}-year-old {self.species}"


class Owner:
    """Represents a pet owner with multiple pets and preferences."""

    def __init__(self, name: str, availability: Dict, preferences: Dict):
        self.name = name
        self.availability = availability
        self.preferences = preferences
        self.pets: List[Pet] = []

    def get_day_availability(self) -> str:
        """Get the owner's availability for the day."""
        if "start" in self.availability and "end" in self.availability:
            return f"Available from {self.availability['start']} to {self.availability['end']}"
        return str(self.availability)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's collection."""
        if pet in self.pets:
            self.pets.remove(pet)


class Scheduler:
    """Retrieves, organizes, and manages tasks across all of owner's pets."""

    def __init__(self, owner: Owner, total_minutes: int):
        self.owner = owner
        self.total_minutes = total_minutes

    def add_task(self, pet: Pet, task: Task) -> None:
        """Add a task to a specific pet's task list."""
        if pet in self.owner.pets:
            pet.tasks.append(task)

    def remove_task(self, pet: Pet, task: Task) -> None:
        """Remove a task from a specific pet's task list."""
        if pet in self.owner.pets and task in pet.tasks:
            pet.tasks.remove(task)

    def edit_task(self, pet: Pet, old_task: Task, new_task: Task) -> None:
        """Edit an existing task in a pet's task list."""
        if pet in self.owner.pets and old_task in pet.tasks:
            index = pet.tasks.index(old_task)
            pet.tasks[index] = new_task

    def mark_complete(self, pet: Pet, task: Task) -> None:
        """Mark a task as completed."""
        if pet in self.owner.pets and task in pet.tasks:
            task.completed = True

    def mark_incomplete(self, pet: Pet, task: Task) -> None:
        """Mark a task as incomplete."""
        if pet in self.owner.pets and task in pet.tasks:
            task.completed = False

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks across all owner's pets."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def validate_schedule(self) -> bool:
        """Check if total task duration fits within available time."""
        total_duration = sum(task.duration for task in self.get_all_tasks())
        return total_duration <= self.total_minutes

    def generate_plan(self) -> List[Task]:
        """Generate a daily plan prioritizing high-priority tasks that fit."""
        all_tasks = self.get_all_tasks()

        sorted_tasks = sorted(
            all_tasks,
            key=lambda t: (t.priority.lower() != "high", t.duration)
        )

        plan = []
        total_duration = 0
        for task in sorted_tasks:
            if total_duration + task.duration <= self.total_minutes:
                plan.append(task)
                total_duration += task.duration

        return plan

    def explain_plan(self) -> str:
        """Explain the reasoning behind the generated plan."""
        plan = self.generate_plan()
        all_tasks = self.get_all_tasks()

        pet_names = ", ".join(pet.name for pet in self.owner.pets) if self.owner.pets else "Unknown"
        explanation = f"Daily plan for {pet_names}:\n"
        explanation += f"Total time available: {self.total_minutes} minutes\n\n"

        total_time = sum(task.duration for task in plan)
        explanation += f"Tasks scheduled ({total_time} minutes):\n"
        for task in plan:
            explanation += f"  - {task.description} ({task.duration} min) [{task.priority}]\n"

        excluded = [task for task in all_tasks if task not in plan]
        if excluded:
            excluded_time = sum(task.duration for task in excluded)
            explanation += f"\nTasks not scheduled ({excluded_time} minutes):\n"
            for task in excluded:
                explanation += f"  - {task.description} ({task.duration} min) [{task.priority}]\n"

        return explanation

    def _time_to_minutes(self, time_str: str) -> int:
        """Convert time string (HH:MM) to minutes since midnight."""
        h, m = map(int, time_str.split(':'))
        return h * 60 + m

    def _minutes_to_time(self, minutes: int) -> str:
        """Convert minutes since midnight to time string (HH:MM)."""
        h = minutes // 60
        m = minutes % 60
        return f"{h:02d}:{m:02d}"

    def generate_scheduled_plan(self) -> List[tuple]:
        """Auto-assign time slots to tasks, returning (task, time, pet) tuples."""
        all_tasks = self.generate_plan()

        # Get owner availability
        avail = self.owner.availability
        start_mins = self._time_to_minutes(avail.get("start", "08:00"))
        end_mins = self._time_to_minutes(avail.get("end", "18:00"))

        # Build task to pet mapping
        task_to_pet = {}
        for pet in self.owner.pets:
            for task in pet.tasks:
                task_to_pet[id(task)] = pet

        # Separate tasks with and without assigned times
        timed_tasks = [t for t in all_tasks if t.start_time]
        untimed_tasks = [t for t in all_tasks if not t.start_time]

        # Build timeline of occupied slots from pre-assigned tasks
        occupied = []
        for task in timed_tasks:
            start = self._time_to_minutes(task.start_time)
            occupied.append((start, start + task.duration, task))
        occupied.sort()

        # Result list: keep pre-assigned tasks
        result = [(task, task.start_time, task_to_pet[id(task)]) for task in timed_tasks]

        # Sort untimed tasks by priority (high first) then duration
        untimed_tasks.sort(key=lambda t: (t.priority.lower() != "high", t.duration))

        # Assign times to untimed tasks
        for task in untimed_tasks:
            current = start_mins
            assigned = False

            # Try to fit in gaps between occupied slots
            for occ_start, occ_end, _ in occupied:
                if current + task.duration <= occ_start:
                    assigned_time = self._minutes_to_time(current)
                    result.append((task, assigned_time, task_to_pet[id(task)]))
                    occupied.append((current, current + task.duration, task))
                    occupied.sort()
                    assigned = True
                    break
                current = occ_end

            # Try to fit after last occupied slot
            if not assigned and current + task.duration <= end_mins:
                assigned_time = self._minutes_to_time(current)
                result.append((task, assigned_time, task_to_pet[id(task)]))

        return result

    def format_schedule(self) -> str:
        """Format the schedule as a readable list timeline with auto-assigned time slots."""
        scheduled_tasks = self.generate_scheduled_plan()
        all_tasks = self.get_all_tasks()
        plan = self.generate_plan()

        availability = self.owner.get_day_availability()

        output = []
        output.append("DAILY SCHEDULE FOR " + self.owner.name.upper())
        output.append(availability)
        output.append(f"Available: {self.total_minutes} minutes\n")

        # Sort by assigned time
        scheduled_tasks.sort(key=lambda x: self._time_to_minutes(x[1]))

        # Add scheduled tasks
        if scheduled_tasks:
            output.append("SCHEDULED TASKS:")
            for task, time_str, pet in scheduled_tasks:
                pet_emoji = "🐕" if pet.species in ["Dog", "Golden Retriever", "Labrador"] else "🐱"
                status = "✓" if task.completed else "○"
                output.append(f"  {status} {time_str:<5}  {pet_emoji} {pet.name:<12} - {task.description:<22} ({task.duration} min) [{task.priority}]")

        # Add unscheduled tasks (those that didn't fit in the plan)
        unscheduled = [task for task in all_tasks if task not in plan]
        if unscheduled:
            output.append("\nNOT SCHEDULED:")
            task_to_pet = {}
            for pet in self.owner.pets:
                for task in pet.tasks:
                    task_to_pet[id(task)] = pet

            for task in unscheduled:
                pet = task_to_pet[id(task)]
                pet_emoji = "🐕" if pet.species in ["Dog", "Golden Retriever", "Labrador"] else "🐱"
                output.append(f"  {pet_emoji} {pet.name:<12} - {task.description:<22} ({task.duration} min) [{task.priority}]")

        # Summary
        scheduled_time = sum(task.duration for task in plan)
        unscheduled_time = sum(task.duration for task in all_tasks if task not in plan)
        output.append("")
        output.append(f"Scheduled: {scheduled_time}/{self.total_minutes} minutes ({scheduled_time*100//self.total_minutes}%)")
        output.append(f"Not scheduled: {unscheduled_time} minutes")

        return "\n".join(output)
