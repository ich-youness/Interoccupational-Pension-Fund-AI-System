import json
import math
from typing import Dict, Any
from agno.tools import tool
import numpy as np

@tool(name="present_value_calculator", description="Calculate the present value of liabilities.")
def present_value_calculator(data: Dict[str, Any]) -> str:
    """
    Discount future cashflows to present value using given discount rate.
    Input: JSON with liabilities.cashflows and liabilities.discount_rate.
    Output: JSON with total present value.
    """
    cashflows = data["liabilities"]["cashflows"]
    discount_rate = data["liabilities"]["discount_rate"]
    pv = sum(v / ((1 + discount_rate) ** (i+1)) for i, v in enumerate(cashflows.values()))
    return json.dumps({"present_value": pv})


@tool(name="portfolio_statistics", description="Compute portfolio expected return and variance.")
def portfolio_statistics(data: Dict[str, Any]) -> str:
    """
    Compute portfolio return and variance from asset allocation, returns, volatilities, correlations.
    """
    allocation = data["assets"]["current_allocation"]
    returns = data["assets"]["expected_returns"]
    vol = data["assets"]["volatility"]
    corr = data["assets"]["correlations"]

    # Expected return
    expected_return = sum(allocation[a] * returns[a] for a in allocation)

    # Build covariance matrix
    assets = list(allocation.keys())
    cov_matrix = {a: {b: 0.0 for b in assets} for a in assets}
    for i in assets:
        for j in assets:
            if i == j:
                cov_matrix[i][j] = vol[i] ** 2
            else:
                corr_val = corr.get(i, {}).get(j, corr.get(j, {}).get(i, 0))
                cov_matrix[i][j] = corr_val * vol[i] * vol[j]

    # Portfolio variance
    variance = 0.0
    for i in assets:
        for j in assets:
            variance += allocation[i] * allocation[j] * cov_matrix[i][j]

    return json.dumps({
        "expected_return": expected_return,
        "variance": variance,
        "std_dev": math.sqrt(variance)
    })


@tool(name="simple_optimizer", description="Suggests an optimized allocation under constraints.")
def simple_optimizer(data: Dict[str, Any]) -> str:
    """
    Suggests a basic allocation by shifting more weight to higher-return assets,
    while respecting min/max constraints.
    """
    returns = data["assets"]["expected_returns"]
    allocation = data["assets"]["current_allocation"].copy()
    min_alloc = data["constraints"]["min_allocation"]
    max_alloc = data["constraints"]["max_allocation"]

    # Sort assets by expected return
    sorted_assets = sorted(returns.items(), key=lambda x: x[1], reverse=True)

    # Reallocate slightly towards higher-return assets
    for asset, _ in sorted_assets:
        if allocation[asset] < max_alloc.get(asset, 1.0):
            allocation[asset] = min(allocation[asset] + 0.05, max_alloc.get(asset, 1.0))

    # Adjust to keep sum = 1
    total = sum(allocation.values())
    allocation = {k: v/total for k, v in allocation.items()}

    return json.dumps({"recommended_allocation": allocation})


@tool(name="stress_tester", description="Run stress tests on the portfolio.")
def stress_tester(data: Dict[str, Any]) -> str:
    """
    Apply shocks to expected returns and recompute portfolio return.
    """
    allocation = data["assets"]["current_allocation"]
    returns = data["assets"]["expected_returns"]
    scenarios = data["scenarios"]

    results = {}
    for scenario, impacts in scenarios.items():
        if isinstance(impacts, dict):  # Market crash type
            stressed_returns = {
                a: returns[a] + impacts.get(a, 0)
                for a in allocation
            }
        else:
            stressed_returns = {a: returns[a] for a in allocation}
        portfolio_return = sum(allocation[a] * stressed_returns[a] for a in allocation)
        results[scenario] = portfolio_return

    return json.dumps({"stress_test_results": results})


### OPCI Tools

import json
from typing import Dict, Any
from agno.tools import tool

@tool(
    name="opci_optimizer",
    description="Optimizes OPCI allocation based on constraints and market data."
)
def opci_optimizer(data: Dict[str, Any]) -> str:
    """
    Optimize the OPCI real estate allocation.

    Args:
        data (dict): JSON input with 'portfolio', 'constraints', and 'market_data'.

    Returns:
        str: JSON string with optimized weights and recommendations.
    """
    portfolio = data.get("portfolio", {})
    constraints = data.get("constraints", {})
    market_data = data.get("market_data", {})

    # Placeholder: naive optimization logic
    assets = portfolio.get("properties", [])
    total_value = sum(a["value"] for a in assets)

    # Initialize weights proportional to current value
    optimized_allocation = {}
    for a in assets:
        optimized_allocation[a["id"]] = a["value"] / total_value

    # Example adjustment based on simple rules
    recommendations = []
    for a in assets:
        if a.get("vacancy_rate", 0) > constraints.get("max_vacancy", 0.1):
            recommendations.append(
                f"Consider reducing exposure to {a['id']} due to high vacancy ({a['vacancy_rate']*100:.1f}%)."
            )
        if a.get("yield", 0) < constraints.get("min_yield", 0.05):
            recommendations.append(
                f"Consider reallocating {a['id']} for better yield ({a['yield']*100:.1f}%)."
            )

    result = {
        "optimized_allocation": optimized_allocation,
        "recommendations": recommendations
    }

    return json.dumps(result)


