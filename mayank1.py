import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="💰 Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for CU Red & White Theme
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
        color: white;
        border-radius: 12px;
        height: 55px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(220, 20, 60, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #FF1744 0%, #DC143C 100%);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(220, 20, 60, 0.4);
    }
    .metric-card {
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(220, 20, 60, 0.3);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(220, 20, 60, 0.4);
    }
    .expense-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin: 12px 0;
        box-shadow: 0 4px 12px rgba(220, 20, 60, 0.15);
        border-left: 6px solid #DC143C;
        transition: all 0.3s ease;
    }
    .expense-card:hover {
        transform: translateX(10px);
        box-shadow: 0 6px 20px rgba(220, 20, 60, 0.25);
    }
    .add-expense-section {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(220, 20, 60, 0.2);
        border: 3px solid #DC143C;
        margin-bottom: 30px;
    }
    h1 {
        color: #DC143C;
        text-align: center;
        font-size: 3.5em;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    h2 {
        color: #DC143C;
    }
    h3 {
        color: #8B0000;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border: 2px solid #DC143C;
        color: #DC143C;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
        color: white;
    }
    .stTextInput>div>div>input {
        border: 2px solid #DC143C;
        border-radius: 10px;
        padding: 12px;
    }
    .stNumberInput>div>div>input {
        border: 2px solid #DC143C;
        border-radius: 10px;
        padding: 12px;
    }
    .stSelectbox>div>div>div {
        border: 2px solid #DC143C;
        border-radius: 10px;
    }
    .stDateInput>div>div>input {
        border: 2px solid #DC143C;
        border-radius: 10px;
        padding: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Title
st.markdown("<h1>💰 Smart Expense Tracker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #DC143C; font-size: 1.3em; margin-top: -15px;'>🎓 Chandigarh University Theme Edition</p>", unsafe_allow_html=True)
st.markdown("---")

# Add Expense Section on Main Page
st.markdown("<div class='add-expense-section'>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #DC143C; margin-bottom: 25px;'>➕ Add New Expense</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

with col1:
    expense_name = st.text_input("📝 Expense Name", placeholder="e.g., Groceries, Fuel, Movie", key="expense_name")

with col2:
    expense_amount = st.number_input("💵 Amount (₹)", min_value=0.0, step=10.0, format="%.2f", key="expense_amount")

with col3:
    expense_category = st.selectbox("🏷️ Category", 
        ["🍔 Food", "🚗 Transport", "🛍️ Shopping", "💊 Health", 
         "🎬 Entertainment", "📚 Education", "🏠 Bills", "💼 Other"], key="expense_category")

with col4:
    expense_date = st.date_input("📅 Date", datetime.now(), key="expense_date")

col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
with col_btn2:
    if st.button("✅ ADD EXPENSE", key="add_btn"):
        if expense_name and expense_amount > 0:
            st.session_state.expenses.append({
                "name": expense_name,
                "amount": expense_amount,
                "category": expense_category,
                "date": expense_date.strftime("%Y-%m-%d")
            })
            st.success(f"✅ Added {expense_name} - ₹{expense_amount:.2f}")
            st.rerun()
        else:
            st.error("⚠️ Please enter valid expense details!")

st.markdown("</div>", unsafe_allow_html=True)

# Main content area
if not st.session_state.expenses:
    st.markdown("""
        <div style='text-align: center; padding: 50px; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(220, 20, 60, 0.1);'>
            <h2 style='color: #DC143C;'>👋 Welcome to Your Expense Tracker!</h2>
            <p style='font-size: 1.2em; color: #666;'>Start by adding your first expense using the form above.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    # Calculate total and statistics
    total_expenses = sum(exp['amount'] for exp in st.session_state.expenses)
    num_expenses = len(st.session_state.expenses)
    avg_expense = total_expenses / num_expenses if num_expenses > 0 else 0
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin:0; font-size: 1.2em;">💰 Total Spent</h3>
                <h2 style="margin:15px 0; font-size: 2.5em;">₹{total_expenses:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #FF1744 0%, #DC143C 100%);">
                <h3 style="margin:0; font-size: 1.2em;">📊 Total Expenses</h3>
                <h2 style="margin:15px 0; font-size: 2.5em;">{num_expenses}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #C41E3A 0%, #8B0000 100%);">
                <h3 style="margin:0; font-size: 1.2em;">📈 Average</h3>
                <h2 style="margin:15px 0; font-size: 2.5em;">₹{avg_expense:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 All Expenses", "📊 Analytics", "🗑️ Manage"])
    
    with tab1:
        st.subheader("📋 Your Expenses")
        
        # Create DataFrame
        df = pd.DataFrame(st.session_state.expenses)
        df['amount'] = df['amount'].apply(lambda x: f"₹{x:,.2f}")
        df.index = range(1, len(df) + 1)
        
        # Display as styled table
        st.dataframe(
            df,
            use_container_width=True,
            height=400
        )
    
    with tab2:
        st.subheader("📊 Expense Analytics")
        
        # Create DataFrame for charts
        df_chart = pd.DataFrame(st.session_state.expenses)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart for category distribution
            category_sum = df_chart.groupby('category')['amount'].sum().reset_index()
            fig_pie = px.pie(
                category_sum, 
                values='amount', 
                names='category',
                title='💰 Expenses by Category',
                hole=0.4,
                color_discrete_sequence=['#DC143C', '#FF1744', '#C41E3A', '#8B0000', '#FF6B6B', '#EE4B4B', '#CD5C5C', '#B22222']
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart for category spending
            fig_bar = px.bar(
                category_sum,
                x='category',
                y='amount',
                title='📊 Spending by Category',
                color='amount',
                color_continuous_scale=['#FFE5E5', '#FF6B6B', '#DC143C', '#8B0000']
            )
            fig_bar.update_layout(xaxis_title="Category", yaxis_title="Amount (₹)")
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Timeline chart
        df_timeline = df_chart.groupby('date')['amount'].sum().reset_index()
        df_timeline = df_timeline.sort_values('date')
        
        fig_line = px.line(
            df_timeline,
            x='date',
            y='amount',
            title='📈 Expense Trend Over Time',
            markers=True
        )
        fig_line.update_traces(line_color='#DC143C', line_width=4, marker=dict(size=10, color='#8B0000'))
        fig_line.update_layout(xaxis_title="Date", yaxis_title="Amount (₹)")
        st.plotly_chart(fig_line, use_container_width=True)
    
    with tab3:
        st.subheader("🗑️ Manage Expenses")
        
        if st.session_state.expenses:
            for idx, exp in enumerate(st.session_state.expenses):
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    st.markdown(f"""
                        <div class="expense-card">
                            <h3 style="margin:0; color:#DC143C;">{exp['category']} - {exp['name']}</h3>
                            <p style="margin:8px 0; color:#666; font-size: 1.1em;">💰 <strong style="color:#DC143C;">₹{exp['amount']:,.2f}</strong> | 📅 {exp['date']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🗑️ Delete", key=f"delete_{idx}"):
                        st.session_state.expenses.pop(idx)
                        st.success("✅ Expense deleted!")
                        st.rerun()
            
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button("🗑️ CLEAR ALL", key="clear_all"):
                    st.session_state.expenses = []
                    st.success("✅ All expenses cleared!")
                    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #DC143C; padding: 25px; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(220, 20, 60, 0.1);">
        <p style="font-size: 1.1em;">💡 <strong>Pro Tip:</strong> Track your expenses regularly to stay on top of your finances!</p>
        <p style="font-size: 1.2em; margin-top: 10px;">Made with ❤️ by <strong>Dilwinder Singh</strong> | Stay Smart with Your Money 💰</p>
    </div>
""", unsafe_allow_html=True)
