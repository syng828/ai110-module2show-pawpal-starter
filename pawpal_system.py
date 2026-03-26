class Pet:
    """Represents a pet with its attributes and care needs."""
    
    def __init__(self, name, species, age, breed):
        self.name = name
        self.species = species
        self.age = age
        self.breed = breed
        self.special_needs = []
    
    def add_special_need(self, need):
        """Add a special need for the pet."""
        pass
    
    def __repr__(self):
        """Return string representation of the pet."""
        pass


class Owner:
    """Represents a pet owner and their availability."""
    
    def __init__(self, name, available_minutes, preferred_start_time):
        self.name = name
        self.available_minutes = available_minutes
        self.preferred_start_time = preferred_start_time
        self.pets = []
    
    def add_pet(self, pet):
        """Add a pet to the owner's pet list."""
        pass
    
    def get_total_available_time(self):
        """Return the total available time in minutes."""
        pass


class Task:
    """Represents a task related to pet care."""
    
    def __init__(self, title, duration_minutes, priority, category, is_required, time_of_day):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.is_required = is_required
        self.time_of_day = time_of_day
    
    def priority_score(self):
        """Calculate and return the priority score for the task."""
        pass
    
    def __repr__(self):
        """Return string representation of the task."""
        pass


class ScheduledTask:
    """Represents a task that has been scheduled at a specific time."""
    
    def __init__(self, task, start_time, end_time, reason):
        self.task = task
        self.start_time = start_time
        self.end_time = end_time
        self.reason = reason
    
    def duration(self):
        """Calculate and return the duration of the scheduled task."""
        pass
    
    def to_dict(self):
        """Convert the scheduled task to a dictionary representation."""
        pass


class Scheduler:
    """Manages task scheduling for a pet owner."""
    
    def __init__(self, owner, pet):
        self.owner = owner
        self.pet = pet
        self.tasks = []
    
    def add_task(self, task):
        """Add a task to the scheduler's task list."""
        pass
    
    def generate_plan(self):
        """Generate and return a list of scheduled tasks."""
        pass
    
    def explain_plan(self, plan):
        """Provide a string explanation of the generated plan."""
        pass
    
    def total_scheduled_minutes(self, plan):
        """Calculate and return the total minutes for all scheduled tasks."""
        pass
