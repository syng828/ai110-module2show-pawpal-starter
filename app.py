import streamlit as st
import pawpal_system as pawpal

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Session-state vault ───────────────────────────────────────────────────────
# Create the Owner once; every rerun reuses the same object from the vault.
if "owner" not in st.session_state:
    st.session_state.owner = pawpal.Owner(name="Jordan")

owner = st.session_state.owner  # shorthand alias
scheduler = pawpal.Scheduler(owner)

# ── Owner ─────────────────────────────────────────────────────────────────────
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

# ── Add a Pet ─────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Add a Pet")

with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add Pet"):
        # Phase-2 call: Owner.add_pet()
        owner.add_pet(pawpal.Pet(name=pet_name, species=species))
        st.success(f"Added {pet_name} the {species}!")

if owner.pets:
    st.write("Your pets:")
    for p in owner.pets:
        st.write(f"- **{p.name}** ({p.species})")

# ── Add a Task ────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet above before scheduling tasks.")
else:
    pet_names = [p.name for p in owner.pets]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_pet = st.selectbox("For pet", pet_names)
    with col2:
        task_desc = st.text_input("Task description", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])

    schedule_time = None
    use_time = st.checkbox("Schedule at a specific time")
    if use_time:
        from datetime import date, datetime, time as dt_time
        picked_time = st.time_input("Scheduled time", value=dt_time(8, 0))
        today = date.today()
        schedule_time = datetime.combine(today, picked_time)

    if st.button("Add task"):
        target_pet = next(p for p in owner.pets if p.name == selected_pet)
        if schedule_time is not None:
            new_task = pawpal.Task(
                description=task_desc,
                time_value=schedule_time,
                frequency=frequency,
            )
            new_task.time_minutes = int(duration)
        else:
            new_task = pawpal.Task(
                description=task_desc,
                time_value=int(duration),
                frequency=frequency,
            )
        # Phase-2 call: Pet.add_task()
        target_pet.add_task(new_task)
        st.success(f"Added '{task_desc}' to {selected_pet}.")

    all_tasks = scheduler.retrieve_all_tasks()
    if all_tasks:
        st.write("Current tasks")

        conflicts = scheduler.detect_time_conflicts(only_today=False)
        if conflicts:
            for warning in conflicts:
                st.warning(warning)
        else:
            st.success("No scheduling conflicts detected.")

        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            status_filter = st.selectbox("Status filter", ["All", "Pending", "Completed"])
        with filter_col2:
            pet_filter = st.selectbox("Pet filter", ["All pets", *pet_names])

        is_completed = None
        if status_filter == "Pending":
            is_completed = False
        elif status_filter == "Completed":
            is_completed = True

        filtered_tasks = scheduler.filter_tasks(
            is_completed=is_completed,
            pet_name=None if pet_filter == "All pets" else pet_filter,
        )
        sorted_tasks = scheduler.sort_by_time(tasks=filtered_tasks)

        task_owner_lookup = {}
        for pet in owner.pets:
            for task in pet.tasks:
                task_owner_lookup[id(task)] = pet.name

        if sorted_tasks:
            st.table(
                [
                    {
                        "pet": task_owner_lookup.get(id(task), "unknown"),
                        "description": task.description,
                        "scheduled": task.scheduled_for.strftime("%Y-%m-%d %I:%M %p") if task.scheduled_for else "unscheduled",
                        "duration (min)": task.time_minutes if task.time_minutes is not None else "-",
                        "frequency": task.frequency,
                        "status": "done" if task.is_completed else "pending",
                    }
                    for task in sorted_tasks
                ]
            )
        else:
            st.info("No tasks match the selected filters.")

# ── Generate Schedule ─────────────────────────────────────────────────────────
st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not owner.pets or not owner.get_all_tasks():
        st.warning("Add at least one pet and one task first.")
    else:
        for warning in scheduler.detect_time_conflicts():
            st.warning(warning)

        # Phase-2 call: Scheduler.schedule()
        result = scheduler.schedule()
        st.text(result)
