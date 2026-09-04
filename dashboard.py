
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

DIFY_API_URL = "https://api.dify.ai/v1"
DIFY_API_KEY = os.getenv("DIFY_API_KEY")




# =========================================================
# CALL DIFY WORKFLOW
# =========================================================

if generate_report:

    if DIFY_API_URL == "YOUR_DIFY_ENDPOINT_HERE":

        st.error(
            "❌ Please configure your Dify API endpoint."
        )

        st.stop()

    if not DIFY_API_KEY:

        st.error(
            "❌ Dify API key is not configured."
        )

        st.stop()


    # =====================================================
    # EXACT DIFY VARIABLE NAMES
    # =====================================================

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


        # =================================================
        # GET DIFY OUTPUT
        # =================================================

        dify_outputs = dify_result.get(
            "data",
            {}
        ).get(
            "outputs",
            {}
        )


        if not dify_outputs:

            st.error(
                "❌ Dify returned no output."
            )

            st.stop()


        # Store Dify result

        st.session_state["dify_outputs"] = dify_outputs


        st.success(
            "✅ SmartSave AI analysis completed!"
        )


    except requests.exceptions.RequestException as e:

        st.error(
            f"❌ Could not connect to Dify: {e}"
        )


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

remaining_balance = (

    monthly_income
    - total_expenses

)


# =========================================================
# SAVINGS AMOUNT
# =========================================================

savings_amount = remaining_balance


# =========================================================
# PERCENTAGES
# =========================================================

if monthly_income > 0:

    savings_percentage = (

        savings_amount
        / monthly_income

    ) * 100


    expense_percentage = (

        total_expenses
        / monthly_income

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
# LEFT SIDEBAR - FINANCIAL OVERVIEW
# =========================================================

with st.sidebar:

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
        f"Income: ₹{monthly_income:,.0f}"
    )

    st.write(
        f"Expenses: ₹{total_expenses:,.0f}"
    )

    st.write(
        f"Savings: ₹{savings_amount:,.0f}"
    )


# =========================================================
# HEADER
# =========================================================

st.title(
    "💰 SmartSave Financial Dashboard"
)


if user_name.strip():

    display_name = user_name.title()

else:

    display_name = "User"


st.subheader(
    f"Welcome, {display_name} 👋"
)


st.write(
    "Here is a simple view of your income, spending and savings."
)


st.divider()


# =========================================================
# INCOME ALLOCATION
# =========================================================

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
        "Enter your financial details to view the income allocation."
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
            "Enter your expenses to view the chart."
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
            "Enter your expenses to view the chart."
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

    highest_amount
    / total_expenses
    * 100

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

            "🏠 Rent is usually a fixed expense, "
            "so focus on Food and Transport for easier savings."

        )

    elif highest_category == "Food":

        st.info(

            "🍱 Food is your biggest flexible expense. "
            "Meal planning and cooking at home can help."

        )

    elif highest_category == "Transport":

        st.info(

            "🚌 Transport is your biggest flexible expense. "
            "Public transport or carpooling may reduce costs."

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


    st.success(

        f"💰 Reducing Food, Transport and Shopping by 10% "
        f"could save around **₹{potential_saving:,.0f}/month**."

    )

else:

    st.info(
        "Enter your expenses to get personalized cutting suggestions."
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

        f"Focusing on flexible expenses like Food and Transport "
        f"could help you save even more."

    )


    st.success(

        f"📅 If you maintain your current savings, "
        f"you could save approximately "
        f"**₹{annual_savings:,.0f} in a year**."

    )

else:

    st.info(
        "Enter your income and expenses to generate your SmartSave insight."
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
        "Enter your expenses to view the ranking."
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

    "This estimate assumes your current monthly income and "
    "expenses stay similar throughout the year."

)


# =========================================================
# SAVINGS GOAL
# =========================================================

st.divider()

st.subheader(
    "🎯 Savings Goal"
)


# Suggested goal based on income

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

            savings_amount
            - monthly_goal

        )


        st.success(

            f"🎉 Great job! You are saving "
            f"₹{savings_amount:,.0f} this month, "

            f"which is ₹{extra_savings:,.0f} more than "
            f"your ₹{monthly_goal:,.0f} goal."

        )

    else:

        remaining_goal = (

            monthly_goal
            - savings_amount

        )


        st.warning(

            f"💪 You need ₹{remaining_goal:,.0f} more "
            f"to reach your monthly goal."

        )

else:

    st.info(
        "Enter your income to calculate your savings goal."
    )


# =========================================================
# SAVING OPPORTUNITIES
# =========================================================

st.divider()

st.subheader(
    "💡 Saving Opportunities"
)


st.write(
    "These are small areas where you may be able to save more money:"
)


# =========================================================
# FOOD
# =========================================================

if food_monthly > 0:

    food_saving = (

        food_monthly * 0.10

    )


    st.info(

        f"🍱 **Food:** You spend "
        f"₹{food_monthly:,.0f} per month on food. "

        f"If you reduce this by 10%, "
        f"you could save around "
        f"₹{food_saving:,.0f} every month."

    )


# =========================================================
# TRANSPORT
# =========================================================

if transport_monthly > 0:

    transport_saving = (

        transport_monthly * 0.10

    )


    st.info(

        f"🚌 **Transport:** You spend "
        f"₹{transport_monthly:,.0f} per month on transport. "

        f"Using public transport or carpooling "
        f"could help you save around "
        f"₹{transport_saving:,.0f} every month."

    )


# =========================================================
# SHOPPING
# =========================================================

if shopping_monthly > 0:

    shopping_saving = (

        shopping_monthly * 0.10

    )


    st.info(

        f"🛍️ **Shopping:** You spend "
        f"₹{shopping_monthly:,.0f} per month on shopping. "

        f"Cutting unnecessary purchases by 10% "
        f"could save around "
        f"₹{shopping_saving:,.0f} every month."

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

        f"₹{annual_savings:,.0f}"

    ]

})


st.dataframe(

    summary_data,

    use_container_width=True,

    hide_index=True

)


# =========================================================
# DIFY AI OUTPUT
# =========================================================

if "dify_outputs" in st.session_state:

    st.divider()

    st.subheader(
        "🤖 SmartSave AI Report"
    )


    dify_outputs = st.session_state[
        "dify_outputs"
    ]


    if isinstance(dify_outputs, dict):

        for key, value in dify_outputs.items():

            if isinstance(value, str):

                st.markdown(value)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "💰 SmartSave AI | Personal Finance & Savings Optimization Dashboard"
)

