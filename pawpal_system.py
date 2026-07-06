"""
PawPal+ Backend System

See diagrams/uml_draft.mmd for the class design.
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Task:
    """Represents a pet care task with duration, priority, and category."""
    description: str
    duration: int
    priority: str
    category: str

    def is_high_priority(self) -> bool:
        """Check if this task has high priority."""
        pass

    def estimate_time(self) -> int:
        """Estimate the time needed for this task."""
        pass


@dataclass
class Pet:
    """Represents a pet with basic information."""
    name: str
    species: str
    age: int

    def describe(self) -> str:
        """Return a description of the pet."""
        pass


class Owner:
    """Represents a pet owner with availability and preferences."""

    def __init__(self, name: str, availability: Dict, preferences: Dict):
        self.name = name
        self.availability = availability
        self.preferences = preferences

    def get_day_availability(self) -> str:
        """Get the owner's availability for the day."""
        pass


class Scheduler:
    """Manages scheduling of tasks for a pet based on owner constraints."""

    def __init__(self, owner: Owner, pet: Pet, total_minutes: int):
        self.tasks: List[Task] = []
        self.owner = owner
        self.pet = pet
        self.total_minutes = total_minutes

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule."""
        pass

    def generate_plan(self) -> List[Task]:
        """Generate a daily plan based on constraints and priorities."""
        pass

    def explain_plan(self) -> str:
        """Explain the reasoning behind the generated plan."""
        pass
