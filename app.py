import streamlit as st
from PIL import Image
import pandas as pd
import os
import random

# --- Config ---
PET_IMAGE_DIR = "data/pet_images"
MAPPING_CSV = "data/pet_owner_mapping.csv"

st.set_page_config(page_title="Guess the Owner Game", layout="wide")
st.title("Guess the DS Team Pet Owner Game")

# --- Load mapping ---
try:
    mapping_df = pd.read_csv(MAPPING_CSV)
except FileNotFoundError:
    st.error(f"Mapping file `{MAPPING_CSV}` not found.")
    st.stop()

# --- Extract pet filenames and owner names ---
pet_data = mapping_df.to_dict(
    orient="records"
)  # List of dicts: [{pet_image, owner_name}, ...]
owner_names = sorted(mapping_df["owner_name"].unique().tolist())

# --- Shuffle pet images once per session ---
if "shuffled_pets" not in st.session_state:
    st.session_state.shuffled_pets = random.sample(pet_data, len(pet_data))
    st.session_state.guesses = {}

st.subheader("🕵️ Match each pet to the correct owner!")

# --- Guessing form ---
with st.form("guess_form"):
    for idx, item in enumerate(st.session_state.shuffled_pets):
        pet_image_path = os.path.join(PET_IMAGE_DIR, item["pet_image"])
        image = Image.open(pet_image_path).resize((150, 150))
        pet_name = item["pet_image"].split(".")[0].capitalize()

        cols = st.columns([1, 3])
        with cols[0]:
            st.image(image, caption=f"{pet_name}", use_container_width=False)
        with cols[1]:
            guess = st.selectbox(
                f"Who is the owner of Pet #{idx+1}?", owner_names, key=f"guess_{idx}"
            )
            st.session_state.guesses[idx] = guess

    submitted = st.form_submit_button("Submit Answers")

# --- Show results ---
if submitted:
    st.subheader("📊 Results")

    score = 0
    for idx, item in enumerate(st.session_state.shuffled_pets):
        true_owner = item["owner_name"]
        guess = st.session_state.guesses[idx]

        cols = st.columns([1, 2])
        with cols[0]:
            img_path = os.path.join(PET_IMAGE_DIR, item["pet_image"])
            st.image(Image.open(img_path).resize((150, 150)), use_container_width=False)
        with cols[1]:
            if guess == true_owner:
                st.success(
                    f"✅ Correct! You guessed **{guess}**, and the real owner is **{true_owner}**."
                )
                score += 1
            else:
                st.error(
                    f"❌ Incorrect. You guessed **{guess}**, but the real owner is **{true_owner}**."
                )

    st.markdown(f"### 🎉 Your Score: **{score} / {len(pet_data)}**")

    # Optional: reset option
    if st.button("🔁 Play Again"):
        del st.session_state["shuffled_pets"]
        del st.session_state["guesses"]
        st.experimental_rerun()
