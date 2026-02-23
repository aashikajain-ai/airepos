def compute_financial_health(profile):
    if not profile.monthly_income or profile.monthly_income <= 0:
        return 0

    income = max(0, profile.monthly_income)
    expenses = max(0, profile.monthly_expenses or 0)
    savings = max(0, profile.savings or 0)
    debts = max(0, profile.debts or 0)
    credit_score = profile.credit_score or 300

    expense_ratio = min(1.0, expenses / income)
    savings_ratio = min(1.0, savings / (income * 6))
    debt_ratio = min(1.0, debts / (income * 12))
    credit_ratio = max(0.0, min(1.0, (credit_score - 300) / 550))

    score = (
        (1 - expense_ratio) * 35 +
        savings_ratio * 25 +
        (1 - debt_ratio) * 25 +
        credit_ratio * 15
    )

    return int(round(max(0, min(100, score))))


def recommendations_from_score(score, profile):
    recommendations = []

    if score >= 80:
        return ["Your financial health is strong. Keep maintaining your progress."]

    if profile.monthly_expenses > profile.monthly_income * 0.7:
        recommendations.append("Reduce discretionary spending to improve your expense ratio.")

    if profile.savings < profile.monthly_income * 3:
        recommendations.append("Build an emergency fund covering at least 3–6 months of expenses.")

    if profile.debts > profile.monthly_income * 6:
        recommendations.append("Prioritize high-interest debt repayment.")

    if profile.credit_score < 650:
        recommendations.append("Improve your credit score with timely payments and lower utilization.")

    return recommendations