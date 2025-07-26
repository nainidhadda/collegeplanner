import streamlit as st
import numpy as np
import pandas as pd
import json
import os

# --- Helper Functions ---
def load_data():
    if os.path.exists("planner_data.json"):
        with open("planner_data.json", "r") as f:
            return json.load(f)
    return {"finance": [], "learning": {}}

def save_data(data):
    with open("planner_data.json", "w") as f:
        json.dump(data, f)

# --- Initialize session state ---
if "data" not in st.session_state:
    st.session_state.data = load_data()

def reset_forms():
    st.session_state.pop("finance_type", None)
    st.session_state.pop("edit_finance_idx", None)
    st.session_state.pop("edit_subject", None)
    st.session_state.pop("edit_task_idx", None)

# --- SECTION 1: Intro ---
if "started" not in st.session_state:
    st.title("🎓 College Planner – Learning + Finance Tracker")
    st.markdown("""
    **Welcome!**  
    Managing your money and learning goals is key to a stress-free college life.  
    This planner helps you track savings, budgets, investments, and your study progress—all in one place!
    """)
    if st.button("Start Planning!"):
        st.session_state.started = True
    st.stop()

# --- SECTION 2: Finance Planner ---
# st.header("💰 Finance Planner")  # Remove this line

finance_types = {
    "SIP": "Systematic Investment Plan (SIP): Invest a fixed amount regularly to grow your savings.",
    "Monthly Budget": "Plan your monthly expenses and income.",
    "Savings Goal": "Set a target amount and track your progress.",
    "Stock Experiment": "Simulate stock investments and track results."
}

