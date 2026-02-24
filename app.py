import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config
# --- Header and Menu Hiding CSS ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)(
    page_title="Workorder Analytics", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Stunning Visuals ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated Gradient Title - Single Line with Full Visibility */
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
    
    /* Modern Card Design */
    .card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 1.8rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05), 0 8px 20px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.8rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 50px rgba(102, 126, 234, 0.15);
    }
    
    /* Metric Cards */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 20px 30px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.2;
        margin: 0.3rem 0;
        text-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    .metric-subtitle {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.8rem;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        padding: 0.6rem;
        border-radius: 60px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        color: #4a5568;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* DataFrame Styling */
    .dataframe-container {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid #e9ecef;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.02);
        overflow: auto;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* File Uploader */
    .uploadedFile {
        border: 2px dashed #667eea;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        border-radius: 60px;
        padding: 1rem 2rem;
        color: #155724;
        font-weight: 600;
        text-align: center;
        animation: slideIn 0.5s ease;
        box-shadow: 0 10px 20px rgba(132, 250, 176, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
    }
    
    @keyframes slideIn {
        from {
            transform: translateY(-20px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #6c757d;
        font-size: 1rem;
        border-top: 1px solid rgba(0, 0, 0, 0.05);
        margin-top: 2rem;
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 60px;
        font-weight: 500;
    }
    
    /* DateTime Display */
    .datetime {
        text-align: center;
        color: #4a5568;
        font-size: 1rem;
        margin: 0 auto 2rem auto;
        padding: 0.5rem 2rem;
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 60px;
        display: inline-block;
        width: auto;
    }
    
    .datetime-container {
        display: flex;
        justify-content: center;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- Helper Functions (Unchanged) ---
def is_color_lot(lot):
    lot_str = str(lot).upper()
    valid_patterns = ['HUDSON', '0X', 'CROCKERY', 'OLIVE', 'BLACK', 'BLUE', 'BEIGE', 'BIANCO', 'NERO', 'GHIACCIO', 'BOSCO', 'INDACO', 'NAVY', 'TERRACOTTA'] 
    return any(p in lot_str for p in valid_patterns)

def extract_color(lot):
    if pd.isna(lot) or '-' not in str(lot): return "N/A"
    parts = str(lot).split('-')
    return parts[1] if len(parts) >= 2 else "N/A"

# --- Data Processing (Unchanged) ---
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

    # Grid Calculations
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

    # Actual Columns Logic
    lot_pivot['Actual Material Issued'] = lot_pivot.apply(
        lambda x: (x['Material issue'] - abs(x['Material return'])) if abs(x['Material return']) > 0 else 0, axis=1
    )
    lot_pivot['Actual Completion'] = lot_pivot.apply(
        lambda x: (x['Product completion'] - abs(x['Product return'])) if abs(x['Product return']) > 0 else 0, axis=1
    )
    lot_pivot['Overall Variance'] = (lot_pivot['Material issue'] - lot_pivot['Material return'].abs()) - \
                                     (lot_pivot['Product completion'] - lot_pivot['Product return'].abs())
    
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
        issue_val = wch_sum[wch_sum['Transaction Type'] == 'Material issue']['Quantity'].sum()
        return_val = wch_sum[wch_sum['Transaction Type'] == 'Material return']['Quantity'].abs().sum()
        grand_total_wch = issue_val - return_val
        total_row_wch = pd.DataFrame({'Transaction Type': ['GRAND TOTAL'], 'Quantity': [grand_total_wch]}).fillna('')
        wch_res = pd.concat([wch_sum, total_row_wch], ignore_index=True).fillna('')
    else: wch_res = wch_sum

    return final_grid, lot_res, wch_res

# --- Header Section - Single Line Title with Full Visibility ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="gradient-title">🎯 Workorder Analytics</h1>', unsafe_allow_html=True)
    
    # Date Time Display - Centered
    current_time = datetime.now().strftime("%B %d, %Y • %I:%M %p")
    st.markdown(f'<div class="datetime-container"><div class="datetime">📅 {current_time}</div></div>', unsafe_allow_html=True)

# --- Sidebar with Enhanced UI ---
with st.sidebar:
    st.markdown("## 📂 **Data Controls**")
    st.markdown("---")
    
    # Animated File Uploader
    uploaded_file = st.file_uploader(
        "📤 **Upload Oracle XLSX**", 
        type=['xlsx'],
        help="Upload your Oracle transaction export file"
    )
    
    if uploaded_file:
        st.markdown(
            '<div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); border-radius: 60px; margin-top: 1rem;">'
            '✅ File loaded successfully!'
            '</div>',
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    st.markdown("### 📊 **Quick Actions**")
    
    # Quick action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.experimental_rerun()
    with col2:
        if st.button("📥 Export All", use_container_width=True):
            st.success("Export feature coming soon!")
    
    st.markdown("---")
    st.markdown("### ℹ️ **Information**")
    with st.expander("📌 How to use"):
        st.write("""
        1. Upload Oracle XLSX file
        2. View Color-wise totals
        3. Check Lot comparisons
        4. Monitor Chemical usage
        """)

# --- Main Content ---
if uploaded_file:
    with st.spinner("🔄 Processing your data..."):
        df_raw = pd.read_excel(uploaded_file)
        color_grid, lot_res, wch_res = process_data(df_raw)
    
    # Success Message with Animation
    st.markdown(
        '<div class="success-message">✨ Data processed successfully! View your insights below ✨</div>',
        unsafe_allow_html=True
    )
    
    # Key Metrics Section
    st.markdown("## 📈 **Key Performance Indicators**")
    
    # Calculate metrics
    total_lots = len(lot_res[lot_res['Lot Number'] != 'GRAND TOTAL']) if not lot_res.empty else 0
    total_colors = len(color_grid.columns) - 2
    total_chemicals = len(wch_res['Component or Resource'].unique()) if not wch_res.empty else 0
    total_transactions = len(df_raw)
    
    # Display metrics in modern cards - with smaller icons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">📦</div>
                <div class="metric-label">TOTAL LOTS</div>
                <div class="metric-value">{total_lots}</div>
                <div class="metric-subtitle">Active production lots</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">🎨</div>
                <div class="metric-label">ACTIVE COLORS</div>
                <div class="metric-value">{total_colors}</div>
                <div class="metric-subtitle">Different color variants</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">🧪</div>
                <div class="metric-label">CHEMICALS</div>
                <div class="metric-value">{total_chemicals}</div>
                <div class="metric-subtitle">WCH- components</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">📋</div>
                <div class="metric-label">TRANSACTIONS</div>
                <div class="metric-value">{total_transactions}</div>
                <div class="metric-subtitle">Total records processed</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Tabs with enhanced icons
    tab1, tab2, tab3 = st.tabs([
        "📊 **Color Wise Total**  •  Inventory View", 
        "🔍 **Lot Wise Comparison**  •  Detailed Analysis", 
        "🧪 **Chemicals Summary**  •  WCH Components"
    ])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Header with icons
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("🎨 Color-wise Grid View")
        with col2:
            if st.button("📥 Download Grid", key="download_grid", use_container_width=True):
                csv = color_grid.to_csv(index=False)
                st.download_button(
                    label="✅ Click to Download",
                    data=csv,
                    file_name=f"color_grid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        # Dataframe with highlighting
        def highlight_grid(r):
            if 'return' in str(r[0]).lower():
                return ['background-color: #ffebf0; color: #d32f2f'] * len(r)
            elif 'Total Actual' in str(r[0]):
                return ['background-color: #e3f2fd; font-weight: bold; color: #1976d2'] * len(r)
            return [''] * len(r)
        
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(
            color_grid.style.apply(highlight_grid, axis=1),
            use_container_width=True,
            height=400
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Color distribution info
        st.info("🎯 **Note:** Pink rows indicate return transactions, Blue rows show calculated totals")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("🔍 Lot-wise Detailed Comparison")
        with col2:
            if st.button("📥 Download Lots", key="download_lots", use_container_width=True):
                csv = lot_res.to_csv(index=False)
                st.download_button(
                    label="✅ Click to Download",
                    data=csv,
                    file_name=f"lot_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        def highlight_lot_returns(s):
            if s['Lot Number'] == 'GRAND TOTAL':
                return ['background-color: #f0f2f6; font-weight: bold; border-top: 2px solid #ddd'] * len(s)
            elif abs(s['Material return']) > 0 or abs(s['Product return']) > 0:
                return ['background-color: #ffebf0; color: #d32f2f'] * len(s)
            return [''] * len(s)
        
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(
            lot_res.style.apply(highlight_lot_returns, axis=1),
            use_container_width=True,
            height=500
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Summary stats
        total_variance = lot_res[lot_res['Lot Number'] != 'GRAND TOTAL']['Overall Variance'].sum() if not lot_res.empty else 0
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total Variance", f"{total_variance:,.0f}", 
                     delta="Net difference", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("🧪 Chemical Transaction Summary")
        with col2:
            if st.button("📥 Download Chemicals", key="download_chem", use_container_width=True):
                csv = wch_res.to_csv(index=False)
                st.download_button(
                    label="✅ Click to Download",
                    data=csv,
                    file_name=f"chemicals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        def highlight_chem(s):
            if s['Transaction Type'] == 'Material return':
                return ['background-color: #ffebf0; color: #d32f2f'] * len(s)
            elif s['Transaction Type'] == 'GRAND TOTAL':
                return ['background-color: #f0f2f6; font-weight: bold'] * len(s)
            return [''] * len(s)
        
        if not wch_res.empty:
            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            st.dataframe(
                wch_res.style.apply(highlight_chem, axis=1),
                use_container_width=True,
                height=400
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Chemical summary stats
            total_chem_issue = wch_res[wch_res['Transaction Type'] == 'Material issue']['Quantity'].sum() if 'Quantity' in wch_res.columns else 0
            total_chem_return = wch_res[wch_res['Transaction Type'] == 'Material return']['Quantity'].abs().sum() if 'Quantity' in wch_res.columns else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🧪 Total Issued", f"{total_chem_issue:,.0f}")
            with col2:
                st.metric("↩️ Total Returned", f"{total_chem_return:,.0f}", delta="-")
            with col3:
                st.metric("📊 Net Usage", f"{total_chem_issue - total_chem_return:,.0f}")
        else:
            st.warning("📭 No chemical transactions found in the data")
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Enhanced welcome screen
    st.markdown(
        """
        <div style="text-align: center; padding: 4rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 30px; margin: 2rem 0;">
            <h1 style="font-size: 5rem; margin-bottom: 1rem;">📊</h1>
            <h2 style="color: #2c3e50; font-size: 2rem; margin-bottom: 1rem;">Welcome to Workorder Analytics</h2>
            <p style="color: #34495e; font-size: 1.2rem; margin-bottom: 2rem;">Upload your Oracle transaction file to unlock powerful insights</p>
            <div style="background: rgba(255, 255, 255, 0.3); backdrop-filter: blur(10px); border-radius: 60px; padding: 1rem; max-width: 400px; margin: 0 auto;">
                <p style="color: #2c3e50; margin: 0;">👈 Click the sidebar to upload</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div style="text-align: center; padding: 2rem;">
                <h1 style="font-size: 3rem;">📊</h1>
                <h4>Color Analysis</h4>
                <p style="color: #6c757d;">Track inventory by color variants</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style="text-align: center; padding: 2rem;">
                <h1 style="font-size: 3rem;">🔍</h1>
                <h4>Lot Tracking</h4>
                <p style="color: #6c757d;">Monitor individual lot performance</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div style="text-align: center; padding: 2rem;">
                <h1 style="font-size: 3rem;">🧪</h1>
                <h4>Chemical Usage</h4>
                <p style="color: #6c757d;">Track WCH component consumption</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- Footer - Restored "Powered by Python" line + Mujahid's credit ---
st.markdown(
    """
    <div class="footer">
        <p>Powered by Python • Built with ❤️ for Oracle Analytics</p>
        <p>Developed By Mujahid Abbas 😎</p>
        <p style="font-size: 0.8rem; opacity: 0.8;">© 2024 Workorder Analytics • Version 2.0</p>
    </div>
    """,
    unsafe_allow_html=True

)
