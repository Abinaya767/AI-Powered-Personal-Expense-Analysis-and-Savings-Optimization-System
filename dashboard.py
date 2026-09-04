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
    initial_sidebar_state="expanded"
)


# =========================================================
# READ VALUES FROM DIFY URL
# =========================================================

params = st.query_params


def get_float(name):
    try:
        return float(params.get(name, 0))
    except (ValueError, TypeError):
        return 0.0


user_name = params.get("user_name", "User")

monthly_income = get_float("monthly_income")
rent_monthly = get_float("rent_monthly")
education_monthly = get_float("education_monthly")
healthcare_monthly = get_float("healthcare_monthly")
food_daily = get_float("food_daily")
transport_daily = get_float("transport_daily")
shopping_monthly = get_float("shopping_monthly")
other_monthly = get_float("other_monthly")


# =========================================================
# MONTHLY CALCULATIONS
# =========================================================

food_monthly = food_daily * 30
transport_monthly = transport_daily * 30


# =========================================================
# TOTAL MONTHLY EXPENSES
# =========================================================

total_expenses = (
    rent_monthly
    + education_monthly
    + healthcare_monthly
    + food_monthly
    + transport_monthly
    + shopping_monthly
    + other_monthly
)


# =========================================================
# REMAINING BALANCE
# =========================================================

remaining_balance = monthly_income - total_expenses


# =========================================================
# SAVINGS
# =========================================================

savings_amount = remaining_balance


# =========================================================
# PERCENTAGES
# =========================================================

if monthly_income > 0:

    savings_percentage = (
        savings_amount / monthly_income
    ) * 100

    expense_percentage = (
        total_expenses / monthly_income
    ) * 100

else:

    savings_percentage = 0
    expense_percentage = 0


# =========================================================
# ANNUAL CALCULATIONS
# =========================================================

annual_income = monthly_income * 12
annual_expenses = total_expenses * 12
annual_savings = savings_amount * 12


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
# FINANCIAL PERSONALITY
# =========================================================

if savings_percentage >= 50:

    financial_personality = "🌟 Smart Saver"

    personality_description = (
        "You are maintaining a strong savings rate and "
        "showing good control over your spending."
    )

elif savings_percentage >= 20:

    financial_personality = "⚖️ Balanced Planner"

    personality_description = (
        "You have a reasonable balance between spending "
        "and saving, with opportunities to improve."
    )

else:

    financial_personality = "⚠️ Spending Risk"

    personality_description = (
        "A large portion of your income is being spent. "
        "Reducing flexible expenses could improve your savings."
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


expense_data = expense_data[
    expense_data["Amount"] > 0
]


expense_data = expense_data.sort_values(
    by="Amount",
    ascending=False
)


# =========================================================
# DISPLAY NAME
# =========================================================

if user_name and str(user_name).strip():

    display_name = str(user_name).title()

else:

    display_name = "User"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("💰 SmartSave AI")

    st.caption(
        "Personal Finance & Savings Optimization"
    )

    st.divider()

    st.subheader("📌 Financial Status")

    if financial_status == "Healthy":

        st.success("🟢 Healthy")

    elif financial_status == "Moderate":

        st.warning("🟡 Moderate")

    else:

        st.error("🔴 Needs Improvement")


    st.divider()

    st.subheader("📅 Monthly Overview")

    st.write(
        f"💵 Income: ₹{monthly_income:,.0f}"
    )

    st.write(
        f"💸 Expenses: ₹{total_expenses:,.0f}"
    )

    st.write(
        f"💰 Savings: ₹{savings_amount:,.0f}"
    )

    st.divider()

    st.subheader("🧠 Financial Personality")

    st.write(
        financial_personality
    )


# =========================================================
# HEADER
# =========================================================

st.title(
    "💰 SmartSave Financial Dashboard"
)

st.subheader(
    f"Welcome, {display_name} 👋"
)

st.write(
    "Your personalized financial picture based on the information "
    "you provided to SmartSave AI."
)

st.divider()


# =========================================================
# KEY FINANCIAL METRICS
# =========================================================

st.subheader("📌 Financial Snapshot")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "💵 Monthly Income",
        f"₹{monthly_income:,.0f}"
    )

with col2:

    st.metric(
        "💸 Monthly Expenses",
        f"₹{total_expenses:,.0f}"
    )

with col3:

    st.metric(
        "💰 Remaining Balance",
        f"₹{remaining_balance:,.0f}"
    )

with col4:

    st.metric(
        "📈 Savings Rate",
        f"{savings_percentage:.1f}%"
    )


# =========================================================
# INCOME ALLOCATION
# =========================================================

st.divider()

st.subheader(
    "📊 Income Allocation"
)

allocation_data = pd.DataFrame({

    "Category": [
        "Expenses",
        "Savings"
    ],

    "Amount": [
        max(total_expenses, 0),
        max(savings_amount, 0)
    ]

})