# --- Combined Dashboard ---
st.markdown("""
<style>
body, .main, .block-container {
    background: transparent !important;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    color: #222 !important;
}
html, body, .main, .block-container, .stApp, .stMarkdown, .stText, .stCaption, .stInfo, .stExpander, .stForm, .stTextInput, .stNumberInput, .stSelectbox, .stMultiSelect, .stCheckbox, .stExpanderHeader {
    color: #222 !important;
}
.section-header {
    font-size: 2em;
    font-weight: bold;
    margin-bottom: 0.7em;
    letter-spacing: 0.5px;
    text-shadow: 0 1px 2px #e3e3e3;
}
.stExpander, .stTextInput, .stNumberInput, .stSelectbox, .stButton, .stMultiSelect {
    border-radius: 12px !important;
}
.stExpander {
    box-shadow: none !important;
    margin-bottom: 1.2em;
    background: transparent !important;
    color: #fff !important;
    border: none !important;
}
.stForm {
    background: transparent !important;
    padding: 0.5em 0 0.5em 0;
    margin-bottom: 1em;
    box-shadow: none !important;
    color: #fff !important;
    border: none !important;
}
.stButton>button {
    background: linear-gradient(90deg, #43a047 60%, #66bb6a 100%) !important;
    color: #fff !important;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.5em 1.2em;
    margin: 0.2em 0.2em 0.2em 0;
    box-shadow: 0 1px 4px 0 rgba(67,160,71,0.08);
    transition: background 0.2s, box-shadow 0.2s;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #66bb6a 60%, #43a047 100%) !important;
    box-shadow: 0 2px 8px 0 rgba(67,160,71,0.13);
}
.stProgress>div>div {
    border-radius: 8px;
}
.stTextInput>div>input, .stNumberInput>div>input {
    border-radius: 8px !important;
    padding: 0.4em 0.8em;
    font-size: 1em;
    color: #fff !important;
    background: #222 !important;
}
.stSelectbox>div>div, .stMultiSelect>div>div {
    border-radius: 8px !important;
    color: #fff !important;
    background: #222 !important;
}
.stCheckbox>label {
    font-size: 1.08em;
    padding-left: 0.3em;
    color: #fff !important;
}
.stCheckbox>div>input:checked+label {
    color: #fff !important;
}
.stExpanderHeader {
    font-size: 1.1em;
    font-weight: 600;
    color: #fff !important;
}
.stInfo, .stCaption {
    font-size: 1.05em;
    color: #fff !important;
    background: transparent !important;
}
.stColumns {
    gap: 1.2em !important;
}
.action-btn-row {
    display: flex;
    flex-direction: row;
    gap: 1.1em;
    margin-top: 0.7em;
    margin-bottom: 0.7em;
    align-items: center;
}
.stButton>button.action-btn {
    background: #222 !important;
    color: #fff !important;
    border-radius: 50%;
    width: 2.6em;
    height: 2.6em;
    min-width: 2.6em;
    min-height: 2.6em;
    padding: 0;
    font-size: 1.3em;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: none;
    margin: 0;
    border: none;
    transition: background 0.2s;
}
.stButton>button.action-btn:hover {
    background: #444 !important;
}
</style>
""", unsafe_allow_html=True)
# Remove st.columns and use a single column layout for the dashboard:
# --- Finance Section ---
st.markdown('<div class="section-header" style="color:#fff;text-align:center;">💰 Finance</div>', unsafe_allow_html=True)
selected_types = st.multiselect(
    "Select what you want to plan:",
    options=list(finance_types.keys()),
    help="You can select more than one!"
)
for ftype in selected_types:
    st.subheader(f"Add {ftype} Plan")
    st.info(finance_types[ftype])
    form_key = f"finance_form_{ftype}"
    with st.form(form_key, clear_on_submit=True):
        if ftype == "SIP":
            name = st.text_input("Plan Name", key=f"name_{ftype}")
            amount = st.number_input("Monthly Investment (₹)", min_value=0.0, step=100.0, key=f"amount_{ftype}")
            rate = st.number_input("Expected Annual Return (%)", min_value=0.0, max_value=20.0, step=0.1, key=f"rate_{ftype}")
            years = st.number_input("Years", min_value=1, max_value=50, step=1, key=f"years_{ftype}")
        elif ftype == "Monthly Budget":
            name = st.text_input("Budget Name", key=f"name_{ftype}")
            income = st.number_input("Monthly Income (₹)", min_value=0.0, step=100.0, key=f"income_{ftype}")
            expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0, step=100.0, key=f"expenses_{ftype}")
        elif ftype == "Savings Goal":
            name = st.text_input("Goal Name", key=f"name_{ftype}")
            target = st.number_input("Target Amount (₹)", min_value=0.0, step=100.0, key=f"target_{ftype}")
            saved = st.number_input("Amount Saved So Far (₹)", min_value=0.0, step=100.0, key=f"saved_{ftype}")
        elif ftype == "Stock Experiment":
            name = st.text_input("Experiment Name", key=f"name_{ftype}")
            stock = st.text_input("Stock Name", key=f"stock_{ftype}")
            invested = st.number_input("Amount Invested (₹)", min_value=0.0, step=100.0, key=f"invested_{ftype}")
            result = st.number_input("Current Value (₹)", min_value=0.0, step=100.0, key=f"result_{ftype}")
        col1, col2 = st.columns(2)
        submit = col1.form_submit_button("Save")
        cancel = col2.form_submit_button("Cancel")
        if submit:
            entry = {"type": ftype, "name": name}
            if ftype == "SIP":
                entry.update({"amount": amount, "rate": rate, "years": years})
            elif ftype == "Monthly Budget":
                entry.update({"income": income, "expenses": expenses})
            elif ftype == "Savings Goal":
                entry.update({"target": target, "saved": saved})
            elif ftype == "Stock Experiment":
                entry.update({"stock": stock, "invested": invested, "result": result})
            if (
                st.session_state.get("finance_type") == ftype and
                st.session_state.get("edit_finance_idx") == len(st.session_state.data["finance"]) - 1
            ):
                st.session_state.data["finance"][st.session_state.edit_finance_idx] = entry
                save_data(st.session_state.data)
                st.success("Plan updated!")
                reset_forms()
                st.rerun()
            else:
                st.session_state.data["finance"].append(entry)
                save_data(st.session_state.data)
                reset_forms()
                st.success("Plan saved!")
                st.rerun()
        if cancel:
            reset_forms()
            st.rerun()

