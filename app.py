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

# --- 2. HIDE HEADER, MENU & DEPLOY BUTTON ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        /* Hide the decoration line at the top */
        div[data-testid="stDecoration"] {display:none !important;}
    </style>
""", unsafe_allow_html=True)

# --- 3. PASSWORD PROTECTION LOGIC ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if not st.session_state.authenticated:
        # UI for Login Page
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.markdown("""
                <div style="background: white; padding: 2rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center;">
                    <h2 style="color: #4a5568;">🔐 Dashboard Access</h2>
                    <p style="color: #718096;">Please enter password to continue</p>
                </div>
            """, unsafe_allow_html=True)
            
            pwd = st.text_input("Password", type="password", placeholder="Enter Password")
            if st.button("Unlock Dashboard", use_container_width=True):
                if pwd == "mujahid786":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect Password!")
        return False
    return True

# --- ONLY RUN THE REST OF THE CODE IF AUTHENTICATED ---
if check_password():

    # --- Custom CSS for Stunning Visuals (AAP KA ORIGINAL CSS) ---
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
            letter-spacing: -1px;
            margin-bottom: 1rem;
            text-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
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
            transition: transform 0.3s ease;
        }
        .metric-card:hover { transform: translateY(-5px); }
        .metric-value { font-size: 2rem; font-weight: 700; }
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            background: rgba(255, 255, 255, 0.7);
            padding: 0.6rem;
            border-radius: 60px;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border-radius: 50px;
        }
        .footer {
            text-align: center;
            padding: 1.5rem;
            color: #6c757d;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 60px;
            margin-top: 2rem;
        }
        .datetime {
            text-align: center;
            color: #4a5568;
            padding: 0.5rem 2rem;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 60px;
            display: inline-block;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Helper Functions (AAP KA ORIGINAL) ---
    def is_color_lot(lot):
        lot_str = str(lot).upper()
        valid_patterns = ['HUDSON', '0X', 'CROCKERY', 'OLIVE', 'BLACK', 'BLUE', 'BEIGE', 'BIANCO', 'NERO', 'GHIACCIO', 'BOSCO', 'INDACO', 'NAVY', 'TERRACOTTA'] 
        return any(p in lot_str for p in valid_patterns)

    def extract_color(lot):
        if pd.isna(lot) or '-' not in str(lot): return "N/A"
        parts = str(lot).split('-')
        return parts[1] if len(parts) >= 2 else "N/A"

    # --- Data Processing (AAP KA ORIGINAL) ---
    def process_data(df):
        df.columns = df.columns.str.strip()
        df['Transaction Type'] = df['Transaction Type'].str.strip()
        df['color'] = df['Lot Number'].apply(extract_color)
        
        target_trans = ['Material issue', 'Material return', 'Product completion', 'Product return']
        color_lots_df = df[df['Lot Number'].apply(is_color_lot)].copy()

        # 1. COLOR WISE TOTAL (GRID)
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

        # 2. LOT WISE COMPARISON
        lot_pivot = color_lots_df[color_lots_df['Transaction Type'].isin(target_trans)].pivot_table(
            index='Lot Number', columns='Transaction Type', values='Quantity', aggfunc='sum'
        ).fillna(0)

        for col in target_trans:
            if col not in lot_pivot.columns: lot_pivot[col] = 0

        lot_pivot['Actual Material Issued'] = lot_pivot['Material issue'] - lot_pivot['Material return'].abs()
        lot_pivot['Actual Completion'] = lot_pivot['Product completion'] - lot_pivot['Product return'].abs()
        lot_pivot['Overall Variance'] = lot_pivot['Actual Material Issued'] - lot_pivot['Actual Completion']
        
        cols_order = ['Material issue', 'Material return', 'Actual Material Issued', 
                      'Product completion', 'Product return', 'Actual Completion', 'Overall Variance']
        lot_res = lot_pivot[cols_order].round(0).astype(int).reset_index()

        if not lot_res.empty:
            sums = lot_res.drop(columns='Lot Number').sum()
            total_row = pd.DataFrame([['GRAND TOTAL'] + sums.tolist()], columns=lot_res.columns)
            lot_res = pd.concat([lot_res, total_row], ignore_index=True)

        # 3. CHEMICALS
        mask_wch = (df['Component or Resource'].str.startswith('WCH-', na=False))
        wch_sum = df[mask_wch].groupby(['Transaction Type', 'Component or Resource', 'UOM', 'Subinventory', 'Locator'])['Quantity'].sum().reset_index()
        if not wch_sum.empty:
            grand_total_wch = wch_sum[wch_sum['Transaction Type'] == 'Material issue']['Quantity'].sum() - wch_sum[wch_sum['Transaction Type'] == 'Material return']['Quantity'].abs().sum()
            wch_res = pd.concat([wch_sum, pd.DataFrame({'Transaction Type': ['GRAND TOTAL'], 'Quantity': [grand_total_wch]})], ignore_index=True).fillna('')
        else: wch_res = wch_sum

        return final_grid, lot_res, wch_res

    # --- Header Section ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="gradient-title">🎯 Workorder Analytics</h1>', unsafe_allow_html=True)
        current_time = datetime.now().strftime("%B %d, %Y • %I:%M %p")
        st.markdown(f'<div style="text-align:center;"><div class="datetime">📅 {current_time}</div></div>', unsafe_allow_html=True)

    # --- Sidebar ---
    with st.sidebar:
        st.markdown("## 📂 **Data Controls**")
        st.markdown("---")
        uploaded_file = st.file_uploader("📤 **Upload Oracle XLSX**", type=['xlsx'])
        
        if uploaded_file:
            st.success("✅ File loaded!")
        
        st.markdown("---")
        if st.sidebar.button("🔓 Logout"):
            st.session_state.authenticated = False
            st.rerun()

    # --- Main Content ---
    if uploaded_file:
        with st.spinner("🔄 Processing..."):
            df_raw = pd.read_excel(uploaded_file)
            color_grid, lot_res, wch_res = process_data(df_raw)
        
        st.markdown('<div class="success-message" style="text-align:center; background:#84fab0; padding:10px; border-radius:50px; margin-bottom:20px;">✨ Insights Ready!</div>', unsafe_allow_html=True)
        
        # Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f'<div class="metric-card">📦<br><div class="metric-label">TOTAL LOTS</div><div class="metric-value">{len(lot_res)-1}</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card">🎨<br><div class="metric-label">COLORS</div><div class="metric-value">{len(color_grid.columns)-2}</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card">🧪<br><div class="metric-label">CHEMICALS</div><div class="metric-value">{len(wch_res)-1 if not wch_res.empty else 0}</div></div>', unsafe_allow_html=True)
        m4.markdown(f'<div class="metric-card">📋<br><div class="metric-label">RECORDS</div><div class="metric-value">{len(df_raw)}</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["📊 Color Grid", "🔍 Lot Detail", "🧪 Chemicals"])

        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🎨 Color-wise Grid View")
            st.dataframe(color_grid, use_container_width=True, height=400)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🔍 Lot-wise Comparison")
            st.dataframe(lot_res, use_container_width=True, height=500)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🧪 Chemical Usage")
            st.dataframe(wch_res, use_container_width=True, height=400)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div style="text-align: center; padding: 4rem; background: rgba(255,255,255,0.5); border-radius: 30px;"><h1>📊</h1><h2>Welcome Mujahid!</h2><p>Upload your Oracle file to start.</p></div>', unsafe_allow_html=True)

    # --- Footer ---
    st.markdown(f"""
        <div class="footer">
            <p>Powered by Python • Developed By Mujahid Abbas 😎</p>
            <p style="font-size: 0.8rem;">© {datetime.now().year} Workorder Analytics</p>
        </div>
    """, unsafe_allow_html=True)
