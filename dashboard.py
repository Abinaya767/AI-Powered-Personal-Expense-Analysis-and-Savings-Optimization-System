import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SmartSave AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# READ DIFY INPUTS FROM URL
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

    financial_status = "Healthy"
    status_icon = "🟢"
    status_message = (
        "You are saving a strong portion of your income. "
        "Keep maintaining this spending pattern."
    )

elif savings_percentage >= 20:

    financial_status = "Moderate"
    status_icon = "🟡"
    status_message = (
        "Your savings are at a reasonable level. "
        "Reducing a few flexible expenses can improve your savings."
    )

else:

    financial_status = "Needs Improvement"
    status_icon = "🔴"
    status_message = (
        "A large part of your income is being spent. "
        "Try to reduce non-essential expenses and build your savings."
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
# POTENTIAL SAVINGS
# =========================================================

potential_savings = 0

if food_monthly > 0:
    potential_savings += food_monthly * 0.10

if transport_monthly > 0:
    potential_savings += transport_monthly * 0.10

if shopping_monthly > 0:
    potential_savings += shopping_monthly * 0.20

if other_monthly > 0:
    potential_savings += other_monthly * 0.10

improved_savings = (
    savings_amount + potential_savings
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("💰 SmartSave AI")

    st.markdown(
        f"### 👋 Welcome, {user_name}"
    )

    st.caption(
        "Your personal monthly money overview"
    )

    st.divider()

    st.markdown("### 💵 Income")

    st.metric(
        "Monthly Salary",
        f"₹{monthly_income:,.0f}"
    )

    st.divider()

    st.markdown("### 💸 Spending")

    st.metric(
        "Total Expenses",
        f"₹{total_expenses:,.0f}"
    )

    st.divider()

    st.markdown("### 📈 Savings")

    st.metric(
        "Savings Rate",
        f"{savings_percentage:.1f}%"
    )

    st.divider()

    st.markdown("### 💰 Money Left")

    st.metric(
        "Remaining Balance",
        f"₹{remaining_balance:,.0f}"
    )

    st.divider()

    st.caption(
        "SmartSave AI helps you understand your spending "
        "and make better monthly saving decisions."
    )


# =========================================================
# MAIN DASHBOARD HEADER
# =========================================================

st.title("💰 SmartSave Financial Dashboard")

st.markdown(
    f"### 👤 {user_name}'s Monthly Financial Overview"
)

st.write(
    "This dashboard gives you a simple view of your income, "
    "expenses, savings and areas where you can improve."
)


# =========================================================
# FINANCIAL OVERVIEW
# =========================================================

st.divider()

st.subheader("💵 Financial Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "💰 Monthly Income",
        f"₹{monthly_income:,.0f}"
    )

with col2:

    st.metric(
        "💸 Total Expenses",
        f"₹{total_expenses:,.0f}"
    )

with col3:

    st.metric(
        "💵 Money Left",
        f"₹{remaining_balance:,.0f}"
    )

with col4:

    st.metric(
        "📈 Savings",
        f"{savings_percentage:.1f}%"
    )


st.info(
    f"💡 You earn ₹{monthly_income:,.0f} per month and spend "
    f"₹{total_expenses:,.0f}. After your expenses, you have "
    f"₹{remaining_balance:,.0f} available for savings or other goals."
)


# =========================================================
# FINANCIAL STATUS
# =========================================================

st.divider()

st.subheader("📊 Your Financial Health")

status_col1, status_col2 = st.columns([1, 2])

with status_col1:

    if financial_status == "Healthy":

        st.success(
            f"{status_icon} {financial_status}"
        )

    elif financial_status == "Moderate":

        st.warning(
            f"{status_icon} {financial_status}"
        )

    else:

        st.error(
            f"{status_icon} {financial_status}"
        )


with status_col2:

    st.markdown(
        f"**What this means:** {status_message}"
    )

    st.write(
        f"You are currently saving **{savings_percentage:.1f}%** "
        f"of your monthly income."
    )


# =========================================================
# SMARTSAVE SCORE
# =========================================================

st.divider()

st.subheader("⭐ SmartSave Score")

score_col1, score_col2 = st.columns([1, 3])

with score_col1:

    st.metric(
        "Financial Score",
        f"{smartsave_score}/100"
    )

with score_col2:

    if smartsave_score >= 80:

        st.success(
            "Excellent! Your current savings pattern is strong."
        )

    elif smartsave_score >= 60:

        st.info(
            "Good progress. A few spending improvements "
            "can make your savings stronger."
        )

    else:

        st.warning(
            "Your score shows that there is significant "
            "room to improve your monthly savings."
        )


# =========================================================
# EXPENSE ANALYSIS
# =========================================================

st.divider()

st.subheader("💸 Where Your Money Goes")

st.write(
    "This section shows how your monthly income is distributed "
    "across different expense categories."
)

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
            hole=0.40,
            title="Monthly Expense Distribution"
        )

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

            yaxis_title="Monthly Amount (₹)",

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


# =========================================================
# HIGHEST SPENDING
# =========================================================

st.divider()

st.subheader("🔥 Your Highest Spending Areas")

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
            f"({percentage:.1f}% of your income)"
        )

    highest_category = top_categories.iloc[0]

    st.info(
        f"💡 **{highest_category['Category']}** is your largest "
        f"expense at ₹{highest_category['Amount']:,.0f}. "
        "Because this category takes a larger share of your income, "
        "managing your other flexible expenses can help you save more."
    )


