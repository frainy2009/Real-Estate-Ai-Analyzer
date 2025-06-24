# get2million_ai_analyzer.py – Get2Million Real Estate AI Analyzer

import streamlit as st

st.set_page_config(page_title="Get2Million™ Analyzer", page_icon="💸", layout="centered")

st.markdown("<h1 style='text-align: center; color: #0A2342;'>💸 Get2Million™ Real Estate AI Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px;'>Analyze rental property deals like a pro. Cash flow, ROI, cap rate, and more — all in one AI-powered tool.</p>", unsafe_allow_html=True)
st.markdown("---")

# Step 1: Property Basics
st.subheader("📌 Property Basics")
purchase_price = st.number_input("Purchase Price ($)", min_value=0.0, value=250000.0)
estimated_rent = st.number_input("Monthly Rent ($)", min_value=0.0, value=2200.0)
units = st.number_input("Number of Units", min_value=1, value=1)

# Step 2: Financing & Expenses
st.subheader("🏦 Financing & Expenses")
down_payment_percent = st.slider("Down Payment (%)", 0, 100, 25)
mortgage_rate = st.number_input("Interest Rate (%)", 0.0, 100.0, 6.5)
mortgage_term = st.number_input("Loan Term (years)", 1, 40, 30)
taxes_annual = st.number_input("Annual Property Taxes ($)", 0.0, 100000.0, 6000.0)
insurance_annual = st.number_input("Annual Insurance ($)", 0.0, 10000.0, 1200.0)
repairs_percent = st.slider("Repairs (% of rent)", 0, 50, 10)
vacancy_percent = st.slider("Vacancy (% of rent)", 0, 50, 5)
management_percent = st.slider("Property Management (% of rent)", 0, 50, 8)

# Step 3: Appreciation & Exit
st.subheader("📈 Appreciation & Exit")
appreciation_rate = st.slider("Annual Appreciation (%)", 0.0, 20.0, 3.0)
holding_years = st.slider("Expected Holding Period (Years)", 1, 30, 5)

# Step 4: Calculations
try:
    down_payment = purchase_price * (down_payment_percent / 100)
    loan_amount = purchase_price - down_payment
    monthly_interest = mortgage_rate / 100 / 12
    total_payments = mortgage_term * 12
    mortgage_payment = (loan_amount * monthly_interest) / (1 - (1 + monthly_interest)**-total_payments)

    monthly_rent = estimated_rent * units
    monthly_expenses = (
        mortgage_payment +
        taxes_annual / 12 +
        insurance_annual / 12 +
        monthly_rent * (repairs_percent + vacancy_percent + management_percent) / 100
    )

    monthly_cash_flow = monthly_rent - monthly_expenses
    annual_cash_flow = monthly_cash_flow * 12
    cash_on_cash = (annual_cash_flow / down_payment) * 100 if down_payment else 0
    cap_rate = ((monthly_rent * 12 - (monthly_expenses - mortgage_payment * 12)) / purchase_price) * 100

    future_value = purchase_price * ((1 + appreciation_rate / 100) ** holding_years)
    total_profit = (future_value - purchase_price) + (annual_cash_flow * holding_years)
    total_roi = (total_profit / down_payment) * 100 if down_payment else 0

    st.markdown("---")
    st.subheader("📊 Results Summary")
    st.metric("Monthly Cash Flow", f"${monthly_cash_flow:,.2f}")
    st.metric("Annual Cash Flow", f"${annual_cash_flow:,.2f}")
    st.metric("Cash-on-Cash Return", f"{cash_on_cash:.2f}%")
    st.metric("Cap Rate", f"{cap_rate:.2f}%")
    st.metric("Projected Property Value", f"${future_value:,.2f}")
    st.metric("Total ROI (Cash + Appreciation)", f"{total_roi:.2f}%")
except Exception as e:
    st.error(f"⚠️ Error in calculation: {e}")

st.markdown("---")
st.markdown("<small><center>© Get2Million™ by frainy2009 — Built with ❤️ using Streamlit</center></small>", unsafe_allow_html=True)
