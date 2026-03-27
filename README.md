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

## Smarter Scheduling

Recent improvements added to the scheduler include:

- `sort_by_time(...)`: Orders tasks by scheduled datetime first, then by duration for unscheduled tasks.
- `filter_tasks(...)`: Filters tasks by completion status and/or pet name (case-insensitive pet matching).
- Recurring task rollover: When a `daily` or `weekly` task is marked complete, a new future occurrence is auto-created.
	- `daily` -> next due date is today + 1 day
	- `weekly` -> next due date is today + 7 days
- `detect_time_conflicts(...)`: Lightweight conflict detection that returns warning messages (instead of crashing) when two or more tasks share the same scheduled time.

These changes make the app more practical for day-to-day pet care by improving task visibility, repeat scheduling, and schedule safety.
