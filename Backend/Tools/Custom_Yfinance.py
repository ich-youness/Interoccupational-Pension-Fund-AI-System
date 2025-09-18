import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional, Any, Union

class CustomYFinanceTools:
    """Custom yfinance tools for bond credit monitoring and analysis"""
    
    def __init__(self):
        self.benchmark_cache = {}
    
    def get_bond_data(self, ticker: str, period: str = "1y") -> Dict[str, Any]:
        """
        Get comprehensive bond/issuer data including prices, yields, and fundamentals
        
        Args:
            ticker: Bond or issuer ticker symbol
            period: Time period for historical data (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
        Returns:
            Dictionary with bond data, yields, spreads, and fundamentals
        """
        try:
            # Get ticker data
            ticker_obj = yf.Ticker(ticker)
            
            # Historical data
            hist = ticker_obj.history(period=period)
            
            # Company info and fundamentals
            info = ticker_obj.info
            
            # Financial statements
            financials = self._get_financials(ticker_obj)
            
            # Calculate key metrics
            current_price = hist['Close'].iloc[-1] if not hist.empty else None
            prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else None
            price_change_pct = ((current_price - prev_price) / prev_price * 100) if prev_price else None
            
            # Calculate yield if available
            yield_data = self._calculate_yield_metrics(hist, info)
            
            return {
                "ticker": ticker,
                "current_price": current_price,
                "price_change_pct": price_change_pct,
                "historical_data": {
                    "period": period,
                    "data_points": len(hist),
                    "price_series": hist['Close'].tolist() if not hist.empty else []
                },
                "yield_metrics": yield_data,
                "fundamentals": financials,
                "company_info": {
                    "name": info.get('longName', info.get('shortName', ticker)),
                    "sector": info.get('sector', 'Unknown'),
                    "industry": info.get('industry', 'Unknown'),
                    "market_cap": info.get('marketCap'),
                    "country": info.get('country', 'Unknown')
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to get data for {ticker}: {str(e)}"}
    
    def get_historical_volatility(self, ticker: str, lookback_days: int = 90) -> Dict[str, Any]:
        """
        Calculate historical volatility for a given ticker
        
        Args:
            ticker: Bond or issuer ticker
            lookback_days: Number of days to calculate volatility
        
        Returns:
            Volatility metrics
        """
        try:
            # Get historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=lookback_days)
            
            hist = yf.download(ticker, start=start_date, end=end_date)
            
            if hist.empty:
                return {"error": f"No historical data for {ticker}"}
            
            # Calculate daily returns
            returns = hist['Close'].pct_change().dropna()
            
            # Calculate volatility (annualized)
            daily_volatility = returns.std()
            annualized_volatility = daily_volatility * np.sqrt(252)
            
            # Calculate max drawdown
            cumulative_returns = (1 + returns).cumprod()
            peak = cumulative_returns.expanding(min_periods=1).max()
            drawdown = (cumulative_returns - peak) / peak
            max_drawdown = drawdown.min()
            
            return {
                "ticker": ticker,
                "lookback_days": lookback_days,
                "daily_volatility": float(daily_volatility),
                "annualized_volatility": float(annualized_volatility),
                "max_drawdown": float(max_drawdown),
                "average_daily_return": float(returns.mean()),
                "data_points": len(returns),
                "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            }
            
        except Exception as e:
            return {"error": f"Failed to calculate volatility for {ticker}: {str(e)}"}
    
    def calculate_spread_vs_benchmark(self, bond_ticker: str, benchmark_ticker: str = "^TNX", 
                                    lookback_days: int = 30) -> Dict[str, Any]:
        """
        Calculate yield spread vs benchmark (e.g., Treasury)
        
        Args:
            bond_ticker: Bond ticker symbol
            benchmark_ticker: Benchmark ticker (default: 10-year Treasury ^TNX)
            lookback_days: Lookback period for spread calculation
        
        Returns:
            Spread metrics and comparison data
        """
        try:
            # Get bond data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=lookback_days)
            
            bond_data = yf.download(bond_ticker, start=start_date, end=end_date)
            benchmark_data = yf.download(benchmark_ticker, start=start_date, end=end_date)
            
            if bond_data.empty or benchmark_data.empty:
                return {"error": "Missing data for spread calculation"}
            
            # Align dates
            common_dates = bond_data.index.intersection(benchmark_data.index)
            bond_aligned = bond_data.loc[common_dates]
            benchmark_aligned = benchmark_data.loc[common_dates]
            
            # Calculate spread (assuming bond yield is in price data - adjust as needed)
            # For bonds, you might need to get yield data differently
            spread = bond_aligned['Close'] - benchmark_aligned['Close']
            
            current_spread = spread.iloc[-1] if len(spread) > 0 else None
            avg_spread = spread.mean()
            max_spread = spread.max()
            min_spread = spread.min()
            
            return {
                "bond_ticker": bond_ticker,
                "benchmark_ticker": benchmark_ticker,
                "current_spread_bps": float(current_spread * 100) if current_spread else None,  # Convert to basis points
                "average_spread_bps": float(avg_spread * 100),
                "max_spread_bps": float(max_spread * 100),
                "min_spread_bps": float(min_spread * 100),
                "spread_volatility": float(spread.std() * 100),
                "lookback_days": lookback_days,
                "data_points": len(spread),
                "spread_series": spread.tolist()
            }
            
        except Exception as e:
            return {"error": f"Failed to calculate spread: {str(e)}"}
    
    def get_issuer_fundamentals(self, ticker: str) -> Dict[str, Any]:
        """
        Get fundamental financial ratios for credit analysis
        
        Args:
            ticker: Company ticker symbol
        
        Returns:
            Dictionary with financial ratios and fundamentals
        """
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info
            
            # Extract key financial ratios for credit analysis
            fundamentals = {
                "debt_to_equity": info.get('debtToEquity'),
                "current_ratio": info.get('currentRatio'),
                "quick_ratio": info.get('quickRatio'),
                "return_on_equity": info.get('returnOnEquity'),
                "return_on_assets": info.get('returnOnAssets'),
                "profit_margins": info.get('profitMargins'),
                "operating_margins": info.get('operatingMargins'),
                "ebitda": info.get('ebitda'),
                "total_debt": info.get('totalDebt'),
                "total_cash": info.get('totalCash'),
                "free_cash_flow": info.get('freeCashflow'),
                "operating_cash_flow": info.get('operatingCashflow'),
                "revenue_growth": info.get('revenueGrowth'),
                "earnings_growth": info.get('earningsGrowth'),
                "interest_coverage": self._calculate_interest_coverage(info),
                "debt_to_ebitda": self._calculate_debt_to_ebitda(info)
            }
            
            # Clean None values
            fundamentals = {k: v for k, v in fundamentals.items() if v is not None}
            
            return {
                "ticker": ticker,
                "fundamentals": fundamentals,
                "as_of_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to get fundamentals for {ticker}: {str(e)}"}
    
    def get_multiple_issuers_data(self, tickers: List[str], period: str = "3mo") -> Dict[str, Any]:
        """
        Get data for multiple issuers simultaneously
        
        Args:
            tickers: List of ticker symbols
            period: Historical period
        
        Returns:
            Dictionary with data for all issuers
        """
        results = {}
        for ticker in tickers:
            results[ticker] = self.get_bond_data(ticker, period)
        
        return {
            "issuers": results,
            "timestamp": datetime.now().isoformat(),
            "total_issuers": len(tickers)
        }
    
    def _get_financials(self, ticker_obj) -> Dict[str, Any]:
        """Extract financial statements data"""
        try:
            financials = {
                "balance_sheet": ticker_obj.balance_sheet.iloc[:, 0].to_dict() if hasattr(ticker_obj, 'balance_sheet') and not ticker_obj.balance_sheet.empty else {},
                "income_statement": ticker_obj.financials.iloc[:, 0].to_dict() if hasattr(ticker_obj, 'financials') and not ticker_obj.financials.empty else {},
                "cash_flow": ticker_obj.cashflow.iloc[:, 0].to_dict() if hasattr(ticker_obj, 'cashflow') and not ticker_obj.cashflow.empty else {}
            }
            return financials
        except:
            return {}
    
    def _calculate_yield_metrics(self, hist_data: pd.DataFrame, info: Dict) -> Dict[str, Any]:
        """Calculate yield-related metrics"""
        try:
            if hist_data.empty:
                return {}
            
            current_price = hist_data['Close'].iloc[-1]
            prev_price = hist_data['Close'].iloc[-2] if len(hist_data) > 1 else current_price
            
            # Simple yield calculation (adjust based on actual bond data availability)
            # For bonds, you might have actual yield data in info or need different calculation
            yield_value = info.get('yield', None)
            if yield_value is None and 'trailingAnnualDividendYield' in info:
                yield_value = info['trailingAnnualDividendYield']
            
            return {
                "current_yield": yield_value,
                "yield_change": None,  # Would need previous yield data
                "current_price": current_price,
                "price_change": current_price - prev_price
            }
        except:
            return {}
    
    def _calculate_interest_coverage(self, info: Dict) -> Optional[float]:
        """Calculate interest coverage ratio"""
        try:
            ebit = info.get('ebit')
            interest_expense = info.get('interestExpense')
            if ebit and interest_expense and interest_expense != 0:
                return ebit / interest_expense
            return None
        except:
            return None
    
    def _calculate_debt_to_ebitda(self, info: Dict) -> Optional[float]:
        """Calculate debt to EBITDA ratio"""
        try:
            total_debt = info.get('totalDebt')
            ebitda = info.get('ebitda')
            if total_debt and ebitda and ebitda != 0:
                return total_debt / ebitda
            return None
        except:
            return None

# Example usage and test function
def test_yfinance_tools():
    """Test the CustomYFinanceTools class"""
    tools = CustomYFinanceTools()
    
    # Test single issuer data
    print("Testing single issuer data...")
    result = tools.get_bond_data("AAPL", "3mo")
    print(f"AAPL data: {json.dumps(result, indent=2, default=str)}")
    
    # Test volatility calculation
    print("\nTesting volatility calculation...")
    vol_result = tools.get_historical_volatility("AAPL", 90)
    print(f"AAPL volatility: {json.dumps(vol_result, indent=2)}")
    
    # Test fundamentals
    print("\nTesting fundamentals...")
    fund_result = tools.get_issuer_fundamentals("AAPL")
    print(f"AAPL fundamentals: {json.dumps(fund_result, indent=2)}")
    
    # Test multiple issuers
    print("\nTesting multiple issuers...")
    multi_result = tools.get_multiple_issuers_data(["AAPL", "MSFT", "GOOGL"])
    print(f"Multiple issuers: Found data for {multi_result['total_issuers']} issuers")

# if __name__ == "__main__":
#     test_yfinance_tools()