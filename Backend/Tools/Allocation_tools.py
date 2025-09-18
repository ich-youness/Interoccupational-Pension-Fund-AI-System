import json
import math
from typing import Dict, Any
from agno.tools import tool


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
