import pandas as pd
from fpdf import FPDF
import smtplib
from email.mime.text import MIMEText

class BudgetManager:
    def _init_(self):
        self.budgets = {}  # Category budget limits
        self.expenses = pd.DataFrame(columns=["Category", "Amount", "Description", "Date"])

    def set_budget(self, category, amount):
        self.budgets[category] = amount
        print(f"Budget set: {category} -> {amount}")

    def add_expense(self, category, amount, description, date):
        # Add the expense to the DataFrame
        self.expenses = self.expenses.append(
            {"Category": category, "Amount": amount, "Description": description, "Date": date},
            ignore_index=True,
        )
        print(f"Expense added: {category} -> {amount}")

        # Check and trigger alert if budget exceeds
        self.check_budget(category)

    def check_budget(self, category):
        total_spent = self.expenses[self.expenses["Category"] == category]["Amount"].sum()
        budget = self.budgets.get(category, None)

        if budget and total_spent >= budget:
            print(f"ALERT: {category} has exceeded its budget! (Spent: {total_spent}, Limit: {budget})")
            # Add email notification trigger here if needed.

    def generate_excel_report(self, filename="Budget_Report.xlsx"):
        self.expenses.to_excel(filename, index=False)
        print(f"Excel report generated: {filename}")

    def generate_pdf_report(self, filename="Budget_Report.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Budget Report", ln=True, align="C")

        for i, row in self.expenses.iterrows():
            pdf.cell(200, 10, txt=f"{row['Category']}: {row['Amount']} - {row['Description']} on {row['Date']}", ln=True)

        pdf.output(filename)
        print(f"PDF report generated: {filename}")

# Example Usage
if _name_ == "_main_":
    bm = BudgetManager()

    # Set budgets
    bm.set_budget("Food", 500)
    bm.set_budget("Entertainment", 300)

    # Add expenses
    bm.add_expense("Food", 200, "Groceries", "2024-06-27")
    bm.add_expense("Food", 350, "Dinner", "2024-06-28")  # Exceeds budget
    bm.add_expense("Entertainment", 150, "Movies", "2024-06-29")

    # Generate reports
    bm.generate_excel_report()
    bm.generate_pdf_report()