@tool(
    name="scenario_stress_tester",
    description="Runs stress tests on the OPCI portfolio under different scenarios."
)
def scenario_stress_tester(data: Dict[str, Any]) -> str:
    """
    Apply scenario shocks (vacancy/yield changes) to the OPCI portfolio.

    Args:
        data (dict): JSON with 'portfolio' and 'scenarios'.

    Returns:
        str: JSON with stressed portfolio performance.
    """
    portfolio = data.get("portfolio", {})
    scenarios = data.get("scenarios", [])

    stress_results = []

    for scenario in scenarios:
        shocked_yield_total = 0
        shocked_vacancy_total = 0
        properties = portfolio.get("properties", [])
        for prop in properties:
            # Apply scenario shocks if provided
            yield_shock = scenario.get(f"shock_{prop['type']}", 0)
            vacancy_shock = scenario.get(f"vacancy_shock_{prop['type']}", 0)
            shocked_yield_total += prop.get("yield", 0) + yield_shock
            shocked_vacancy_total += prop.get("vacancy_rate", 0) + vacancy_shock

        # Compute averages
        n_props = len(properties) if properties else 1
        stress_results.append({
            "scenario": scenario.get("name", "Unnamed Scenario"),
            "average_yield": shocked_yield_total / n_props,
            "average_vacancy": shocked_vacancy_total / n_props
        })

    return json.dumps({"stress_results": stress_results})


### RebalancingAI tools


@tool(name="calculate_deviation", description="Calculate deviations between current and target allocations.")
def calculate_deviation(data: Dict[str, Any]) -> str:
    """
    Input JSON:
    {
        "current_portfolio": {"equities": 0.55, "bonds": 0.35, "commodities": 0.10},
        "target_allocation": {"equities": 0.50, "bonds": 0.40, "commodities": 0.10}
    }
    Output JSON:
    {"deviation": {"equities": 0.05, "bonds": -0.05, "commodities": 0.0}}
    """
    current = data["current_portfolio"]
    target = data["target_allocation"]
    deviation = {k: round(current[k] - target.get(k, 0.0), 4) for k in current}
    return json.dumps({"deviation": deviation})


@tool(name="rebalance_portfolio", description="Suggest rebalancing trades based on deviation, constraints, and market data.")
def rebalance_portfolio(data: Dict[str, Any]) -> str:
    """
    Input JSON includes:
    - current_portfolio
    - target_allocation
    - market_data (liquidity, transaction_costs)
    - constraints (max_trade_percentage)
    
    Output JSON includes:
    - rebalance_plan
    - estimated_risk_metrics
    - summary
    """
    deviation = {k: data["current_portfolio"][k] - data["target_allocation"].get(k, 0.0)
                 for k in data["current_portfolio"]}
    max_trade = data.get("constraints", {}).get("max_trade_percentage", 0.1)
    
    rebalance_plan = {}
    for asset, diff in deviation.items():
        if abs(diff) < 0.001:
            action = "hold"
            amount = 0.0
        elif diff > 0:
            action = "sell"
            amount = min(diff, max_trade)
        else:
            action = "buy"
            amount = min(-diff, max_trade)
        rebalance_plan[asset] = {"action": action, "amount": round(amount, 4)}
    
    # Mock risk metrics (can be replaced with real calculation)
    risk_metrics = {"VaR": 0.045, "volatility": 0.095}
    
    summary = "Suggested trades to move portfolio closer to target allocation within constraints. Minimal market impact expected."
    
    return json.dumps({
        "rebalance_plan": rebalance_plan,
        "risk_metrics": risk_metrics,
        "summary": summary
    })


############################ 2end Module

@tool(name="parametric_var_calculator", description="Compute parametric Value at Risk (VaR) for a portfolio.")
def parametric_var_calculator(data: Dict[str, Any]) -> str:
    """
    Input JSON:
    {
        "portfolio": {asset: {"weight": float, "price": float, "volatility": float}, ...},
        "confidence_level": 0.95,
        "time_horizon_days": 1,
        "correlations": { "asset1-asset2": float, ... }
    }
    Output JSON:
    {
        "VaR": float,
        "asset_contributions": {asset: float, ...},
        "summary": str
    }
    """
    portfolio = data["portfolio"]
    confidence = data.get("confidence_level", 0.95)
    horizon = data.get("time_horizon_days", 1)
    
    assets = list(portfolio.keys())
    weights = np.array([portfolio[a]["weight"] for a in assets])
    volatilities = np.array([portfolio[a]["volatility"] for a in assets])
    
    # Build correlation matrix
    corr_matrix = np.eye(len(assets))
    for i, a1 in enumerate(assets):
        for j, a2 in enumerate(assets):
            if i < j:
                key = f"{a1}-{a2}"
                rev_key = f"{a2}-{a1}"
                corr = data.get("correlations", {}).get(key, data.get("correlations", {}).get(rev_key, 0))
                corr_matrix[i, j] = corr
                corr_matrix[j, i] = corr
    
    cov_matrix = np.outer(volatilities, volatilities) * corr_matrix
    portfolio_var = weights.T @ cov_matrix @ weights
    portfolio_std = np.sqrt(portfolio_var) * np.sqrt(horizon)
    z_score = -1 * np.percentile(np.random.normal(0, 1, 100000), (1-confidence)*100)
    VaR = round(portfolio_std * z_score * sum([portfolio[a]["price"] for a in assets]), 2)
    
    # Asset contributions (approximate)
    asset_contributions = {a: round(weights[i] * portfolio_std * portfolio[a]["price"], 2) for i, a in enumerate(assets)}
    
    summary = f"{horizon}-day {int(confidence*100)}% VaR indicates a potential loss of {VaR} DH. Major contributors: {', '.join(assets)}."
    
    return json.dumps({
        "VaR": VaR,
        "asset_contributions": asset_contributions,
        "summary": summary
    })

