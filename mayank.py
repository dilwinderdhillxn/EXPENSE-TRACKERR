import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ---- Config ----
st.set_page_config(page_title="💸 Expense Tracker", layout="centered")

DATA_FILE = "expenses.csv"

# ---- Load or Initialize ----
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

# ---- Sidebar: Add Expense ----
st.sidebar.header("➕ Add New Expense")
with st.sidebar.form("expense_form"):
    date = st.date_input("Date", datetime.today())
    category = st.selectbox("Category", ["Food", "Travel", "Bills", "Shopping", "Entertainment", "Other"])
    desc = st.text_input("Description")
    amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    new_expense = {"Date": date, "Category": category, "Description": desc, "Amount": amount}
    df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.sidebar.success("✅ Expense Added!")

# ---- Main Dashboard ----
st.title("💸 Personal Expense Tracker")
st.caption("Track your spending like a boss 😎")

# ---- Stats ----
if not df.empty:
    total = df["Amount"].sum()
    monthly = df.groupby(df["Date"].apply(lambda x: str(x)[:7]))["Amount"].sum()
    category_sum = df.groupby("Category")["Amount"].sum()

    st.subheader("📊 Overview")
    st.metric("Total Spent", f"₹{total:,.2f}")

    st.bar_chart(category_sum)
    st.line_chart(monthly)

    # ---- Show Data ----
    st.subheader("🧾 All Expenses")
    st.dataframe(df, use_container_width=True)

    # ---- Delete Section ----
    st.subheader("🗑️ Delete Expense")
    delete_index = st.number_input("Enter index to delete (row number)", min_value=0, max_value=len(df)-1, step=1)
    if st.button("Delete Selected Expense"):
        df = df.drop(df.index[delete_index])
        df.to_csv(DATA_FILE, index=False)
        st.success("Expense deleted successfully!")

    # ---- Download CSV ----
    st.download_button(
        label="📥 Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="expenses.csv",
        mime="text/csv",
    )
else:
    st.info("No expenses yet. Add some from the sidebar!")

# ---- Footer ----
st.markdown("---")
st.caption("Built with ❤️ by Mayank – Powered by Streamlit 🚀")
