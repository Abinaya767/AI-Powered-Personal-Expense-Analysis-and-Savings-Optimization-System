import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SmartSave Financial Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DIFY API CONFIGURATION
# =========================================================

DIFY_API_URL = "https://api.dify.ai/v1/workflows/run"
DIFY_API_KEY = os.getenv("DIFY_API_KEY")


# =========================================================
# USER INPUT
# =========================================================

with st.sidebar:

    st.title("💰 SmartSave AI")
    st.subheader("📝 Enter Your Financial Details")

    user_name = st.text_input(
        "Name",
        value=""
    )

    monthly_income = st.number_input(
        "Monthly Income (₹)",
        min_value=0.0,
        value=0.0
    )

    rent_monthly = st.number_input(
        "Monthly Rent (₹)",
        min_value=0.0,
        value=0.0
    )

    education_monthly = st.number_input(
        "Education (₹)",
        min_value=0.0,
        value=0.0
    )

    healthcare_monthly = st.number_input(
        "Healthcare (₹)",
        min_value=0.0,
        value=0.0
    )

    food_daily = st.number_input(
        "Daily Food Expense (₹)",
        min_value=0.0,
        value=0.0
    )

    transport_daily = st.number_input(
        "Daily Transport Expense (₹)",
        min_value=0.0,
        value=0.0
    )

    shopping_monthly = st.number_input(
        "Shopping (₹)",
        min_value=0.0,
        value=0.0
    )

    other_monthly = st.number_input(
        "Other Expenses (₹)",
        min_value=0.0,
        value=0.0
    )

    generate_report = st.button(
        "🚀 Analyze with SmartSave AI",
        use_container_width=True
    )


# =========================================================
# DIFY WORKFLOW
# =========================================================

