# Connect deployment demo

This is a silly streamlit app created to demonstrate [deployment of Python apps to the Strategy Unit (SU) Connect Server](https://the-strategy-unit.github.io/data_science/presentations/2025-07-17_deploy-to-connect). It was mostly written using Gen AI.

The app is a simple game, displaying images of pets belonging to members of the SU Data Science team. Users are asked to match the pet image to the owner name.

To run it locally, you will need to add the files in the `data` folder, as demonstrated below.
Once you have the data, run the app with `streamlit run app.py` or, if you use `uv`, `uv run streamlit run app.py`

```
Project Root
├── data
|   ├── pet_owner_mapping.csv
│   └── pet_images
|       ├── pet_name1.jpg
|       └── pet_name2.jpg
├── .gitignore
├── app.py
├── pyproject.toml
├── README.md
├── requirements.txt
└── uv.lock
```
