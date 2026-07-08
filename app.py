"""
PawPal+ Streamlit Frontend

Interactive pet care scheduling app with session state management.
Includes recurring tasks with auto-creation of next occurrences.
"""

import streamlit as st
from datetime import date, timedelta
import importlib
import sys

# Force reload of pawpal_system to ensure latest changes are used
if 'pawpal_system' in sys.modules:
    importlib.reload(sys.modules['pawpal_system'])

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐕", layout="wide")

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None


def initialize_owner(name: str, start_time: str, end_time: str) -> None:
    """Create a new owner and scheduler."""
    st.session_state.owner = Owner(
        name=name,
        availability={"start": start_time, "end": end_time},
        preferences={}
    )
    total_mins = (int(end_time.split(":")[0]) - int(start_time.split(":")[0])) * 60
    st.session_state.scheduler = Scheduler(st.session_state.owner, total_mins)


# Sidebar: Owner Management
st.sidebar.title("🐕 PawPal+")

if st.session_state.owner is None:
    st.sidebar.header("Create Owner")
    with st.sidebar.form("owner_form"):
        owner_name = st.text_input("Owner name", placeholder="e.g., Alice")
        start_time = st.selectbox("Available from", [f"{h:02d}:00" for h in range(6, 24)], index=2)
        end_time = st.selectbox("Available until", [f"{h:02d}:00" for h in range(6, 24)], index=12)

        if st.form_submit_button("Create Owner"):
            if owner_name:
                initialize_owner(owner_name, start_time, end_time)
                st.success(f"Owner '{owner_name}' created!")
                st.rerun()
            else:
                st.error("Please enter an owner name")
else:
    st.sidebar.success(f"Owner: {st.session_state.owner.name}")
    if st.sidebar.button("🔄 Reset"):
        st.session_state.owner = None
        st.session_state.scheduler = None
        st.rerun()


# Main App
st.title("🐕 PawPal+ Pet Care Scheduler")

if st.session_state.owner is None:
    st.info("👈 Create an owner in the sidebar to get started")