finance_list = st.session_state.data["finance"]
if finance_list:
    for idx, plan in enumerate(finance_list):
        with st.expander(f"{plan['type']}: {plan['name']}"):
            st.write(plan)
            # Progress bar for Savings Goal
            if plan['type'] == "Savings Goal":
                target = plan.get('target', 0)
                saved = plan.get('saved', 0)
                pct = (saved / target * 100) if target else 0
                st.write(f"**Progress:** {pct:.1f}% (₹{saved:,.0f} / ₹{target:,.0f})")
                st.progress(pct / 100 if target else 0)
            # SIP line chart
            if plan['type'] == "SIP":
                def sip_growth(amount, rate, years):
                    months = int(years * 12)
                    monthly_rate = rate / 12 / 100
                    values = []
                    total = 0
                    for m in range(1, months+1):
                        total = total * (1 + monthly_rate) + amount
                        values.append(total)
                    return values
                growth = sip_growth(plan['amount'], plan['rate'], plan['years'])
                df = pd.DataFrame({'Month': list(range(1, len(growth)+1)), 'Value': growth})
                st.line_chart(df.set_index('Month'))
                st.caption(f"Projected SIP Value after {plan['years']} years: ₹{growth[-1]:,.2f}")
            # Monthly Budget pie chart for categories
            if plan['type'] == "Monthly Budget":
                categories = plan.get('categories', {})
                if not categories:
                    st.info("Add budget categories below to see allocation chart.")
                else:
                    cat_df = pd.DataFrame({'Category': list(categories.keys()), 'Amount': list(categories.values())})
                    st.write("**Budget Allocation:**")
                    st.plotly_chart({
                        "data": [{
                            "labels": cat_df['Category'],
                            "values": cat_df['Amount'],
                            "type": "pie",
                            "hole": 0.3,
                        }],
                        "layout": {"showlegend": True}
                    }, use_container_width=True)
                # Add/Edit categories
                with st.form(f"cat_form_{idx}", clear_on_submit=True):
                    new_cat = st.text_input("Category Name", key=f"catname_{idx}")
                    new_amt = st.number_input("Amount (₹)", min_value=0.0, step=100.0, key=f"catamt_{idx}")
                    add_cat = st.form_submit_button("Add/Update Category")
                    if add_cat and new_cat:
                        plan.setdefault('categories', {})[new_cat] = new_amt
                        save_data(st.session_state.data)
                        st.success(f"Category '{new_cat}' updated!")
                        st.rerun()
                    # Delete category
                    if categories:
                        del_cat = st.selectbox("Delete Category", options=["-"]+list(categories.keys()), key=f"delcat_{idx}")
                        if del_cat != "-" and st.form_submit_button("Delete Selected Category"):
                            del plan['categories'][del_cat]
                            save_data(st.session_state.data)
                            st.success(f"Category '{del_cat}' deleted!")
                            st.rerun()
            # Stock Experiment bar chart
            if plan['type'] == "Stock Experiment":
                st.bar_chart(pd.DataFrame({
                    "Amount": [plan['invested'], plan['result']]
                }, index=["Invested", "Current Value"]))
            btn_cols = st.columns([1,1,1,1,8])
            with btn_cols[0]:
                if st.button("✏️", key=f"editf{idx}", help="Edit", use_container_width=True):
                    st.session_state.finance_type = plan["type"]
                    st.session_state.edit_finance_idx = idx
                    st.rerun()
            with btn_cols[1]:
                if st.button("🗑️", key=f"delf{idx}", help="Delete", use_container_width=True):
                    finance_list.pop(idx)
                    save_data(st.session_state.data)
                    st.success("Deleted!")
                    st.rerun()
            with btn_cols[2]:
                if st.button("⬆️", key=f"upf{idx}", help="Move Up", use_container_width=True) and idx > 0:
                    finance_list[idx-1], finance_list[idx] = finance_list[idx], finance_list[idx-1]
                    save_data(st.session_state.data)
                    st.rerun()
            with btn_cols[3]:
                if st.button("⬇️", key=f"downf{idx}", help="Move Down", use_container_width=True) and idx < len(finance_list)-1:
                    finance_list[idx+1], finance_list[idx] = finance_list[idx], finance_list[idx+1]
                    save_data(st.session_state.data)
                    st.rerun()
