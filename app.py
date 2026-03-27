import streamlit as st
import pawpal_system as pawpal

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Session-state vault ───────────────────────────────────────────────────────
# Create the Owner once; every rerun reuses the same object from the vault.
if "owner" not in st.session_state:
    st.session_state.owner = pawpal.Owner(name="Jordan")

owner = st.session_state.owner  # shorthand alias

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

    if st.button("Add task"):
        target_pet = next(p for p in owner.pets if p.name == selected_pet)
        new_task = pawpal.Task(
            description=task_desc,
            time_value=int(duration),
            frequency=frequency,
        )
        # Phase-2 call: Pet.add_task()
        target_pet.add_task(new_task)
        st.success(f"Added '{task_desc}' to {selected_pet}.")

    # Show all tasks grouped by pet
    tasks_by_pet = pawpal.Scheduler(owner).get_tasks_by_pet()
    if any(tasks_by_pet.values()):
        st.write("Current tasks:")
        for p_name, tasks in tasks_by_pet.items():
            if tasks:
                st.markdown(f"**{p_name}**")
                st.table(
                    [
                        {
                            "description": t.description,
                            "duration (min)": t.time_minutes,
                            "frequency": t.frequency,
                            "status": "done" if t.is_completed else "pending",
                        }
                        for t in tasks
                    ]
                )

# ── Generate Schedule ─────────────────────────────────────────────────────────
st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not owner.pets or not owner.get_all_tasks():
        st.warning("Add at least one pet and one task first.")
    else:
        # Phase-2 call: Scheduler.schedule()
        result = pawpal.Scheduler(owner).schedule()
        st.text(result)
