import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SmartSave Financial Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# READ DIFY INPUTS FROM DASHBOARD URL
# =========================================================

params = st.query_params

user_name = params.get("user_name", "User")

monthly_income = float(params.get("monthly_income", 0))
rent_monthly = float(params.get("rent_monthly", 0))
education_monthly = float(params.get("education_monthly", 0))
healthcare_monthly = float(params.get("healthcare_monthly", 0))
food_daily = float(params.get("food_daily", 0))
transport_daily = float(params.get("transport_daily", 0))
shopping_monthly = float(params.get("shopping_monthly", 0))
other_monthly = float(params.get("other_monthly", 0))


# =========================================================
# MONTHLY CALCULATIONS
# =========================================================

food_monthly = food_daily * 30
transport_monthly = transport_daily * 30

total_expenses = (
    rent_monthly
    + education_monthly
    + healthcare_monthly
    + food_monthly
    + transport_monthly
    + shopping_monthly
    + other_monthly
)

remaining_balance = monthly_income - total_expenses

savings_amount = max(remaining_balance, 0)

if monthly_income > 0:
    savings_percentage = (
        savings_amount / monthly_income
    ) * 100
else:
    savings_percentage = 0


# =========================================================
# FINANCIAL STATUS
# =========================================================

if savings_percentage >= 50:

    financial_status = "🟢 Healthy"
    status_message = (
        "You are saving a strong portion of your monthly income."
    )

elif savings_percentage >= 20:

    financial_status = "🟡 Moderate"
    status_message = (
        "Your savings are okay, but there is room to improve."
    )

else:

    financial_status = "🔴 Needs Improvement"
    status_message = (
        "Try reducing flexible expenses and increase your savings."
    )


# =========================================================
# SMARTSAVE SCORE
# =========================================================

if savings_percentage >= 70:
    smartsave_score = 90
elif savings_percentage >= 50:
    smartsave_score = 80
elif savings_percentage >= 30:
    smartsave_score = 70
elif savings_percentage >= 20:
    smartsave_score = 60
else:
    smartsave_score = 50


# =========================================================
# DASHBOARD HEADER
# =========================================================

st.title("💰 SmartSave Financial Dashboard")

st.markdown(
    f"### 👤 User: {user_name}"
)

st.divider()


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💵 Monthly Income",
        f"₹{monthly_income:,.0f}"
    )

with col2:
    st.metric(
        "💸 Total Expenses",
        f"₹{total_expenses:,.0f}"
    )

with col3:
    st.metric(
        "💰 Remaining Balance",
        f"₹{remaining_balance:,.0f}"
    )

with col4:
    st.metric(
        "📈 Savings %",
        f"{savings_percentage:.1f}%"
    )


# =========================================================
# FINANCIAL STATUS + SCORE
# =========================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 Financial Status")

    if financial_status == "🟢 Healthy":
        st.success(financial_status)

    elif financial_status == "🟡 Moderate":
        st.warning(financial_status)

    else:
        st.error(financial_status)

    st.write(status_message)


with col2:

    st.subheader("⭐ SmartSave Score")

    st.metric(
        "Score",
        f"{smartsave_score}/100"
    )


# =========================================================
# EXPENSE DATA
# =========================================================

expense_data = pd.DataFrame({

    "Category": [
        "Rent",
        "Education",
        "Healthcare",
        "Food",
        "Transport",
        "Shopping",
        "Other"
    ],

    "Amount": [
        rent_monthly,
        education_monthly,
        healthcare_monthly,
        food_monthly,
        transport_monthly,
        shopping_monthly,
        other_monthly
    ]
})

chart_data = expense_data[
    expense_data["Amount"] > 0
].copy()


# =========================================================
# CHARTS
# =========================================================

st.divider()

st.subheader("📊 Expense Analysis")

chart_col1, chart_col2 = st.columns(2)


# =========================================================
# PIE CHART
# =========================================================

with chart_col1:

    if not chart_data.empty:

        fig_pie = px.pie(
            chart_data,
            names="Category",
            values="Amount",
            hole=0.35,
            title="Monthly Expense Distribution"
        )

        # PIE LABEL FIX
        fig_pie.update_traces(
            textinfo="label+percent",
            textposition="inside",
            texttemplate="<b>%{label}</b><br>%{percent:.1%}",
            insidetextorientation="horizontal",
            textfont_size=11,
            hovertemplate=(
                "<b>%{label}</b>"
                "<br>Amount: ₹%{value:,.0f}"
                "<br>Share: %{percent:.1%}"
                "<extra></extra>"
            )
        )

        fig_pie.update_layout(
            uniformtext_minsize=8,
            uniformtext_mode="show",
            margin=dict(
                t=50,
                b=20,
                l=20,
                r=20
            )
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    else:

        st.info("No expense data available.")


# =========================================================
# BAR CHART
# =========================================================

with chart_col2:

    if not chart_data.empty:

        fig_bar = px.bar(
            chart_data.sort_values(
                "Amount",
                ascending=False
            ),
            x="Category",
            y="Amount",
            title="Expense by Category",
            text="Amount"
        )

        fig_bar.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )

        fig_bar.update_layout(
            yaxis_title="Amount (₹)",
            xaxis_title="Category",
            margin=dict(
                t=50,
                b=40,
                l=20,
                r=20
            )
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    else:

        st.info("No expense data available.")


# =========================================================
# HIGHEST SPENDING
# =========================================================

st.divider()

st.subheader("🔥 Highest Spending Categories")

if not chart_data.empty:

    top_categories = chart_data.sort_values(
        "Amount",
        ascending=False
    ).head(3)

    for _, row in top_categories.iterrows():

        percentage = (
            row["Amount"] / monthly_income * 100
            if monthly_income > 0
            else 0
        )

        st.write(
            f"**{row['Category']}** — "
            f"₹{row['Amount']:,.0f} "
            f"({percentage:.1f}% of income)"
        )


# =========================================================
# SAVINGS SUMMARY
# =========================================================

st.divider()

st.subheader("💰 Savings Summary")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Current Savings",
        f"₹{savings_amount:,.0f}"
    )

with col2:

    st.metric(
        "Savings Rate",
        f"{savings_percentage:.1f}%"
    )


# =========================================================
# FINAL SUMMARY
# =========================================================

st.divider()

st.subheader("📋 Financial Summary")

st.write(f"**Monthly Income:** ₹{monthly_income:,.0f}")

st.write(f"**Total Monthly Expenses:** ₹{total_expenses:,.0f}")

st.write(f"**Remaining Balance:** ₹{remaining_balance:,.0f}")

st.write(f"**Savings Amount:** ₹{savings_amount:,.0f}")

st.write(f"**Savings Percentage:** {savings_percentage:.1f}%")

st.write(f"**Financial Status:** {financial_status}")

st.write(f"**SmartSave Score:** {smartsave_score}/100")