if generate_report:

    if not DIFY_API_KEY:
        st.error("❌ Dify API key is not configured.")
        st.stop()

    payload = {
        "inputs": {
            "user_name": user_name,
            "monthly_income": monthly_income,
            "rent_monthly": rent_monthly,
            "education_monthly": education_monthly,
            "healthcare_monthly": healthcare_monthly,
            "food_daily": food_daily,
            "transport_daily": transport_daily,
            "shopping_monthly": shopping_monthly,
            "other_monthly": other_monthly
        },
        "response_mode": "blocking",
        "user": user_name
    }

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    try:

        response = requests.post(
            DIFY_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        dify_result = response.json()

        dify_outputs = (
            dify_result
            .get("data", {})
            .get("outputs", {})
        )

        if dify_outputs:
            st.session_state["dify_outputs"] = dify_outputs

            st.success(
                "✅ SmartSave AI analysis completed!"
            )

        else:
            st.error("❌ Dify returned no output.")

    except requests.exceptions.RequestException as e:

        st.error(
            f"❌ Could not connect to Dify: {e}"
        )


# =========================================================
# MAIN DASHBOARD
# =========================================================

st.title("💰 SmartSave Financial Dashboard")


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

remaining_balance = (
    monthly_income - total_expenses
)

savings_amount = max(
    remaining_balance,
    0
)

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

    financial_status = "Healthy"

elif savings_percentage >= 20:

    financial_status = "Moderate"

else:

    financial_status = "Needs Improvement"


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
# HEADER
# =========================================================

if user_name.strip():

    st.subheader(
        f"👤 User: {user_name}"
    )

else:

    st.subheader(
        "👤 User: User"
    )


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
# FINANCIAL STATUS
# =========================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 Financial Status")

    if financial_status == "Healthy":

        st.success(
            f"🟢 {financial_status}"
        )

    elif financial_status == "Moderate":

        st.warning(
            f"🟡 {financial_status}"
        )

    else:

        st.error(
            f"🔴 {financial_status}"
        )


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

        # ⭐ PIE LABEL FIX
        fig_pie.update_traces(

            textinfo="label+percent",

            textposition="inside",

            texttemplate=(
                "<b>%{label}</b>"
                "<br>%{percent:.1%}"
            ),

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

        st.info(
            "No expenses entered yet."
        )


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

        st.info(
            "No expenses entered yet."
        )


# =========================================================
# HIGHEST SPENDING CATEGORIES
# =========================================================

st.divider()

st.subheader(
    "🔥 Highest Spending Categories"
)

if not chart_data.empty:

    top_categories = chart_data.sort_values(
        "Amount",
        ascending=False
    ).head(3)

    for _, row in top_categories.iterrows():

        if monthly_income > 0:

            percentage = (
                row["Amount"]
                / monthly_income
            ) * 100

        else:

            percentage = 0

        st.write(
            f"**{row['Category']}** — "
            f"₹{row['Amount']:,.0f} "
            f"({percentage:.1f}% of income)"
        )

else:

    st.info(
        "No expense data available."
    )


# =========================================================
# POTENTIAL SAVINGS
# =========================================================

st.divider()

st.subheader(
    "💡 Potential Savings"
)

potential_savings = 0

saving_items = []


if food_monthly > 0:

    food_saving = (
        food_monthly * 0.10
    )

    potential_savings += food_saving

    saving_items.append(
        f"🍱 Food: potential additional "
        f"saving ₹{food_saving:,.0f}."
    )


if transport_monthly > 0:

    transport_saving = (
        transport_monthly * 0.10
    )

    potential_savings += transport_saving

    saving_items.append(
        f"🚌 Transport: potential additional "
        f"saving ₹{transport_saving:,.0f}."
    )


if shopping_monthly > 0:

    shopping_saving = (
        shopping_monthly * 0.20
    )

    potential_savings += shopping_saving

    saving_items.append(
        f"🛍️ Shopping: potential additional "
        f"saving ₹{shopping_saving:,.0f}."
    )


if other_monthly > 0:

    other_saving = (
        other_monthly * 0.10
    )

    potential_savings += other_saving

    saving_items.append(
        f"📦 Other expenses: potential additional "
        f"saving ₹{other_saving:,.0f}."
    )


for item in saving_items:

    st.write(item)


st.success(
    f"💰 Potential Additional Savings: "
    f"₹{potential_savings:,.0f}"
)


# =========================================================
# SAVINGS SUMMARY
# =========================================================

st.divider()

st.subheader(
    "💰 Savings Summary"
)

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Current Savings",
        f"₹{savings_amount:,.0f}"
    )


with col2:

    st.metric(
        "Potential Additional Savings",
        f"₹{potential_savings:,.0f}"
    )


with col3:

    improved_savings = (
        savings_amount
        + potential_savings
    )

    st.metric(
        "Improved Savings",
        f"₹{improved_savings:,.0f}"
    )


# =========================================================
# SMARTSAVE RECOMMENDATIONS
# =========================================================

st.divider()

st.subheader(
    "🤖 SmartSave Recommendations"
)

recommendations = []


if rent_monthly > 0 and monthly_income > 0:

    rent_percentage = (
        rent_monthly
        / monthly_income
    ) * 100

    if rent_percentage > 40:

        recommendations.append(
            f"🏠 Rent takes around "
            f"{rent_percentage:.0f}% of your income. "
            "Since it is a fixed expense, focus on "
            "controlling flexible expenses."
        )


if food_monthly > 0:

    recommendations.append(
        "🍱 Review food spending and avoid "
        "unnecessary food purchases where possible."
    )


if transport_monthly > 0:

    recommendations.append(
        "🚌 Plan trips efficiently to reduce "
        "avoidable transport expenses."
    )


if shopping_monthly > 0:

    if monthly_income > 0 and (
        shopping_monthly
        / monthly_income
    ) * 100 < 5:

        recommendations.append(
            "🛍️ Shopping spending is currently very "
            "low and does not require major reduction."
        )

    else:

        recommendations.append(
            "🛍️ Consider limiting non-essential "
            "shopping to improve savings."
        )


if savings_percentage >= 30:

    recommendations.append(
        "🎯 You are currently saving a good portion "
        "of your monthly income. Maintain this habit."
    )

else:

    recommendations.append(
        "🎯 Try to gradually increase your monthly "
        "savings by controlling flexible expenses."
    )


for recommendation in recommendations:

    st.write(
        f"• {recommendation}"
    )


# =========================================================
# NEXT MONTH TARGET
# =========================================================

st.divider()

st.subheader(
    "🎯 Next Month Target"
)

st.info(
    "Try to keep your **total monthly expenses "
    "at ₹20,000 or less** next month."
)


# =========================================================
# FINAL SUMMARY
# =========================================================

st.divider()

st.subheader(
    "📋 Financial Summary"
)

st.write(
    f"**Monthly Income:** "
    f"₹{monthly_income:,.0f}"
)

st.write(
    f"**Total Monthly Expenses:** "
    f"₹{total_expenses:,.0f}"
)

st.write(
    f"**Remaining Balance:** "
    f"₹{remaining_balance:,.0f}"
)

st.write(
    f"**Savings Percentage:** "
    f"{savings_percentage:.1f}%"
)

st.write(
    f"**Financial Status:** "
    f"{financial_status}"
)

st.write(
    f"**SmartSave Score:** "
    f"{smartsave_score}/100"
)
