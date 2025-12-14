import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:5001"

st.set_page_config(page_title="Prompt & Experiment Tracker", layout="wide")
st.title("🧠 Prompt & Experiment Tracker")

tab_prompts, tab_experiments, tab_analytics = st.tabs(["Prompts", "Experiments", "Analytics"])


# ---------- Prompts tab ----------
with tab_prompts:
    st.subheader("Create new prompt")

    with st.form("create_prompt"):
        title = st.text_input("Title")
        task_type = st.text_input("Task type (e.g. summarization, coding assistant)")
        tags = st.text_input("Tags (comma separated, e.g. 'python,debugging')")
        prompt_text = st.text_area("Prompt text", height=200)
        submitted = st.form_submit_button("Save prompt")

    if submitted:
        payload = {
            "title": title,
            "task_type": task_type,
            "tags": tags,
            "prompt_text": prompt_text,
        }
        r = requests.post(f"{API_BASE}/api/prompts", json=payload)
        if r.ok:
            st.success(r.json())
        else:
            st.error(f"Error: {r.status_code}")
            st.text(r.text)

    st.markdown("---")
    st.subheader("Existing prompts")

    r = requests.get(f"{API_BASE}/api/prompts")
    if r.ok:
        prompts = r.json()
        if prompts:
            df = pd.DataFrame(prompts)
            st.dataframe(df[["id", "title", "task_type", "tags", "created_at"]])
        else:
            st.info("No prompts yet.")
    else:
        st.error("Failed to load prompts")


# ---------- Experiments tab ----------
with tab_experiments:
    st.subheader("Log new experiment")

    # Load prompts for selection
    pr = requests.get(f"{API_BASE}/api/prompts")
    prompt_options = pr.json() if pr.ok else []

    if not prompt_options:
        st.warning("Create a prompt first in the Prompts tab.")
    else:
        prompt_map = {f"{p['id']} - {p['title']}": p["id"] for p in prompt_options}
        with st.form("create_experiment"):
            selected_prompt = st.selectbox("Prompt", list(prompt_map.keys()))
            model_name = st.text_input("Model name (e.g. gpt-4o, llama-3)")
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
            max_tokens = st.number_input("Max tokens", min_value=1, value=512)
            rating = st.slider("Your rating (1–5)", 1, 5, 4)
            notes = st.text_area("Notes (what worked / failed)")
            submitted_exp = st.form_submit_button("Log experiment")

        if submitted_exp:
            payload = {
                "prompt_id": prompt_map[selected_prompt],
                "model_name": model_name,
                "temperature": float(temperature),
                "max_tokens": int(max_tokens),
                "rating": int(rating),
                "notes": notes,
            }
            r = requests.post(f"{API_BASE}/api/experiments", json=payload)
            if r.ok:
                st.success(r.json())
            else:
                st.error(f"Error: {r.status_code}")
                st.text(r.text)

    st.markdown("---")
    st.subheader("Experiment history")

    er = requests.get(f"{API_BASE}/api/experiments")
    if er.ok:
        exps = er.json()
        if exps:
            df = pd.DataFrame(exps)
            st.dataframe(df[["id", "prompt_id", "model_name", "rating", "created_at"]])
        else:
            st.info("No experiments yet.")
    else:
        st.error("Failed to load experiments")


# ---------- Analytics tab ----------
with tab_analytics:
    st.subheader("Analytics")

    er = requests.get(f"{API_BASE}/api/experiments")
    pr = requests.get(f"{API_BASE}/api/prompts")

    if not (er.ok and pr.ok):
        st.error("Failed to load data")
    else:
        exps = pd.DataFrame(er.json())
        prompts = pd.DataFrame(pr.json())

        if exps.empty:
            st.info("No experiments yet.")
        else:
            # Join to show prompt titles
            if not prompts.empty:
                exps = exps.merge(prompts[["id", "title"]], left_on="prompt_id", right_on="id", suffixes=("", "_prompt"))

            st.write("Average rating by model")
            model_group = exps.groupby("model_name")["rating"].mean().reset_index()
            st.bar_chart(model_group.set_index("model_name"))

            if "title" in exps.columns:
                st.write("Average rating by prompt")
                prompt_group = exps.groupby("title")["rating"].mean().reset_index()
                st.bar_chart(prompt_group.set_index("title"))