else:
    st.markdown("""
    <div style='text-align:center; margin-top:2em; margin-bottom:2em;'>
        <div style='font-size:3em;'>💡</div>
        <div style='font-size:1.1em; color:#fff; margin-top:0.5em;'>No finance plans yet.<br>Start planning your financial future today!</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('<hr style="border:1px solid #fff; margin:2em 0;">', unsafe_allow_html=True)
# --- Learning Section ---
st.markdown('<div class="section-header" style="color:#fff;text-align:center;">📚 Learning</div>', unsafe_allow_html=True)
# --- Daily Goals ---
st.markdown('<div style="margin-bottom:1em;"><b style="color:#fff;">🌞 Daily Goals</b></div>', unsafe_allow_html=True)
if "daily_goals" not in st.session_state:
    st.session_state["daily_goals"] = []
with st.form("add_daily_goal", clear_on_submit=True):
    new_goal = st.text_input("Add Daily Goal")
    add_goal = st.form_submit_button("Add Goal")
    if add_goal and new_goal:
        st.session_state["daily_goals"].append({"goal": new_goal, "done": False})
        save_data(st.session_state.data)
        st.success("Goal added!")
        st.rerun()
# Checklist for daily goals
done_count = 0
for idx, g in enumerate(st.session_state["daily_goals"]):
    cols = st.columns([8,1])
    checked = g["done"]
    new_checked = cols[0].checkbox(g["goal"], value=checked, key=f"chk_daily_{idx}")
    if new_checked != checked:
        st.session_state["daily_goals"][idx]["done"] = new_checked
        save_data(st.session_state.data)
        st.rerun()
    if cols[1].button("🗑️", key=f"del_daily_{idx}"):
        st.session_state["daily_goals"].pop(idx)
        save_data(st.session_state.data)
        st.rerun()
    if new_checked:
        done_count += 1
total_goals = len(st.session_state["daily_goals"])
st.progress(done_count / total_goals if total_goals > 0 else 0)
st.markdown(f'<span style="color:#fff;font-size:1.05em;">{done_count} of {total_goals} daily goals completed</span>', unsafe_allow_html=True)
st.markdown('<hr style="border:1px solid #e65100; margin:1.5em 0;">', unsafe_allow_html=True)
# Add Subject
with st.form("add_subject", clear_on_submit=True):
    subject = st.text_input("Add New Subject")
    add_sub = st.form_submit_button("Add Subject")
    if add_sub and subject:
        if subject not in st.session_state.data["learning"]:
            st.session_state.data["learning"][subject] = []
            save_data(st.session_state.data)
            st.success(f"Added subject: {subject}")
            st.rerun()
        else:
            st.warning("Subject already exists.")
# List Subjects and Tasks
subjects = list(st.session_state.data["learning"].keys())
for idx, subject in enumerate(subjects):
    tasks = st.session_state.data["learning"][subject]
    with st.expander(f"Subject: {subject}"):
        # --- Progress Calculation ---
        total_tasks = len(tasks)
        done_tasks = sum(1 for t in tasks if t["status"] == "Done")
        progress_pct = (done_tasks / total_tasks * 100) if total_tasks > 0 else 0
        st.write(f"**Progress:** {progress_pct:.1f}% ({done_tasks}/{total_tasks} tasks done)")
        st.progress(progress_pct / 100 if total_tasks > 0 else 0)
        # --- Status Distribution Chart ---
        if total_tasks > 0:
            status_counts = {s: 0 for s in ["ToDo", "In Progress", "Done"]}
            for t in tasks:
                status_counts[t["status"]] += 1
            status_df = pd.DataFrame({"Status": list(status_counts.keys()), "Count": list(status_counts.values())})
            st.write("**Task Status Distribution:**")
            st.plotly_chart(
                {
                    "data": [
                        {
                            "labels": status_df["Status"],
                            "values": status_df["Count"],
                            "type": "pie",
                            "hole": 0.3,
                        }
                    ],
                    "layout": {"showlegend": True}
                },
                use_container_width=True
            )
        # --- Bulk Add Tasks ---
        with st.form(f"bulk_add_{subject}", clear_on_submit=True):
            bulk_tasks = st.text_area("Add multiple tasks (one per line)")
            add_bulk = st.form_submit_button("Add Tasks")
            if add_bulk and bulk_tasks.strip():
                new_tasks = [line.strip() for line in bulk_tasks.splitlines() if line.strip()]
                st.session_state.data["learning"][subject].extend({"task": t, "status": "ToDo"} for t in new_tasks)
                save_data(st.session_state.data)
                st.success(f"Added {len(new_tasks)} tasks!")
                st.rerun()
        # --- Checklist for Tasks ---
        for tidx, t in enumerate(tasks):
            checked = t["status"] == "Done"
            cols = st.columns([10,1])
            with cols[0]:
                new_checked = st.checkbox(t["task"], value=checked, key=f"chk_{subject}_{tidx}")
                if new_checked != checked:
                    st.session_state.data["learning"][subject][tidx]["status"] = "Done" if new_checked else "ToDo"
                    save_data(st.session_state.data)
                    st.rerun()
            with cols[1]:
                if st.button("🗑️", key=f"deltask{subject}{tidx}"):
                    st.session_state.data["learning"][subject].pop(tidx)
                    save_data(st.session_state.data)
                    st.rerun()
        # Reorder subjects
        btn_cols = st.columns([1,1,1,1,8])
        with btn_cols[0]:
            if st.button("🗑️", key=f"delsub{subject}", help="Delete Subject", use_container_width=True):
                st.session_state.data["learning"].pop(subject)
                save_data(st.session_state.data)
                st.success("Subject deleted!")
                st.rerun()
        with btn_cols[1]:
            if st.button("⬆️", key=f"upsub{idx}", help="Move Up", use_container_width=True) and idx > 0:
                subjects[idx-1], subjects[idx] = subjects[idx], subjects[idx-1]
                st.session_state.data["learning"] = {k: st.session_state.data["learning"][k] for k in subjects}
                save_data(st.session_state.data)
                st.rerun()
        with btn_cols[2]:
            if st.button("⬇️", key=f"downsub{idx}", help="Move Down", use_container_width=True) and idx < len(subjects)-1:
                subjects[idx+1], subjects[idx] = subjects[idx], subjects[idx+1]
                st.session_state.data["learning"] = {k: st.session_state.data["learning"][k] for k in subjects}
                save_data(st.session_state.data)
                st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
# Remove Streamlit's default divider and caption, add a custom footer
st.markdown("""
<style>
.custom-footer {
    background: rgba(255,255,255,0.0);
    color: #888;
    text-align: center;
    font-size: 1em;
    margin-top: 2em;
    margin-bottom: 0.5em;
    padding: 0.5em 0 0.2em 0;
}
</style>
<div class="custom-footer">
    Made with ❤️ using Streamlit. Your data is saved locally in this folder.
</div>
""", unsafe_allow_html=True) 