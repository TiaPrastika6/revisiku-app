import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(56, 189, 248, 0.16), transparent 32%),
                radial-gradient(circle at bottom right, rgba(99, 102, 241, 0.14), transparent 35%),
                linear-gradient(135deg, #080b16 0%, #0b1220 45%, #07111f 100%);
            color: #e5e7eb;
        }

        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.92);
            border-right: 1px solid rgba(148, 163, 184, 0.16);
        }

        [data-testid="stSidebar"] * {
            color: #e5e7eb;
        }

        .block-container {
            padding-top: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 1500px;
        }

        .dashboard-hero {
            display: flex;
            justify-content: space-between;
            gap: 28px;
            padding: 34px;
            border-radius: 30px;
            background:
                linear-gradient(135deg, rgba(59, 130, 246, 0.20), rgba(14, 165, 233, 0.10)),
                rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 24px 70px rgba(0, 0, 0, 0.32);
            margin-bottom: 26px;
        }

        .hero-left {
            max-width: 680px;
        }

        .app-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 13px;
            border-radius: 999px;
            background: rgba(125, 211, 252, 0.12);
            border: 1px solid rgba(125, 211, 252, 0.22);
            color: #7dd3fc;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 18px;
        }

        .hero-title {
            font-size: 52px;
            line-height: 1.05;
            font-weight: 900;
            letter-spacing: -1.8px;
            margin: 0 0 14px 0;
            color: #f8fafc;
        }

        .hero-subtitle {
            color: #a8b3c7;
            font-size: 16px;
            line-height: 1.8;
            margin-bottom: 20px;
        }

        .hero-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .chip {
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.16);
            color: #cbd5e1;
            font-size: 13px;
            font-weight: 600;
        }

        .hero-right {
            min-width: 230px;
            padding: 22px;
            border-radius: 24px;
            background: rgba(2, 6, 23, 0.40);
            border: 1px solid rgba(148, 163, 184, 0.16);
        }

        .focus-label {
            color: #94a3b8;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .focus-number {
            font-size: 48px;
            font-weight: 900;
            color: #f8fafc;
            line-height: 1;
        }

        .focus-text {
            color: #a8b3c7;
            font-size: 14px;
            line-height: 1.6;
            margin-top: 10px;
        }

        .stat-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 14px;
            margin-bottom: 24px;
        }

        .stat-card {
            padding: 20px;
            border-radius: 24px;
            background: rgba(15, 23, 42, 0.70);
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 14px 40px rgba(0, 0, 0, 0.20);
        }

        .stat-icon {
            font-size: 23px;
            margin-bottom: 12px;
        }

        .stat-label {
            color: #94a3b8;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .stat-value {
            color: #f8fafc;
            font-size: 34px;
            font-weight: 900;
            line-height: 1;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1.2fr;
            gap: 18px;
            margin-top: 10px;
        }

        .glass-card {
            padding: 24px;
            border-radius: 26px;
            background: rgba(15, 23, 42, 0.70);
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 14px 42px rgba(0, 0, 0, 0.22);
        }

        .section-heading {
            font-size: 21px;
            font-weight: 850;
            color: #f8fafc;
            margin-bottom: 14px;
        }

        .muted-text {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.7;
        }

        .progress-track {
            height: 12px;
            border-radius: 999px;
            background: rgba(148, 163, 184, 0.18);
            overflow: hidden;
            margin-top: 18px;
            margin-bottom: 12px;
        }

        .progress-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
        }

        .progress-number {
            font-size: 42px;
            font-weight: 900;
            color: #f8fafc;
            margin-top: 8px;
        }

        .task-item {
            padding: 16px;
            border-radius: 18px;
            background: rgba(2, 6, 23, 0.38);
            border: 1px solid rgba(148, 163, 184, 0.13);
            margin-bottom: 12px;
        }

        .task-title {
            font-size: 15px;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 7px;
        }

        .task-meta {
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.6;
        }

        .empty-state {
            padding: 28px;
            border-radius: 24px;
            background: rgba(14, 165, 233, 0.10);
            border: 1px dashed rgba(125, 211, 252, 0.30);
            color: #bae6fd;
            font-size: 15px;
            line-height: 1.7;
        }

        .badge {
            display: inline-block;
            padding: 7px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
            margin-right: 6px;
            margin-bottom: 8px;
        }

        .badge-blue {
            background-color: rgba(14, 165, 233, 0.18);
            color: #7dd3fc;
            border: 1px solid rgba(125, 211, 252, 0.22);
        }

        .badge-yellow {
            background-color: rgba(245, 158, 11, 0.16);
            color: #fcd34d;
            border: 1px solid rgba(252, 211, 77, 0.22);
        }

        .badge-green {
            background-color: rgba(34, 197, 94, 0.16);
            color: #86efac;
            border: 1px solid rgba(134, 239, 172, 0.22);
        }

        .badge-red {
            background-color: rgba(239, 68, 68, 0.16);
            color: #fca5a5;
            border: 1px solid rgba(252, 165, 165, 0.22);
        }

        .badge-gray {
            background-color: rgba(148, 163, 184, 0.14);
            color: #cbd5e1;
            border: 1px solid rgba(203, 213, 225, 0.18);
        }

        .soft-card {
            padding: 22px;
            border-radius: 22px;
            background: rgba(15, 23, 42, 0.74);
            border: 1px solid rgba(255,255,255,0.10);
            box-shadow: 0 12px 30px rgba(0,0,0,0.18);
            margin-bottom: 18px;
        }

        .note-title {
            font-size: 23px;
            font-weight: 800;
            margin-bottom: 10px;
            color: #f8fafc;
        }

        .note-body {
            color: #cbd5e1;
            line-height: 1.7;
            margin-top: 10px;
            margin-bottom: 12px;
        }

        .stButton > button {
            border-radius: 14px;
            font-weight: 700;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(30, 41, 59, 0.9);
            color: #f8fafc;
        }

        .stButton > button:hover {
            border-color: rgba(125, 211, 252, 0.45);
            color: #7dd3fc;
        }

        input, textarea, select {
            border-radius: 14px !important;
        }

        @media (max-width: 1100px) {
            .stat-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .dashboard-grid {
                grid-template-columns: 1fr;
            }

            .dashboard-hero {
                flex-direction: column;
            }
        }

        [data-testid="stSidebar"] {
            background: #0f172a;
        }

        [data-testid="stSidebar"] h2 {
            font-size: 24px;
            font-weight: 800;
            margin-bottom: 4px;
        }

        [data-testid="stSidebar"] .stCaption {
            color: #94a3b8;
        }

        [data-testid="stSidebar"] .stButton > button {
            background: transparent;
            border: 1px solid transparent;
            color: #e5e7eb;
            justify-content: flex-start;
            text-align: left;
            padding: 12px 14px;
            border-radius: 14px;
            font-weight: 700;
            font-size: 15px;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.22);
            color: #7dd3fc;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(148, 163, 184, 0.18);
        }
        </style>
        """,
        unsafe_allow_html=True
    )