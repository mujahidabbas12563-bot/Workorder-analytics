import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# --- 1. PAGE CONFIGURATION (Must be at the very top) ---
st.set_page_config(
    page_title="Workorder Analytics", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. HIDE HEADER & MENU CSS ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        /* Hide the decoration line at the top */
        .st-emotion-cache-zq59db {display:none !important;}
    </style>
""", unsafe_allow_html=True)

# --- 3. PASSWORD PROTECTION LOGIC ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center;'>🔐 Secure Access</h2>", unsafe_allow_html=True)
            pwd = st.text_input("Enter Dashboard Password:", type="password")
            if st.button("Login", use_container_width=True):
                if pwd == "mujahid786":  # <--- Aapna password yahan change kar sakte hain
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect Password!")
        return False
    return True

# --- ONLY RUN THE REST OF THE CODE IF AUTHENTICATED ---
if check_password():
    # --- Custom CSS for Stunning Visuals (Aapka original CSS) ---
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            font-family: 'Inter', sans-serif;
        }
        .gradient-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff6b6b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% 200%;
            animation: gradientShift 5s ease infinite;
            font-size: 3.2rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 1rem;
            white-space: nowrap;
            width: 100%;
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 1.8rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.8rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 20px 30px rgba(102, 126, 234, 0.3);
            color: white;
        }
        .footer {
            text-align: center;
            padding: 1.5rem;
            color: #6c757d;
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(10px);
            border-radius: 60px;
            margin-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Helper Functions (Aapka original logic) ---
    def is_color_lot(lot):
        lot_str = str(lot).upper()
        valid_patterns = ['HUDSON', '0X', 'CROCKERY', 'OLIVE', 'BLACK', 'BLUE', 'BEIGE', 'BIANCO', 'NERO', 'GHIACCIO', 'BOSCO', 'INDACO', 'NAVY', 'TERRACOTTA'] 
        return any(p in lot_str for p in valid_patterns)

    def extract_color(lot):
        if pd.isna(lot) or '-' not in str(lot): return "N/A"
        parts = str(lot).split('-')
        return parts[1] if len(parts) >= 2 else "N/A"

    def process_data(df):
        # ... (Aapka pura processing logic yahan continue hota hai)
        df.columns = df.columns.str.strip()
        df['Transaction Type'] = df['Transaction Type'].str.strip()
        df['color'] = df['Lot Number'].apply(extract_color)
        
        target_trans = ['Material issue', 'Material return', 'Product completion', 'Product return']
        color_lots_df = df[df['Lot Number'].apply(is_color_lot)].copy()

        # Grid Logic
        grid_pivot = color_lots_df[color_lots_df['Transaction Type'].isin(target_trans)].pivot_table(
            index=['Transaction Type'], columns='color', values='Quantity', aggfunc='sum'
        ).fillna(0)
        for trans in target_trans:
            if trans not in grid_pivot.index: grid_pivot.loc[trans] = 0
        grid_pivot = grid_pivot.reindex(target_trans)

        actual_issued_grid = grid_pivot.loc['Material issue'] - grid_pivot.loc['Material return'].abs()
        actual_comp_grid = grid_pivot.loc['Product completion'] - grid_pivot.loc['Product return'].abs()

        final_grid = pd.concat([grid_pivot, pd.DataFrame([actual_issued_grid, actual_comp_grid], 
                               index=['Total Actual Material Issued', 'Total Actual Completion'])])
        final_grid['Grand Total'] = final_grid.sum(axis=1)
        final_grid = final_grid.round(0).astype(int).reset_index()

        # Lot Logic
        lot_pivot = color_lots_df[color_lots_df['Transaction Type'].isin(target_trans)].pivot_table(
            index='Lot Number', columns='Transaction Type', values='Quantity', aggfunc='sum'
        ).fillna(0)
        for col in target_trans:
            if col not in lot_pivot.columns: lot_pivot[col] = 0
        
        lot_pivot['Actual Material Issued'] = lot_pivot['Material issue'] - lot_pivot['Material return'].abs()
        lot_pivot['Actual Completion'] = lot_pivot['Product completion'] - lot_pivot['Product return'].abs()
        lot_pivot['Overall Variance'] = lot_pivot['Actual Material Issued'] - lot_pivot['Actual Completion']
        lot_res = lot_pivot.round(0).astype(int).reset_index()

        # Chemical Logic
        mask_wch = (df['Component or Resource'].str.startswith('WCH-', na=False))
        wch_res = df[mask_wch].groupby(['Transaction Type', 'Component or Resource', 'UOM'])['Quantity'].sum().reset_index()
        
        return final_grid, lot_res, wch_res

    # --- Header Section ---
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown('<h1 class="gradient-title">🎯 Workorder Analytics</h1>', unsafe_allow_html=True)
        current_time = datetime.now().strftime("%B %d, %Y • %I:%M %p")
        st.markdown(f'<div style="text-align:center;">📅 {current_time}</div>', unsafe_allow_html=True)

    # --- Sidebar ---
    with st.sidebar:
        st.markdown("## 📂 **Data Controls**")
        st.markdown("---")
        uploaded_file = st.file_uploader("📤 **Upload Oracle XLSX**", type=['xlsx'])
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

    # --- Main Content (Aapka pura 600 line ka logic idhar chalega) ---
    if uploaded_file:
        with st.spinner("Processing..."):
            df_raw = pd.read_excel(uploaded_file)
            color_grid, lot_res, wch_res = process_data(df_raw)
            
            # (Metric Cards and Tabs go here - exactly like your old code)
            st.success("✨ Data processed successfully!")
            
            t1, t2, t3 = st.tabs(["📊 Color Grid", "🔍 Lot Detail", "🧪 Chemicals"])
            with t1:
                st.dataframe(color_grid, use_container_width=True)
            with t2:
                st.dataframe(lot_res, use_container_width=True)
            with t3:
                st.dataframe(wch_res, use_container_width=True)
    else:
        # Welcome screen for Mujahid
        st.info("👋 Welcome Mujahid! Please upload your Excel file to start.")

    # --- Footer ---
    st.markdown(f"""
    <div class="footer">
        <p>Developed By Mujahid Abbas 😎 • © {datetime.now().year}</p>
    </div>
    """, unsafe_allow_html=True)
