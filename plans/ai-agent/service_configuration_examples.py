"""
Service Configuration Examples for Dynamic ValidationManager.

This module demonstrates how different services configure the ValidationManager
with exactly the validation capabilities they need using the provider pattern
and dynamic method registration.
"""

import logging
from typing import Dict, List

from validation.managers.validation_manager import ValidationManager
from validation.providers.xml_validation_provider import (
    register_xml_validation,
    register_json_validation,
    register_common_validation_methods,
)
from validation.providers.agent_governance_provider import register_agent_governance_validation

logger = logging.getLogger(__name__)


# Example 1: Basic Service - Only needs XML validation
def configure_basic_service() -> ValidationManager:
    """
    Configure ValidationManager for a basic service that only needs XML validation.
    
    This represents a simple service like a document processing service
    that only validates XML documents against schemas.
    
    Returns:
        ValidationManager: Configured with XML validation only
    """
    logger.info("Configuring basic service validation manager")
    
    # Create generic ValidationManager
    validation_manager = ValidationManager("document_processing_service")
    
    # Add only XML validation capability
    register_xml_validation(validation_manager)
    
    logger.info("Basic service configured with XML validation")
    return validation_manager


# Example 2: Web Service - Needs both XML and JSON validation
def configure_web_service() -> ValidationManager:
    """
    Configure ValidationManager for a web service that handles both XML and JSON.
    
    This represents a typical web service that processes both XML documents
    and JSON API requests.
    
    Returns:
        ValidationManager: Configured with XML and JSON validation
    """
    logger.info("Configuring web service validation manager")
    
    # Create generic ValidationManager
    validation_manager = ValidationManager("web_api_service")
    
    # Add common validation methods (both XML and JSON)
    register_common_validation_methods(validation_manager)
    
    logger.info("Web service configured with XML and JSON validation")
    return validation_manager


# Example 3: AI Agent Trading Service - Needs comprehensive validation
def configure_trading_service() -> ValidationManager:
    """
    Configure ValidationManager for an AI agent trading service.
    
    This represents a sophisticated AI agent service that needs:
    - Agent governance validation (LTL contract checking)
    - XML validation (for market data feeds)
    - JSON validation (for API requests/responses)
    
    Returns:
        ValidationManager: Configured with all validation capabilities
    """
    logger.info("Configuring AI agent trading service validation manager")
    
    # Create generic ValidationManager
    validation_manager = ValidationManager("ai_trading_service")
    
    # Add all validation capabilities
    register_common_validation_methods(validation_manager)  # XML + JSON
    register_agent_governance_validation(validation_manager)  # Agent governance
    
    logger.info("Trading service configured with comprehensive validation capabilities")
    return validation_manager


# Example 4: Configuration-Driven Service Setup
class ServiceValidationConfig:
    """Configuration class for service validation capabilities."""
    
    def __init__(self):
        self.xml_validation = False
        self.json_validation = False
        self.agent_governance = False
        self.service_name = "default_service"
    
    @classmethod
    def for_basic_service(cls, service_name: str) -> 'ServiceValidationConfig':
        """Create config for basic service with XML only."""
        config = cls()
        config.service_name = service_name
        config.xml_validation = True
        return config
    
    @classmethod
    def for_web_service(cls, service_name: str) -> 'ServiceValidationConfig':
        """Create config for web service with XML and JSON."""
        config = cls()
        config.service_name = service_name
        config.xml_validation = True
        config.json_validation = True
        return config
    
    @classmethod
    def for_agent_service(cls, service_name: str) -> 'ServiceValidationConfig':
        """Create config for agent service with all capabilities."""
        config = cls()
        config.service_name = service_name
        config.xml_validation = True
        config.json_validation = True
        config.agent_governance = True
        return config


def configure_service_from_config(config: ServiceValidationConfig) -> ValidationManager:
    """
    Configure ValidationManager based on configuration object.
    
    This demonstrates configuration-driven setup where services specify
    their validation needs declaratively.
    
    Args:
        config: Service validation configuration
        
    Returns:
        ValidationManager: Configured according to specification
    """
    logger.info(f"Configuring service '{config.service_name}' from configuration")
    
    # Create generic ValidationManager
    validation_manager = ValidationManager(config.service_name)
    
    capabilities_added = []
    
    # Add capabilities based on configuration
    if config.xml_validation:
        register_xml_validation(validation_manager)
        capabilities_added.append("XML")
    
    if config.json_validation:
        register_json_validation(validation_manager)
        capabilities_added.append("JSON")
    
    if config.agent_governance:
        register_agent_governance_validation(validation_manager)
        capabilities_added.append("Agent Governance")
    
    logger.info(f"Service configured with capabilities: {', '.join(capabilities_added)}")
    return validation_manager


# Example 5: Runtime Method Registration Example
def demonstrate_runtime_registration():
    """
    Demonstrate how services can add validation methods at runtime.
    
    This shows the dynamic nature of the ValidationManager where methods
    can be added after initial configuration based on runtime conditions.
    """
    logger.info("Demonstrating runtime validation method registration")
    
    # Start with minimal ValidationManager
    validation_manager = ValidationManager("dynamic_service")
    logger.info("Created minimal validation manager")
    
    # Simulate runtime condition - service discovers it needs XML validation
    logger.info("Runtime condition: Service needs XML validation")
    register_xml_validation(validation_manager)
    
    # Verify method is now available
    assert hasattr(validation_manager, 'validate_xml_document')
    logger.info("XML validation method registered successfully")
    
    # Later runtime condition - service needs agent governance
    logger.info("Runtime condition: Service needs agent governance")
    register_agent_governance_validation(validation_manager)
    
    # Verify method is now available
    assert hasattr(validation_manager, 'validate_agent_execution')
    logger.info("Agent governance validation method registered successfully")
    
    return validation_manager