else:
    owner = st.session_state.owner
    scheduler = st.session_state.scheduler

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pets & Tasks", "Schedule", "Task Manager", "Upcoming", "Stats"])

    # TAB 1: Pets & Tasks
    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🐾 Pets")
            if owner.pets:
                for i, pet in enumerate(owner.pets):
                    with st.expander(f"{pet.name} ({pet.species})"):
                        st.write(pet.describe())
                        st.write(f"**Tasks:** {len(pet.tasks)}")

                        if st.button(f"Remove {pet.name}", key=f"remove_pet_{i}"):
                            owner.remove_pet(pet)
                            st.rerun()
            else:
                st.write("No pets yet")

            st.divider()
            st.subheader("➕ Add Pet")
            with st.form("add_pet_form"):
                pet_name = st.text_input("Pet name", placeholder="e.g., Buddy")
                pet_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Rabbit", "Other"])
                pet_age = st.slider("Age (years)", 0, 20, 1)

                if st.form_submit_button("Add Pet"):
                    if pet_name:
                        new_pet = Pet(name=pet_name, species=pet_species, age=pet_age)
                        owner.add_pet(new_pet)
                        st.success(f"Added {pet_name}!")
                        st.rerun()
                    else:
                        st.error("Please enter a pet name")

        with col2:
            st.subheader("📋 Add Task")
            if not owner.pets:
                st.warning("Add a pet first")
            else:
                with st.form("add_task_form"):
                    pet_idx = st.selectbox("Pet", range(len(owner.pets)), format_func=lambda i: owner.pets[i].name)
                    pet = owner.pets[pet_idx]

                    task_desc = st.text_input("Task description", placeholder="e.g., Morning walk")
                    task_duration = st.slider("Duration (minutes)", 5, 180, 30)
                    task_priority = st.selectbox("Priority", ["low", "medium", "high"])
                    task_category = st.selectbox("Category", ["exercise", "nutrition", "grooming", "hygiene", "enrichment", "medical"])
                    task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
                    task_time = st.selectbox("Scheduled time (optional)",
                                            ["—"] + [f"{h:02d}:00" for h in range(6, 24)],
                                            help="Leave as '—' for auto-scheduling")

                    if st.form_submit_button("Add Task"):
                        if task_desc:
                            new_task = Task(
                                description=task_desc,
                                duration=task_duration,
                                priority=task_priority,
                                category=task_category,
                                frequency=task_frequency,
                                start_time=None if task_time == "—" else task_time,
                                due_date=date.today()
                            )
                            scheduler.add_task(pet, new_task)
                            st.success(f"Added task to {pet.name}!")
                            st.rerun()
                        else:
                            st.error("Please enter a task description")

    # TAB 2: Schedule
    with tab2:
        st.subheader("📅 Today's Schedule")

        if not owner.pets or not scheduler.get_all_tasks():
            st.info("Add pets and tasks to see a schedule")
        else:
            is_valid = scheduler.validate_schedule()
            if is_valid:
                st.success("✓ Schedule fits within available time")
            else:
                st.warning("⚠️ Some tasks don't fit in available time")

            # Check for time conflicts (multiple tasks at same time)
            scheduled_tasks = scheduler.generate_scheduled_plan()
            time_conflicts = {}
            for task, time_str, pet in scheduled_tasks:
                if pet is not None:  # Skip break tasks
                    if time_str not in time_conflicts:
                        time_conflicts[time_str] = []
                    time_conflicts[time_str].append((task.description, pet.name))

            # Show warning if there are conflicts
            conflicts = {t: tasks for t, tasks in time_conflicts.items() if len(tasks) > 1}
            if conflicts:
                warning_text = "⚠️ **Time conflicts detected:**\n"
                for time_str in sorted(conflicts.keys()):
                    tasks = conflicts[time_str]
                    task_list = ", ".join([f"{pet}'s {desc}" for desc, pet in tasks])
                    warning_text += f"  • {time_str}: {task_list}\n"
                st.warning(warning_text)

            st.text(scheduler.format_schedule())

    # TAB 3: Task Manager
    with tab3:
        st.subheader("✏️ Manage Tasks")

        if not owner.pets:
            st.info("Add a pet first")
        else:
            all_tasks = scheduler.get_all_tasks()
            if not all_tasks:
                st.info("No tasks added yet")
            else:
                # Build pet lookup
                task_to_pet = {}
                for pet in owner.pets:
                    for task in pet.tasks:
                        task_to_pet[id(task)] = pet

                for task in all_tasks:
                    pet = task_to_pet[id(task)]

                    # Show task with due date and frequency badge
                    due_info = f" • {task.get_due_date_str()}" if task.due_date else ""
                    freq_badge = f" [{task.frequency.upper()}]" if task.frequency != "once" else ""
                    expander_title = f"{task.description} ({pet.name}){freq_badge}{due_info}"

                    with st.expander(expander_title, expanded=False):
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            if st.button(f"✓ Mark Complete" if not task.completed else "⊘ Mark Incomplete",
                                       key=f"toggle_{id(task)}"):
                                if task.completed:
                                    scheduler.mark_incomplete(pet, task)
                                else:
                                    scheduler.mark_complete(pet, task)
                                    # Show info about auto-created next occurrence
                                    if task.frequency in ["daily", "weekly"]:
                                        if task.frequency == "daily":
                                            next_date = (task.due_date + timedelta(days=1)).strftime("%Y-%m-%d")
                                        else:
                                            next_date = (task.due_date + timedelta(weeks=1)).strftime("%Y-%m-%d")
                                        st.info(f"✨ Next occurrence auto-created for {next_date}")
                                st.rerun()

                        with col2:
                            new_duration = st.number_input("Duration (min)", value=task.duration, key=f"dur_{id(task)}")
                            if new_duration != task.duration:
                                task.duration = new_duration

                        with col3:
                            if st.button("🗑️ Delete", key=f"del_{id(task)}"):
                                scheduler.remove_task(pet, task)
                                st.rerun()

                        # Status and details
                        status_text = "✓ Completed" if task.completed else "○ Incomplete"
                        st.caption(f"Status: {status_text} | Priority: {task.priority} | Category: {task.category}")
                        if task.due_date:
                            st.caption(f"Due: {task.get_due_date_str()}")

    # TAB 4: Upcoming Tasks
    with tab4:
        st.subheader("📅 Upcoming Recurring Tasks")

        all_tasks = scheduler.get_all_tasks()
        if not all_tasks:
            st.info("No tasks yet")
        else:
            # Build pet lookup
            task_to_pet = {}
            for pet in owner.pets:
                for task in pet.tasks:
                    task_to_pet[id(task)] = pet

            # Group tasks by due date
            tasks_by_date = {}
            for task in all_tasks:
                if task.due_date and not task.completed and task.frequency != "once":
                    if task.due_date not in tasks_by_date:
                        tasks_by_date[task.due_date] = []
                    tasks_by_date[task.due_date].append(task)

            if not tasks_by_date:
                st.info("No upcoming recurring tasks (all tasks are completed or one-time)")
            else:
                # Sort by date
                for task_date in sorted(tasks_by_date.keys()):
                    # Format date nicely
                    today = date.today()
                    if task_date == today:
                        date_label = "📆 Today"
                    elif task_date == today + timedelta(days=1):
                        date_label = "📆 Tomorrow"
                    else:
                        days_away = (task_date - today).days
                        date_label = f"📆 {task_date.strftime('%A, %B %d')} (in {days_away} days)"

                    with st.expander(date_label):
                        for task in tasks_by_date[task_date]:
                            pet = task_to_pet[id(task)]
                            emoji = "🐕" if pet.species in ["Dog", "Golden Retriever", "Labrador"] else "🐱"
                            st.write(f"{emoji} **{pet.name}**: {task.description} ({task.duration} min) - {task.priority}")

    # TAB 5: Stats
    with tab5:
        st.subheader("📊 Statistics")

        all_tasks = scheduler.get_all_tasks()
        if all_tasks:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Tasks", len(all_tasks))

            with col2:
                completed = sum(1 for t in all_tasks if t.completed)
                st.metric("Completed", completed)

            with col3:
                total_duration = sum(t.duration for t in all_tasks)
                st.metric("Total Duration", f"{total_duration} min")

            with col4:
                plan = scheduler.generate_plan()
                st.metric("Scheduled", len(plan))

            st.divider()

            # Task breakdown by pet
            st.subheader("Tasks by Pet")
            for pet in owner.pets:
                high = sum(1 for t in pet.tasks if t.is_high_priority())
                med = sum(1 for t in pet.tasks if t.priority.lower() == "medium")
                low = sum(1 for t in pet.tasks if t.priority.lower() == "low")

                st.write(f"**{pet.name}**: {len(pet.tasks)} total | 🔴 {high} high | 🟡 {med} medium | 🟢 {low} low")
        else:
            st.info("No tasks yet")
