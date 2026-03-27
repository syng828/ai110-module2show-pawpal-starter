# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

Features
Multi-pet task management — An Owner can register multiple Pet profiles (name, species); tasks are tracked per pet and aggregated across all pets.

Flexible task input — Each Task accepts either a scheduled datetime (string or datetime object in multiple formats) or an integer duration in minutes, handled by a single _parse_time_value parser.

Sorting by time — sort_by_time() orders tasks using a multi-key sort: scheduled tasks appear before unscheduled ones, ordered chronologically; unscheduled tasks are then ordered by duration (shortest first), with description as a final tiebreaker.

Filtering by status and pet — filter_tasks() supports filtering by completion status (pending / completed) and/or pet name (case-insensitive match), independently or combined.

Conflict detection — detect_time_conflicts() groups tasks by exact scheduled datetime and emits a human-readable warning for every timeslot shared by two or more pending tasks. Supports scoping to today-only or all dates.

Daily and weekly recurrence — When mark_task_complete() is called on a daily or weekly task, _build_next_occurrence() automatically creates a new task instance scheduled +1 day or +7 days forward and attaches it to the same pet.

Daily schedule builder — schedule() generates a formatted, chronologically sorted plain-text schedule for the day, listing each pending task with its time and frequency label (or "unscheduled" if no time is set).

Pending-first organization — organize_tasks() surfaces incomplete tasks before completed ones, with alphabetical tiebreaking within each group.

## Smarter Scheduling

Recent improvements added to the scheduler include:

- `sort_by_time(...)`: Orders tasks by scheduled datetime first, then by duration for unscheduled tasks.
- `filter_tasks(...)`: Filters tasks by completion status and/or pet name (case-insensitive pet matching).
- Recurring task rollover: When a `daily` or `weekly` task is marked complete, a new future occurrence is auto-created.
	- `daily` -> next due date is today + 1 day
	- `weekly` -> next due date is today + 7 days
- `detect_time_conflicts(...)`: Lightweight conflict detection that returns warning messages (instead of crashing) when two or more tasks share the same scheduled time.

These changes make the app more practical for day-to-day pet care by improving task visibility, repeat scheduling, and schedule safety.

## Testing PawPaL+
Run all tests with:

```bash
python -m pytest
```

Test coverage includes:

- Sorting correctness: verifies tasks are returned in chronological order.
- Recurrence logic: verifies completing daily and weekly tasks creates the next occurrence.
- Conflict detection: verifies duplicate scheduled times are flagged with warning messages.
- Core task behavior: verifies marking tasks complete and adding tasks to pets.

Latest result: `8 passed`.

Confidence Level: `(4/5)`

## Demo
<a href="/course_images/ai110/pawpal_ui.png" target="_blank"><img src='/course_images/ai110/pawpal_ui.png' /></a>