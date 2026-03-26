from datetime import date, datetime


class Task:
    """Represents a single activity for pet care."""

    def __init__(self, description, time_value, frequency, is_completed=False):
        self.description = description
        self.time_minutes = None
        self.scheduled_for = self._parse_time_value(time_value)
        self.frequency = frequency
        self.is_completed = bool(is_completed)

    def _parse_time_value(self, time_value):
        """Support either an integer duration or a datetime string."""
        if isinstance(time_value, int):
            self.time_minutes = time_value
            return None

        if isinstance(time_value, datetime):
            return time_value

        if not isinstance(time_value, str):
            raise ValueError("time_value must be an int, datetime, or datetime string")

        formats = [
            "%Y-%m-%d %I:%M %p",
            "%Y-%m-%d %H:%M",
            "%I:%M %p",
            "%H:%M",
        ]
        for fmt in formats:
            try:
                parsed = datetime.strptime(time_value, fmt)
                if fmt in {"%I:%M %p", "%H:%M"}:
                    today = date.today()
                    parsed = parsed.replace(year=today.year, month=today.month, day=today.day)
                return parsed
            except ValueError:
                continue

        raise ValueError(
            "Invalid time format. Use e.g. '2026-06-01 9:00 AM', '09:00', or an integer duration."
        )

    def mark_complete(self):
        """Mark the task as complete."""
        self.is_completed = True

    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.is_completed = False

    def __repr__(self):
        status = "done" if self.is_completed else "pending"
        return (
            f"Task(description={self.description!r}, time_minutes={self.time_minutes}, "
            f"frequency={self.frequency!r}, status={status})"
        )


class Pet:
    """Stores pet details and a list of tasks."""

    def __init__(self, name, species, age=None):
        self.name = name
        self.species = species
        self.age = age
        self.tasks = []

    def add_task(self, task):
        """Attach a task to this pet."""
        self.tasks.append(task)

    def get_pending_tasks(self):
        """Return only tasks that are not completed."""
        return [task for task in self.tasks if not task.is_completed]

    def __repr__(self):
        return f"Pet(name={self.name!r}, species={self.species!r}, tasks={len(self.tasks)})"


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return all tasks across all owned pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def __repr__(self):
        return f"Owner(name={self.name!r}, pets={len(self.pets)})"


class Scheduler:
    """The brain that retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner=None):
        self.owner = owner

    def _resolve_owner(self, owner=None):
        current_owner = owner or self.owner
        if current_owner is None:
            raise ValueError("Owner is required. Pass owner to Scheduler(owner) or schedule(owner).")
        return current_owner

    def retrieve_all_tasks(self, owner=None):
        """Get all tasks for this owner's pets."""
        current_owner = self._resolve_owner(owner)
        return current_owner.get_all_tasks()

    def retrieve_pending_tasks(self, owner=None):
        """Get all pending (not completed) tasks across pets."""
        return [task for task in self.retrieve_all_tasks(owner) if not task.is_completed]

    def organize_tasks(self, pending_first=True, owner=None):
        """Return tasks ordered for viewing/processing."""
        tasks = self.retrieve_all_tasks(owner)
        if pending_first:
            return sorted(tasks, key=lambda task: (task.is_completed, task.description.lower()))
        return sorted(tasks, key=lambda task: task.description.lower())

    def get_tasks_by_pet(self, owner=None):
        """Return a mapping of pet names to task lists."""
        current_owner = self._resolve_owner(owner)
        return {pet.name: list(pet.tasks) for pet in current_owner.pets}

    def mark_task_complete(self, task):
        """Mark a specific task as completed."""
        task.mark_complete()

    def schedule(self, owner=None, only_today=True):
        """Build a readable schedule string across all pets."""
        current_owner = self._resolve_owner(owner)
        entries = []

        for pet in current_owner.pets:
            for task in pet.tasks:
                if task.is_completed:
                    continue
                if only_today and task.scheduled_for is not None:
                    if task.scheduled_for.date() != date.today():
                        continue
                entries.append((pet.name, task))

        entries.sort(
            key=lambda item: (
                item[1].scheduled_for is None,
                item[1].scheduled_for or datetime.max,
                item[0].lower(),
                item[1].description.lower(),
            )
        )

        if not entries:
            return f"Today's schedule for {current_owner.name}: no pending tasks."

        lines = [f"Today's schedule for {current_owner.name}:"]
        for pet_name, task in entries:
            when = task.scheduled_for.strftime("%I:%M %p") if task.scheduled_for else "unscheduled"
            lines.append(f"- {when} | {pet_name}: {task.description} ({task.frequency})")
        return "\n".join(lines)
