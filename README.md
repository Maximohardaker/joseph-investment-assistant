# Joseph: an AI investment assistant for UK banking apps

Early concept prototype for IOT6000U Digital Innovation and Product Development (Queen Mary University of London), assessment 001.

Joseph is named after the Joseph of Genesis 41, who advised Pharaoh to set aside a fifth of every harvest in the good years to prepare for the hard years ahead. The idea: an assistant inside the banking app people already use that helps everyday customers start investing through a stocks and shares ISA.

## v0.1 (this version)

- A few quick questions: goal, timeframe, attitude to risk, emergency fund, monthly amount
- Simple rules that match the answers to a type of ready-made fund
- A plain-English explanation (a template for now)
- A compound growth calculator comparing investing with cash

## Ideas for the next version

- Train a machine learning model (decision tree) to group similar customers, replacing the rules
- Plain-English chat with an LLM, answering only from approved fund documents
- Guardrails that block promises of returns or single-share tips
- Use bank data (with consent) to suggest a comfortable monthly amount
- Payday nudges, goal tracking and calm market updates
- Privacy and security testing

## Run it

```
pip install streamlit pandas
streamlit run app.py
```

All examples are illustrative and not financial advice.
