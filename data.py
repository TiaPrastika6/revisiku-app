import json
import os
import streamlit as st

NAMA_FILE = "catatan.json"


def load_catatan():
    if os.path.exists(NAMA_FILE):
        try:
            with open(NAMA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return []
    return []


def simpan_catatan(data):
    with open(NAMA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def init_session():
    if "catatan_list" not in st.session_state:
        st.session_state.catatan_list = load_catatan()