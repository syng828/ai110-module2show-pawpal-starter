import pawpal_system as pawpal
from datetime import date

if __name__ == "__main__":
    owner = pawpal.Owner("Stephanie")
    cat = pawpal.Pet("Mochi", "cat")
    dog = pawpal.Pet("Momoko", "dog")

    owner.add_pet(dog)
    owner.add_pet(cat)

    today = date.today().strftime("%Y-%m-%d")
    task1 = pawpal.Task("Feed Mochi", f"{today} 9:00 AM", "daily")
    task2 = pawpal.Task("Walk Momoko", f"{today} 10:00 AM", "daily")
    task3 = pawpal.Task("Play with Mochi", f"{today} 2:00 PM", "daily")

    cat.add_task(task1)
    dog.add_task(task2)
    cat.add_task(task3)

    scheduler = pawpal.Scheduler(owner)
    print(scheduler.schedule())