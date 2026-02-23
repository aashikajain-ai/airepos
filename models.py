from dataclasses import dataclass

@dataclass
class FinancialProfile:
    monthly_income: float = 0.0
    monthly_expenses: float = 0.0
    savings: float = 0.0
    debts: float = 0.0
    credit_score: int = 0
