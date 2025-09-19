# CIMR-OS Modular Architecture

This directory contains the refactored CIMR-OS modules with improved encapsulation, reusability, testability, scalability, and custom initialization capabilities.

## Architecture Overview

The refactored modules follow a modular architecture pattern with the following key components:

### Base Classes (`base/`)
- **`BaseAgent`**: Abstract base class for all agents
- **`BaseModule`**: Abstract base class for all modules
- **`AgentConfig`**: Configuration class for agent initialization
- **`ModuleConfig`**: Configuration class for module initialization
- **`DataManager`**: Utility class for data management

### Configuration Management (`config/`)
- **`module_configs.py`**: Centralized configuration definitions for all modules
- Supports custom configuration overrides
- Environment-based configuration management

### Module Factory (`factory/`)
- **`module_factory.py`**: Factory pattern for creating and managing modules
- Centralized module instantiation
- Agent registry and discovery

### Refactored Modules (`modules/`)
- **`acaps_compliance_module.py`**: ACAPS regulatory compliance
- **`member_relations_module.py`**: Member relationship management
- **`financial_risk_module.py`**: Financial risk management
- **`actuarial_projections_module.py`**: Actuarial projections and analysis
- **`allocation_optimization_module.py`**: Portfolio allocation optimization

### Testing Infrastructure (`tests/`)
- **`test_base.py`**: Base test classes and utilities
- Mock implementations for testing
- Comprehensive test coverage

### Examples (`examples/`)
- **`usage_examples.py`**: Comprehensive usage examples
- Best practices demonstration
- Error handling examples

## Key Improvements

### 1. Encapsulation
- Each agent is encapsulated in its own class
- Clear separation of concerns
- Private methods and protected attributes
- Consistent interface across all agents

### 2. Reusability
- Base classes provide common functionality
- Configuration-driven initialization
- Modular design allows easy composition
- Shared utilities and tools

### 3. Testability
- Mock implementations for all components
- Isolated unit tests
- Dependency injection support
- Comprehensive test coverage

### 4. Scalability
- Factory pattern for easy extension
- Plugin architecture for new agents
- Configuration-based scaling
- Lazy loading of components

### 5. Custom Initialization
- Flexible configuration system
- Environment variable support
- Runtime configuration overrides
- Multiple initialization patterns

## Usage Examples

### Basic Usage

```python
from Modules.factory.module_factory import create_module

# Create a module
acaps_module = create_module("ACAPS_Compliance")

# Get available agents
agents = acaps_module.list_agents()

# Use a specific agent
reporter_agent = acaps_module.get_agent("ACAPSReporter")
result = reporter_agent.generate_report()
```

### Custom Configuration

```python
# Custom configuration
custom_config = {
    "agents": {
        "ACAPSReporter": {
            "model_id": "grok-3-mini",
            "api_key": "custom_key",
            "add_history_to_context": True
        }
    }
}

# Create module with custom config
acaps_module = create_module("ACAPS_Compliance", custom_config)
```

### Direct Module Instantiation

```python
from Modules.modules.acaps_compliance_module import ACAPSComplianceModule
from Modules.config.module_configs import get_acaps_compliance_config

# Get configuration
config = get_acaps_compliance_config()

# Create module
module = ACAPSComplianceModule(config)
```

### Error Handling

```python
try:
    # Create module
    module = create_module("ACAPS_Compliance")
    
    # Use agent
    agent = module.get_agent("ACAPSReporter")
    if agent:
        result = agent.generate_report()
    else:
        print("Agent not found")
        
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Module-Specific Usage

### ACAPS Compliance Module

```python
# Generate compliance report
report = acaps_module.generate_compliance_report("ACAPSReporter")

# Monitor compliance
status = acaps_module.generate_compliance_report("ComplianceMonitor")

# Validate data
validation = acaps_module.validate_data(data, "compliance")
```

### Member Relations Module

```python
# Handle member inquiry
response = member_module.handle_member_inquiry("How do I check my pension?")

# Calculate pension projection
projection = member_module.calculate_pension_projection(member_data)