@tool(name="apply_stress_scenarios", description="Apply predefined stress scenarios to a portfolio and compute losses.")
def apply_stress_scenarios(data: Dict[str, Any]) -> str:
    """
    Apply stress shocks to portfolio allocations and compute portfolio losses.
    Input JSON:
    {
      "portfolio": {"MASI": {"weight":0.3,"value":1.5e9}, "Gov10Y": {"weight":0.4,"value":2e9}},
      "scenarios": [
        {"name":"Market Crash","equity_drop":0.3,"bond_drop":0.05},
        {"name":"Interest Rate Spike","equity_drop":0.1,"bond_drop":0.2}
      ]
    }
    Output JSON:
    {
      "scenario_results": [
        {"name":"Market Crash","portfolio_loss":1.2e6,"alert":true,"recommendation":"Reduce equity exposure"},
        {"name":"Interest Rate Spike","portfolio_loss":0.6e6,"alert":false,"recommendation":"Monitor bonds"}
      ]
    }
    """
    portfolio = data["portfolio"]
    scenarios = data["scenarios"]

    results = []
    total_value = sum(asset["value"] for asset in portfolio.values())

    for sc in scenarios:
        # Apply shocks
        equity_loss = sum(
            asset["value"] * sc.get("equity_drop", 0)
            for k, asset in portfolio.items()
            if "MASI" in k or "EQ" in k.upper()
        )
        bond_loss = sum(
            asset["value"] * sc.get("bond_drop", 0)
            for k, asset in portfolio.items()
            if "BOND" in k.upper() or "Gov" in k or "Corp" in k
        )
        total_loss = equity_loss + bond_loss
        loss_pct = total_loss / total_value

        # Alert if losses exceed 10% of portfolio value
        alert = loss_pct > 0.1

        recommendation = (
            "Reduce equity exposure, increase liquid bonds"
            if alert
            else "No immediate action required, monitor exposures"
        )

        results.append(
            {
                "name": sc["name"],
                "portfolio_loss": total_loss,
                "alert": alert,
                "recommendation": recommendation,
            }
        )

    return json.dumps({"scenario_results": results})

import json
from typing import Dict, Any
from agno.tools import tool

@tool(name="longevity_shift_calculator", description="Quantify the impact of longevity shifts (+1, +2, +3 years life expectancy) on liabilities.")
def longevity_shift_calculator(data: Dict[str, Any]) -> str:
    """
    Simulates the effect of longevity improvements on pension liabilities.
    Input JSON must include liabilities.annual_benefits, liabilities.discount_rate, 
    baseline_liabilities, and scenarios.longevity_shift.
    
    Output: JSON with adjusted liabilities for each longevity shift.
    """
    baseline = data["liabilities"]["baseline"]
    annual_benefits = data["liabilities"]["annual_benefits"]
    discount_rate = data["liabilities"]["discount_rate"]
    shifts = data["scenarios"]["longevity_shift"]

    results = {}
    for s in shifts:
        # Simplified model: extend payments by `s` years
        extra = sum(annual_benefits / ((1 + discount_rate) ** (i+1)) for i in range(s))
        results[f"longevity_shift_+{s}"] = baseline + extra

    return json.dumps(results)


@tool(name="mortality_shock_calculator", description="Apply shocks to mortality rates and estimate their impact on liabilities.")
def mortality_shock_calculator(data: Dict[str, Any]) -> str:
    """
    Applies mortality shocks (e.g., -5%, -10%) meaning people die less often, 
    hence longer payouts. Recomputes liabilities accordingly.
    
    Input JSON must include liabilities.baseline and scenarios.mortality_shock.
    Output JSON with adjusted liabilities for each mortality shock.
    """
    baseline = data["liabilities"]["baseline"]
    shocks = data["scenarios"]["mortality_shock"]

    results = {}
    for shock in shocks:
        # Assume liabilities increase proportionally to mortality improvement
        adjusted = baseline * (1 + abs(shock) / 100 * 0.5)  # sensitivity factor 0.5
        results[f"mortality_shock_{shock}%"] = adjusted

    return json.dumps(results)
