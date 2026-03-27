import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task(description="Feed Buddy", time_value=10, frequency="daily")
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Walk Buddy", time_value=30, frequency="daily"))
    assert len(pet.tasks) == 1


def test_sort_by_time_orders_scheduled_then_unscheduled_duration():
    owner = Owner(name="Sam")
    pet = Pet(name="Buddy", species="dog")
    owner.add_pet(pet)

    today = date.today().strftime("%Y-%m-%d")
    later_walk = Task(description="Later walk", time_value=f"{today} 10:00 AM", frequency="daily")
    early_feed = Task(description="Early feed", time_value=f"{today} 09:00 AM", frequency="daily")
    short_play = Task(description="Play", time_value=15, frequency="daily")
    long_train = Task(description="Training", time_value=40, frequency="daily")

    pet.add_task(later_walk)
    pet.add_task(short_play)
    pet.add_task(early_feed)
    pet.add_task(long_train)

    sorted_tasks = Scheduler(owner).sort_by_time()

    assert [task.description for task in sorted_tasks] == [
        "Early feed",
        "Later walk",
        "Play",
        "Training",
    ]


def test_filter_tasks_by_completion_status():
    owner = Owner(name="Sam")
    pet = Pet(name="Buddy", species="dog")
    owner.add_pet(pet)

    completed_task = Task(description="Brush", time_value=10, frequency="weekly")
    pending_task = Task(description="Walk", time_value=20, frequency="daily")
    completed_task.mark_complete()

    pet.add_task(completed_task)
    pet.add_task(pending_task)

    scheduler = Scheduler(owner)
    done_tasks = scheduler.filter_tasks(is_completed=True)
    pending_tasks = scheduler.filter_tasks(is_completed=False)

    assert [task.description for task in done_tasks] == ["Brush"]
    assert [task.description for task in pending_tasks] == ["Walk"]


def test_filter_tasks_by_pet_name_and_completion():
    owner = Owner(name="Sam")
    dog = Pet(name="Buddy", species="dog")
    cat = Pet(name="Mochi", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog_task = Task(description="Dog walk", time_value=30, frequency="daily")
    cat_done_task = Task(description="Cat meds", time_value=5, frequency="daily")
    cat_pending_task = Task(description="Cat play", time_value=15, frequency="daily")
    cat_done_task.mark_complete()

    dog.add_task(dog_task)
    cat.add_task(cat_done_task)
    cat.add_task(cat_pending_task)

    scheduler = Scheduler(owner)
    mochi_tasks = scheduler.filter_tasks(pet_name="mochi")
    mochi_done_tasks = scheduler.filter_tasks(pet_name="Mochi", is_completed=True)

    assert [task.description for task in mochi_tasks] == ["Cat meds", "Cat play"]
    assert [task.description for task in mochi_done_tasks] == ["Cat meds"]


def test_mark_task_complete_creates_next_daily_occurrence():
    owner = Owner(name="Sam")
    pet = Pet(name="Buddy", species="dog")
    owner.add_pet(pet)

    today = date.today().strftime("%Y-%m-%d")
    daily_task = Task(description="Morning walk", time_value=f"{today} 08:00 AM", frequency="daily")
    pet.add_task(daily_task)

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(daily_task)

    assert daily_task.is_completed is True
    assert next_task is not None
    assert next_task in pet.tasks
    assert next_task.is_completed is False
    assert next_task.scheduled_for.date() == date.today() + timedelta(days=1)
    assert next_task.scheduled_for.time() == daily_task.scheduled_for.time()


def test_mark_task_complete_creates_next_weekly_occurrence():
    owner = Owner(name="Sam")
    pet = Pet(name="Mochi", species="cat")
    owner.add_pet(pet)

    today = date.today().strftime("%Y-%m-%d")
    weekly_task = Task(description="Nail trim", time_value=f"{today} 07:30 PM", frequency="weekly")
    pet.add_task(weekly_task)

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(weekly_task)

    assert weekly_task.is_completed is True
    assert next_task is not None
    assert next_task in pet.tasks
    assert next_task.scheduled_for.date() == date.today() + timedelta(days=7)
    assert next_task.scheduled_for.time() == weekly_task.scheduled_for.time()


def test_detect_time_conflicts_returns_warning_messages():
    owner = Owner(name="Sam")
    dog = Pet(name="Buddy", species="dog")
    cat = Pet(name="Mochi", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    today = date.today().strftime("%Y-%m-%d")
    dog_task = Task(description="Dog walk", time_value=f"{today} 10:00 AM", frequency="daily")
    cat_task = Task(description="Cat play", time_value=f"{today} 10:00 AM", frequency="daily")
    dog.add_task(dog_task)
    cat.add_task(cat_task)

    warnings = Scheduler(owner).detect_time_conflicts()

    assert len(warnings) == 1
    assert "Warning: time conflict" in warnings[0]
    assert "Buddy: Dog walk" in warnings[0]
    assert "Mochi: Cat play" in warnings[0]
