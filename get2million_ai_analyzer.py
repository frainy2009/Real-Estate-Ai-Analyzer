import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="💼 Get2Million | Real Estate Deal Analyzer", layout="wide")

# ---------- Title ----------
st.markdown("""
# 🏠 Get2Million Real Estate Deal Analyzer  
**Elite investment underwriting tool built for serious real estate professionals.**
""")

# ---------- Property Details ----------
with st.expander("📋 Property Details", expanded=True):
    col1, col2, col3 = st.columns(3)
    purchase_price = col1.number_input("Purchase Price ($)", value=350000, step=1000, format="%.0f")
    down_payment_pct = col2.number_input("Down Payment (%)", value=25.0, step=1.0, format="%.2f") / 100
    closing_costs = col3.number_input("Closing Costs ($)", value=6000, step=500, format="%.0f")

    loan_amount = purchase_price * (1 - down_payment_pct)
    total_investment = purchase_price * down_payment_pct + closing_costs

# ---------- Rental Income ----------
with st.expander("💰 Rental Income", expanded=True):
    unit_count = st.number_input("Number of Units", 1, 20, 3)
    unit_cols = st.columns(unit_count)
    rents = [unit_cols[i].number_input(f"Unit {i+1} Rent ($)", value=1200, step=50, format="%.0f") for i in range(unit_count)]

    monthly_gross_rent = sum(rents)
    annual_gross_rent = monthly_gross_rent * 12
    st.success(f"🏦 **Monthly Gross Rent:** ${monthly_gross_rent:,.0f} | **Annual:** ${annual_gross_rent:,.0f}")

# ---------- Expenses ----------
with st.expander("🧾 Operating Expenses", expanded=True):
    e1, e2, e3 = st.columns(3)
    taxes = e1.number_input("Property Taxes ($/yr)", value=7200, format="%.0f")
    insurance = e2.number_input("Insurance ($/yr)", value=1200, format="%.0f")
    vacancy_rate = e3.number_input("Vacancy Rate (%)", value=5.0, format="%.2f") / 100

    e4, e5, e6 = st.columns(3)
    repairs = e4.number_input("Repairs & Maintenance ($/yr)", value=1500, format="%.0f")
    management_pct = e5.number_input("Property Management (%)", value=8.0, format="%.2f") / 100
    utilities = e6.number_input("Utilities ($/yr)", value=1800, format="%.0f")

    reserves = st.number_input("Capital Reserves ($/yr)", value=600, format="%.0f")

    vacancy_loss = annual_gross_rent * vacancy_rate
    management_fee = annual_gross_rent * management_pct

    total_expenses = taxes + insurance + vacancy_loss + repairs + management_fee + utilities + reserves
    noi = annual_gross_rent - total_expenses
    cap_rate = (noi / purchase_price) * 100

# ---------- Loan & Amortization ----------
with st.expander("🏦 Loan Details", expanded=True):
    lc1, lc2 = st.columns(2)
    interest_rate = lc1.number_input("Interest Rate (%)", value=6.5, format="%.2f") / 100
    loan_term = lc2.number_input("Loan Term (years)", value=30)

    monthly_rate = interest_rate / 12
    n_payments = loan_term * 12
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
    annual_debt_service = monthly_payment * 12

# ---------- Depreciation & Tax Savings ----------
with st.expander("💵 Depreciation & Tax Benefits", expanded=True):
    structure_value = purchase_price * 0.85
    depreciation = structure_value / 27.5
    tax_rate = st.number_input("Marginal Tax Rate (%)", value=24.0, format="%.2f") / 100
    tax_savings = depreciation * tax_rate

# ---------- Principal Paydown (Year 1) ----------
balance = loan_amount
principal_paid = 0
for _ in range(12):
    interest = balance * monthly_rate
    principal = monthly_payment - interest
    balance -= principal
    principal_paid += principal

# ---------- Appreciation ----------
appreciation_rate = st.number_input("Annual Appreciation Rate (%)", value=3.0, format="%.2f") / 100
equity_gain = purchase_price * appreciation_rate

# ---------- ROI Breakdown ----------
st.markdown("### 📊 ROI Summary")
cash_flow = noi - annual_debt_service
total_return = cash_flow + tax_savings + principal_paid + equity_gain
roi = (total_return / total_investment) * 100
dcr = noi / annual_debt_service

st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Net Operating Income", f"${noi:,.0f}")
col2.metric("Cash Flow (Year 1)", f"${cash_flow:,.0f}")
col3.metric("Cap Rate", f"{cap_rate:.2f}%")
col4.metric("DCR", f"{dcr:.2f}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Tax Savings", f"${tax_savings:,.0f}")
col6.metric("Principal Paydown", f"${principal_paid:,.0f}")
col7.metric("Equity Gain (Appreciation)", f"${equity_gain:,.0f}")
col8.metric("ROI (Year 1)", f"{roi:.2f}%")
st.divider()

# ---------- Rent Growth Forecast ----------
with st.expander("📈 10-Year Rent Growth Forecast"):
    growth_rate = st.number_input("Annual Rent Growth (%)", value=3.0, format="%.2f") / 100
    years = np.arange(1, 11)
    projected_rent = monthly_gross_rent * ((1 + growth_rate) ** (years - 1))
    df_growth = pd.DataFrame({
        "Year": years,
        "Monthly Rent": projected_rent.round(2),
        "Annual Rent": (projected_rent * 12).round(2)
    })
    st.dataframe(df_growth.style.format({"Monthly Rent": "${:,.2f}", "Annual Rent": "${:,.2f}"}), use_container_width=True)

# ---------- Footer ----------
st.markdown("---")
st.caption("🛡️ Built by Get2Million.com • Trusted real estate analytics for elite investors.")