if allocation_data["Amount"].sum() > 0:

    fig_allocation = px.pie(
        allocation_data,
        names="Category",
        values="Amount",
        hole=0.5
    )

    fig_allocation.update_traces(
        textinfo="label+percent"
    )

    st.plotly_chart(
        fig_allocation,
        use_container_width=True
    )

else:

    st.info(
        "No financial data was provided."
    )


# =========================================================
# EXPENSE ANALYSIS
# =========================================================

st.divider()

st.subheader(
    "📊 Expense Analysis"
)

col1, col2 = st.columns(2)


# =========================================================
# EXPENSE DISTRIBUTION
# =========================================================

with col1:

    st.write(
        "### 🍩 Expense Distribution"
    )

    if len(expense_data) > 0:

        fig_pie = px.pie(
            expense_data,
            names="Category",
            values="Amount",
            hole=0.45
        )

        fig_pie.update_traces(
            textinfo="label+percent"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    else:

        st.info(
            "No expense data available."
        )


# =========================================================
# SPENDING BY CATEGORY
# =========================================================

with col2:

    st.write(
        "### 📊 Spending by Category"
    )

    if len(expense_data) > 0:

        fig_bar = px.bar(
            expense_data,
            x="Category",
            y="Amount",
            text="Amount"
        )

        fig_bar.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )

        fig_bar.update_layout(
            xaxis_title="Category",
            yaxis_title="Amount (₹)"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    else:

        st.info(
            "No expense data available."
        )


# =========================================================
# SPENDING INSIGHTS
# =========================================================

st.divider()

st.subheader(
    "🏆 Spending Insights"
)

if len(expense_data) > 0:

    highest_category = (
        expense_data.iloc[0]["Category"]
    )

    highest_amount = (
        expense_data.iloc[0]["Amount"]
    )

else:

    highest_category = "None"
    highest_amount = 0


highest_percentage = (

    highest_amount / total_expenses * 100

    if total_expenses > 0

    else 0

)


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🏆 Highest Spending",
        highest_category
    )

with col2:

    st.metric(
        "💸 Highest Amount",
        f"₹{highest_amount:,.0f}"
    )

with col3:

    st.metric(
        "📊 Share of Expenses",
        f"{highest_percentage:.1f}%"
    )


# =========================================================
# SMARTSAVE SCORE
# =========================================================

st.divider()

st.subheader(
    "⭐ SmartSave Score"
)


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


score_col1, score_col2 = st.columns([1, 3])


with score_col1:

    st.metric(
        "SmartSave Score",
        f"{smartsave_score}/100"
    )


with score_col2:

    if smartsave_score >= 80:

        st.success(
            "⭐ Excellent! Your savings rate is strong "
            "and your finances are well controlled."
        )

    elif smartsave_score >= 60:

        st.info(
            "👍 Good progress! A few spending changes "
            "can improve your financial health."
        )

    else:

        st.warning(
            "💡 Your spending needs attention. "
            "Focus on reducing unnecessary expenses."
        )


# =========================================================
# FINANCIAL PERSONALITY
# =========================================================

st.divider()

st.subheader(
    "🧠 Your Financial Personality"
)

st.markdown(
    f"## {financial_personality}"
)

st.write(
    personality_description
)


# =========================================================
# WHERE SHOULD I CUT?
# =========================================================

st.divider()

st.subheader(
    "✂️ Where Should I Cut?"
)


if len(expense_data) > 0:

    st.write(

        f"Your biggest expense is "
        f"**{highest_category} – ₹{highest_amount:,.0f}**."
    )


    if highest_category == "Rent":

        st.info(

            "🏠 Rent is usually a fixed expense. "
            "Focus on flexible categories such as Food, "
            "Transport and Shopping for easier savings."
        )

    elif highest_category == "Food":

        st.info(

            "🍱 Food is your biggest flexible expense. "
            "Meal planning and cooking at home can help."
        )

    elif highest_category == "Transport":

        st.info(

            "🚌 Transport is one of your major expenses. "
            "Public transport or carpooling may reduce costs."
        )

    elif highest_category == "Shopping":

        st.info(

            "🛍️ Shopping is your biggest flexible expense. "
            "Reducing non-essential purchases can improve savings."
        )

    else:

        st.info(

            "💡 Start by reducing your highest flexible "
            "expense before cutting essential expenses."
        )


    potential_saving = (

        food_monthly * 0.10
        + transport_monthly * 0.10
        + shopping_monthly * 0.10
    )


    if potential_saving > 0:

        st.success(

            f"💰 Reducing Food, Transport and Shopping by "
            f"10% could save around "
            f"**₹{potential_saving:,.0f}/month**."
        )

else:

    st.info(
        "No expense data available."
    )


# =========================================================
# SMARTSAVE AI INSIGHT
# =========================================================

st.divider()

st.subheader(
    "🤖 SmartSave AI Insight"
)


