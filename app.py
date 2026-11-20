"""
Joseph v0.1 - early concept prototype (IOT6000U assessment 001)

An AI investment assistant idea for UK high-street banking apps, named after
Joseph, who advised Pharaoh to set aside a fifth of every harvest in the good
years to prepare for the hard years ahead (Genesis 41).

This first version is deliberately simple:
  - a few quick questions about the customer's goal, timeframe and risk
  - a simple rule that matches them to a type of ready-made fund
  - a plain-English explanation (a template for now; an LLM comes next)
  - a compound growth calculator to show investing vs cash

Run:  pip install streamlit pandas
      streamlit run app.py
"""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Joseph v0.1", page_icon="🌾", layout="centered")

st.title("🌾 Joseph")
st.caption("Early concept prototype (v0.1). Illustration only, not financial advice.")

tab1, tab2 = st.tabs(["Get a suggestion", "Compound growth calculator"])

# ---------------------------------------------------------------------------
# 1. Quick questions -> simple suggestion
# ---------------------------------------------------------------------------
FUNDS = {
    "safety": None,
    "cash": ("Cash ISA", "low", "cash only"),
    "cautious": ("Cautious ready-made fund", "lower", "mostly bonds, some shares"),
    "balanced": ("Balanced ready-made fund", "medium", "a mix of shares and bonds"),
    "growth": ("Growth ready-made fund", "higher", "mostly global shares"),
}


def suggest(emergency_fund, years, risk):
    """Simple rules for v0.1. A trained model replaces this in the next version."""
    if not emergency_fund:
        return "safety"
    if years < 3:
        return "cash"
    if risk <= 2:
        return "cautious"
    if risk >= 4 and years >= 10:
        return "growth"
    return "balanced"


with tab1:
    goal = st.selectbox("What are you saving for?",
                        ["Long-term wealth", "House deposit", "Retirement", "Something soon"])
    years = st.slider("How many years until you need the money?", 1, 30, 10)
    risk = st.select_slider("If your investment fell 10% in a month, you would...",
                            options=[1, 2, 3, 4, 5], value=3,
                            format_func=lambda v: {1: "Sell everything", 2: "Sell some",
                                                   3: "Wait and see", 4: "Hold calmly",
                                                   5: "Invest more"}[v])
    emergency = st.checkbox("I have at least 3 months of spending saved as cash", value=True)
    monthly = st.number_input("How much could you invest each month? (£)", 0, 5000, 100, step=25)

    choice = suggest(emergency, years, risk)
    st.divider()
    if FUNDS[choice] is None:
        st.info("Build a safety net first. Joseph suggests saving 3 months of spending in cash "
                "before you start investing.")
    else:
        name, level, mix = FUNDS[choice]
        st.subheader(f"Suggested starting point: {name}")
        st.write(
            f"For **{goal.lower()}** in **{years} years**, people in a similar position often "
            f"start with a **{name.lower()}**. It holds {mix}, with **{level} risk**. "
            f"Investing **£{monthly:,} a month** inside a stocks and shares ISA means any growth "
            f"is tax-free. The value of investments can fall as well as rise."
        )
        st.button("Talk to a human")
    st.caption("v0.1 uses simple rules and a template. Next: a trained model and an LLM chat.")

# ---------------------------------------------------------------------------
# 2. Compound growth calculator
# ---------------------------------------------------------------------------
with tab2:
    c1, c2 = st.columns(2)
    start = c1.number_input("Starting amount (£)", 0, 1_000_000, 1000, step=500)
    per_month = c2.number_input("Monthly amount (£)", 0, 10_000, 100, step=25)
    c3, c4 = st.columns(2)
    n_years = c3.slider("Years", 1, 40, 20)
    rate = c4.slider("Yearly growth (%)", 0.0, 12.0, 7.0, 0.5)
    cash_rate = 3.0

    invested = cash = paid = float(start)
    rows = []
    for year in range(1, n_years + 1):
        for _ in range(12):
            invested = invested * (1 + rate / 100 / 12) + per_month
            cash = cash * (1 + cash_rate / 100 / 12) + per_month
            paid += per_month
        rows.append({"Year": year, "Invested": round(invested),
                     "Cash at 3%": round(cash), "Paid in": round(paid)})

    m1, m2, m3 = st.columns(3)
    m1.metric("You pay in", f"£{paid:,.0f}")
    m2.metric(f"Invested at {rate:.1f}%", f"£{invested:,.0f}")
    m3.metric("Cash at 3%", f"£{cash:,.0f}")
    st.line_chart(pd.DataFrame(rows).set_index("Year"), color=["#117ACA", "#C9A227", "#5C6B7A"])
    st.caption("The S&P 500 has averaged about 10% a year since 1957 with dividends reinvested "
               "(Fidelity), but markets fall as well as rise. Fees and inflation not included.")