# Detect fraud
fraud_check = member_module.detect_fraud(member_data)
```

### Financial Risk Management Module

```python
# Calculate VaR
var_result = risk_module.calculate_portfolio_var(portfolio_data, 0.95, 1)

# Run stress test
stress_result = risk_module.run_stress_analysis(portfolio_data, ["market_crash"])

# Monitor credit risk
credit_result = risk_module.monitor_credit_risk(["MAR_GOV_10Y", "BCP_CORP_BOND"])
```

### Actuarial Projections Module

```python
# Project demographics
demographics = actuarial_module.project_demographics("Morocco", 80)

# Calculate pension benefits
benefits = actuarial_module.calculate_pension_benefits(member_data)

# Optimize reserves
reserves = actuarial_module.optimize_reserve_levels(reserve_data)
```

### Allocation Optimization Module

```python
# Optimize portfolio
optimization = allocation_module.optimize_portfolio_allocation(portfolio_data)

# Analyze OPCI
opci_analysis = allocation_module.analyze_opci_portfolio(opci_data)

# Get market analysis
market_analysis = allocation_module.get_moroccan_market_analysis()

# Rebalance portfolio
rebalance = allocation_module.rebalance_portfolio(portfolio_data)
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest Modules/tests/

# Run specific test file
python -m pytest Modules/tests/test_base.py

# Run with coverage
python -m pytest Modules/tests/ --cov=Modules
```

### Writing Tests

```python
from Modules.tests.test_base import BaseAgentTest, MockDataProvider

class TestACAPSReporter(BaseAgentTest):
    def test_generate_report(self):
        # Test report generation
        agent = self.get_agent("ACAPSReporter")
        result = agent.generate_report()
        self.assertIsNotNone(result)
    
    def test_validate_compliance(self):
        # Test compliance validation
        data = MockDataProvider.get_sample_compliance_data()
        agent = self.get_agent("ACAPSReporter")
        result = agent.validate_compliance(data)
        self.assertIsNotNone(result)
```

## Configuration

### Environment Variables

```bash
# Required
export XAI_API_KEY="your_api_key_here"

# Optional
export CIMR_DB_FILE="tmp/agno.db"
export CIMR_LOG_LEVEL="INFO"
```

### Configuration Files

Configuration can be customized by modifying the files in `config/` or by passing custom configuration dictionaries to the factory methods.

## Error Handling

The refactored modules include comprehensive error handling:

- **Configuration Errors**: Invalid module/agent names, missing required parameters
- **Runtime Errors**: Agent initialization failures, tool execution errors
- **Data Errors**: Invalid input data, missing files
- **Network Errors**: API connection issues, timeout errors

## Logging

All modules include structured logging:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CIMR-OS")

# Logs are automatically generated for:
# - Module initialization
# - Agent creation
# - Request processing
# - Error conditions
```

## Performance Considerations

- **Lazy Loading**: Agents are created only when needed
- **Connection Pooling**: Database connections are reused
- **Caching**: Configuration and data can be cached
- **Async Support**: Future enhancement for async operations

## Migration from Original Modules

The refactored modules maintain backward compatibility with the original agent interfaces while providing additional functionality:

1. **Import Changes**: Update imports to use the new module structure
2. **Configuration**: Use the new configuration system
3. **Error Handling**: Implement proper error handling
4. **Testing**: Add comprehensive tests

## Future Enhancements

- **Async Support**: Full async/await support
- **Plugin System**: Dynamic agent loading
- **Metrics**: Performance monitoring and metrics
- **API Gateway**: REST API for module access
- **Docker Support**: Containerized deployment
- **CI/CD**: Automated testing and deployment

## Contributing

When adding new modules or agents:

1. Follow the established patterns
2. Add comprehensive tests
3. Update documentation
4. Include usage examples
5. Follow error handling conventions

## Support

For questions or issues:

1. Check the examples in `examples/`
2. Review the test cases in `tests/`
3. Consult the configuration files in `config/`
4. Check the base classes in `base/`