# Usage Examples and Service Patterns
def example_usage_patterns():
    """
    Demonstrate common usage patterns for the dynamic ValidationManager.
    
    This shows how different types of services would typically configure
    and use their ValidationManager instances.
    """
    
    # Pattern 1: Simple document service
    logger.info("=== Pattern 1: Simple Document Service ===")
    doc_service_manager = configure_basic_service()
    
    # This service only has validate_xml_document method available
    available_methods = [
        method for method in dir(doc_service_manager)
        if method.startswith('validate_') and not method.startswith('_')
    ]
    logger.info(f"Document service available methods: {available_methods}")
    
    # Pattern 2: Full-featured web API service
    logger.info("=== Pattern 2: Web API Service ===")
    api_service_manager = configure_web_service()
    
    available_methods = [
        method for method in dir(api_service_manager)
        if method.startswith('validate_') and not method.startswith('_')
    ]
    logger.info(f"API service available methods: {available_methods}")
    
    # Pattern 3: AI agent service with comprehensive validation
    logger.info("=== Pattern 3: AI Agent Service ===")
    agent_service_manager = configure_trading_service()
    
    available_methods = [
        method for method in dir(agent_service_manager)
        if method.startswith('validate_') and not method.startswith('_')
    ]
    logger.info(f"Agent service available methods: {available_methods}")
    
    # Pattern 4: Configuration-driven setup
    logger.info("=== Pattern 4: Configuration-Driven Setup ===")
    
    configs = [
        ServiceValidationConfig.for_basic_service("config_basic_service"),
        ServiceValidationConfig.for_web_service("config_web_service"),
        ServiceValidationConfig.for_agent_service("config_agent_service"),
    ]
    
    for config in configs:
        manager = configure_service_from_config(config)
        available_methods = [
            method for method in dir(manager)
            if method.startswith('validate_') and not method.startswith('_')
        ]
        logger.info(f"Service '{config.service_name}' methods: {available_methods}")


# Service Factory for Common Configurations
class ValidationManagerFactory:
    """
    Factory for creating commonly configured ValidationManager instances.
    
    This provides a convenient way for services to get pre-configured
    ValidationManager instances for common use cases.
    """
    
    @staticmethod
    def create_document_service_manager(service_name: str) -> ValidationManager:
        """Create ValidationManager for document processing services."""
        manager = ValidationManager(service_name)
        register_xml_validation(manager)
        return manager
    
    @staticmethod
    def create_api_service_manager(service_name: str) -> ValidationManager:
        """Create ValidationManager for API services."""
        manager = ValidationManager(service_name)
        register_common_validation_methods(manager)
        return manager
    
    @staticmethod
    def create_agent_service_manager(service_name: str) -> ValidationManager:
        """Create ValidationManager for AI agent services."""
        manager = ValidationManager(service_name)
        register_common_validation_methods(manager)
        register_agent_governance_validation(manager)
        return manager
    
    @staticmethod
    def create_custom_manager(
        service_name: str,
        capabilities: List[str]
    ) -> ValidationManager:
        """
        Create ValidationManager with custom capabilities.
        
        Args:
            service_name: Name of the service
            capabilities: List of capability names ('xml', 'json', 'agent_governance')
            
        Returns:
            ValidationManager: Configured with specified capabilities
        """
        manager = ValidationManager(service_name)
        
        capability_map = {
            'xml': register_xml_validation,
            'json': register_json_validation,
            'agent_governance': register_agent_governance_validation,
        }
        
        for capability in capabilities:
            if capability in capability_map:
                capability_map[capability](manager)
            else:
                logger.warning(f"Unknown capability: {capability}")
        
        return manager


def main():
    """
    Main demonstration of service configuration patterns.
    
    Run this to see how different services would configure their
    ValidationManager instances.
    """
    logging.basicConfig(level=logging.INFO)
    
    logger.info("=== Dynamic ValidationManager Service Configuration Examples ===")
    
    # Show usage patterns
    example_usage_patterns()
    
    # Demonstrate runtime registration
    logger.info("=== Runtime Registration Demo ===")
    demonstrate_runtime_registration()
    
    # Show factory usage
    logger.info("=== Factory Pattern Examples ===")
    factory_examples = [
        ValidationManagerFactory.create_document_service_manager("doc_service"),
        ValidationManagerFactory.create_api_service_manager("api_service"),
        ValidationManagerFactory.create_agent_service_manager("agent_service"),
        ValidationManagerFactory.create_custom_manager("custom_service", ["xml", "agent_governance"]),
    ]
    
    for i, manager in enumerate(factory_examples):
        available_methods = [
            method for method in dir(manager)
            if method.startswith('validate_') and not method.startswith('_')
        ]
        logger.info(f"Factory example {i+1} methods: {available_methods}")


if __name__ == "__main__":
    main()