# simulation-input-validation


A Streamlit web tool to check consistency between:
- `ra_input.xlsx`: Mapping between customer locations and marker codes.
- `order_data.xlsx`: Order file with `Storage Space`.
- `map.json/.smap`: Warehouse map file with `instance-name` markers.

## Features
- Upload all 3 files from the browser.
- Get a mismatch report:
  - Missing `Storage Space` → `Location` mapping.
  - Missing `Marker Code` → map marker (`instance-name`) mapping.
- Download CSV report of issues.

## How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud
1. Fork this repo.
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud).
3. Connect your GitHub repo and deploy `app.py`.