# =========================================================
# SAVINGS ANALYSIS
# =========================================================

st.divider()

st.subheader("💰 Savings Analysis")

save_col1, save_col2, save_col3 = st.columns(3)

with save_col1:

    st.metric(
        "💵 Current Savings",
        f"₹{savings_amount:,.0f}"
    )

with save_col2:

    st.metric(
        "📈 Savings Rate",
        f"{savings_percentage:.1f}%"
    )

with save_col3:

    st.metric(
        "🎯 Potential Extra Savings",
        f"₹{potential_savings:,.0f}"
    )


st.write(
    f"Right now, you can save around **₹{savings_amount:,.0f}** "
    f"from your monthly income. With small improvements in flexible "
    f"expenses, you could potentially save an additional "
    f"**₹{potential_savings:,.0f}**."
)


# =========================================================
# SPENDING INSIGHTS
# =========================================================

st.divider()

st.subheader("🤖 SmartSave Insights")

if rent_monthly > 0 and monthly_income > 0:

    rent_percentage = (
        rent_monthly / monthly_income
    ) * 100

    if rent_percentage > 40:

        st.write(
            f"🏠 **Housing:** Your rent is ₹{rent_monthly:,.0f}, "
            f"which is about {rent_percentage:.1f}% of your income. "
            "Since rent is usually a fixed cost, focus on controlling "
            "your flexible expenses."
        )


if food_monthly > 0:

    st.write(
        f"🍱 **Food:** Your estimated monthly food spending is "
        f"₹{food_monthly:,.0f}. Planning meals and avoiding "
        "unnecessary purchases may help reduce this amount."
    )


if transport_monthly > 0:

    st.write(
        f"🚌 **Transport:** Your estimated monthly transport "
        f"spending is ₹{transport_monthly:,.0f}. Better trip planning "
        "may help reduce avoidable transport costs."
    )


if shopping_monthly > 0:

    if monthly_income > 0 and (
        shopping_monthly / monthly_income
    ) * 100 < 5:

        st.write(
            f"🛍️ **Shopping:** Your shopping expense is only "
            f"₹{shopping_monthly:,.0f}. This is a small part of "
            "your income, so it does not need major reduction."
        )

    else:

        st.write(
            f"🛍️ **Shopping:** You spend ₹{shopping_monthly:,.0f} "
            "per month. Reducing non-essential purchases can "
            "increase your savings."
        )


# =========================================================
# SIMPLE MONEY BREAKDOWN
# =========================================================

st.divider()

st.subheader("💡 Simple Money Breakdown")

if monthly_income > 0:

    expense_percentage = (
        total_expenses / monthly_income
    ) * 100

    st.write(
        f"💸 **{expense_percentage:.1f}%** of your income "
        f"is currently going towards expenses."
    )

    st.write(
        f"💰 **{savings_percentage:.1f}%** of your income "
        f"remains as savings."
    )

    if savings_percentage >= 30:

        st.success(
            "Your savings level is good. Try to maintain it "
            "every month and gradually increase it if possible."
        )

    elif savings_percentage >= 20:

        st.warning(
            "Your savings are reasonable. Small reductions "
            "in flexible expenses can improve your savings rate."
        )

    else:

        st.error(
            "Your expenses are taking up most of your income. "
            "Focus first on reducing non-essential spending."
        )


# =========================================================
# NEXT MONTH GOAL
# =========================================================

st.divider()

st.subheader("🎯 Next Month Savings Goal")

target_savings = monthly_income * 0.35

if target_savings > savings_amount:

    additional_needed = (
        target_savings - savings_amount
    )

    st.info(
        f"🎯 A practical next goal is to save around "
        f"**₹{target_savings:,.0f}** per month. "
        f"That means finding about **₹{additional_needed:,.0f}** "
        "of additional savings from flexible expenses."
    )

else:

    st.success(
        f"🎯 Great! Your current savings of "
        f"₹{savings_amount:,.0f} already meet the "
        f"₹{target_savings:,.0f} target."
    )


# =========================================================
# FINAL SUMMARY
# =========================================================

st.divider()

st.subheader("📋 Your Financial Summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.write(
        f"💰 **Monthly Income:** ₹{monthly_income:,.0f}"
    )

    st.write(
        f"💸 **Monthly Expenses:** ₹{total_expenses:,.0f}"
    )

    st.write(
        f"💵 **Money Left:** ₹{remaining_balance:,.0f}"
    )

with summary_col2:

    st.write(
        f"📈 **Savings Rate:** {savings_percentage:.1f}%"
    )

    st.write(
        f"{status_icon} **Financial Status:** "
        f"{financial_status}"
    )

    st.write(
        f"⭐ **SmartSave Score:** "
        f"{smartsave_score}/100"
    )


st.success(
    f"💚 SmartSave Summary: You have ₹{remaining_balance:,.0f} "
    f"left after your monthly expenses. Your current savings rate "
    f"is {savings_percentage:.1f}%. Use the insights above to "
    "make small, realistic improvements next month."
)