if monthly_income > 0:

    st.info(

        f"You are currently saving "
        f"**{savings_percentage:.1f}% of your income**. "

        f"Your biggest expense is "
        f"**{highest_category}**. "

        f"Focusing on flexible expenses could help "
        f"you improve your savings further."
    )


    st.success(

        f"📅 If you maintain your current savings, "
        f"you could save approximately "
        f"**₹{annual_savings:,.0f} in a year**."
    )

else:

    st.info(
        "No income data available."
    )


# =========================================================
# EXPENSE RANKING
# =========================================================

st.divider()

st.subheader(
    "🥇 Expense Ranking"
)


ranking_data = expense_data.copy()


if len(ranking_data) > 0:

    ranking_data.insert(
        0,
        "Rank",
        range(
            1,
            len(ranking_data) + 1
        )
    )


    ranking_data["Amount"] = (

        ranking_data["Amount"]

        .apply(
            lambda x: f"₹{x:,.0f}"
        )

    )


    st.dataframe(
        ranking_data,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No expense data available."
    )


# =========================================================
# ANNUAL PROJECTION
# =========================================================

st.divider()

st.subheader(
    "📅 Annual Financial Projection"
)

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Annual Income",
        f"₹{annual_income:,.0f}"
    )


with col2:

    st.metric(
        "Annual Expenses",
        f"₹{annual_expenses:,.0f}"
    )


with col3:

    st.metric(
        "Estimated Annual Savings",
        f"₹{annual_savings:,.0f}"
    )


st.caption(

    "This estimate assumes your current monthly income "
    "and expenses remain similar throughout the year."
)


# =========================================================
# SAVINGS GOAL
# =========================================================

st.divider()

st.subheader(
    "🎯 Savings Goal"
)


if monthly_income > 0:

    monthly_goal = monthly_income * 0.20

else:

    monthly_goal = 0


st.write(

    f"Your suggested monthly savings goal is "
    f"**₹{monthly_goal:,.0f}**."
)


if monthly_income > 0:

    if savings_amount >= monthly_goal:

        extra_savings = (
            savings_amount - monthly_goal
        )

        st.success(

            f"🎉 Great job! You are saving "
            f"₹{savings_amount:,.0f} this month, "
            f"which is ₹{extra_savings:,.0f} more than "
            f"your ₹{monthly_goal:,.0f} goal."
        )

    else:

        remaining_goal = (
            monthly_goal - savings_amount
        )

        st.warning(

            f"💪 You need ₹{remaining_goal:,.0f} more "
            f"to reach your monthly goal."
        )


# =========================================================
# SAVING OPPORTUNITIES
# =========================================================

st.divider()

st.subheader(
    "💡 Saving Opportunities"
)

st.write(
    "Based on your current spending pattern:"
)


if food_monthly > 0:

    food_saving = food_monthly * 0.10

    st.info(

        f"🍱 **Food:** ₹{food_monthly:,.0f}/month. "
        f"A 10% reduction could save approximately "
        f"₹{food_saving:,.0f}/month."
    )


if transport_monthly > 0:

    transport_saving = transport_monthly * 0.10

    st.info(

        f"🚌 **Transport:** ₹{transport_monthly:,.0f}/month. "
        f"A 10% reduction could save approximately "
        f"₹{transport_saving:,.0f}/month."
    )


if shopping_monthly > 0:

    shopping_saving = shopping_monthly * 0.10

    st.info(

        f"🛍️ **Shopping:** ₹{shopping_monthly:,.0f}/month. "
        f"A 10% reduction could save approximately "
        f"₹{shopping_saving:,.0f}/month."
    )


# =========================================================
# SMARTSAVE RECOMMENDATIONS
# =========================================================

st.divider()

st.subheader(
    "💡 SmartSave Recommendations"
)


recommendations = [

    "🍱 Plan your meals and cook at home when possible.",

    "🚌 Use public transport or carpool for regular travel.",

    "🛍️ Think twice before buying non-essential items.",

    "📱 Track your daily expenses to find small spending leaks.",

    "🎯 Set a monthly savings target and try to reach it every month."

]


for recommendation in recommendations:

    st.write(
        recommendation
    )


# =========================================================
# FINANCIAL SUMMARY
# =========================================================

st.divider()

st.subheader(
    "📋 Financial Summary"
)


summary_data = pd.DataFrame({

    "Financial Metric": [

        "Monthly Income",
        "Total Monthly Expenses",
        "Remaining Balance",
        "Savings Amount",
        "Savings Percentage",
        "Expense Percentage",
        "Financial Status",
        "Financial Personality",
        "Estimated Annual Savings"

    ],

    "Value": [

        f"₹{monthly_income:,.0f}",
        f"₹{total_expenses:,.0f}",
        f"₹{remaining_balance:,.0f}",
        f"₹{savings_amount:,.0f}",
        f"{savings_percentage:.1f}%",
        f"{expense_percentage:.1f}%",
        financial_status,
        financial_personality,
        f"₹{annual_savings:,.0f}"

    ]

})


st.dataframe(

    summary_data,

    use_container_width=True,

    hide_index=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "💰 SmartSave AI | Personal Finance & Savings Optimization Dashboard"
)
