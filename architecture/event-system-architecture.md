# Event System Architecture

## Overview

The modular Python platform implements a fully typed, distributed event system that serves as the backbone for monitoring, observability, and cross-service communication. This document details the architecture, implementation patterns, and integration strategies.

## Core Architecture

### Event System Hierarchy

```
core_interfaces/
├── interfaces/event_handling/
│   ├── events/
│   │   ├── ievent.py              # Base event interface
│   │   ├── iperformance_event.py  # Performance event interface
│   │   └── ivalidation_event.py   # Validation event interface
│   ├── producer/
│   │   ├── ievent_producer.py     # Core producer interface
│   │   └── ievent_publisher_frontend.py  # High-level publisher
│   └── consumer/
│       ├── ievent_consumer.py     # Core consumer interface
│       └── ievent_consumer_frontend.py   # High-level consumer

service_infrastructure/
├── event_handling/
│   ├── events/
│   │   ├── performance_event.py   # Concrete performance event
│   │   ├── validation_event.py    # Concrete validation event
│   │   └── resource_usage.py      # Resource usage data
│   ├── producer/
│   │   ├── noop_event_producer.py      # Zero overhead
│   │   ├── in_memory_event_producer.py # Testing/development
│   │   └── redis_event_producer.py     # Production
│   └── consumer/
│       ├── noop_event_consumer.py      # Zero overhead
│       ├── in_memory_event_consumer.py # Testing/development
│       └── redis_event_consumer.py     # Production
```

## Key Design Principles

### 1. Fully Typed Events (NO Dict[str, Any])

All events are fully typed with no dictionary-based data:

```python
@dataclass
class PerformanceEvent(IPerformanceEvent):
    event_id: UUID
    event_type: str
    timestamp: datetime
    context_id: str
    field_path: FieldPath
    operation: str
    duration_ms: float
    resource_usage: IResourceUsage
    phase: str
    status: str
```

### 2. Protocol-Based Interfaces

Using Python protocols for maximum flexibility:

```python
@runtime_checkable
class IEvent(Protocol):
    event_id: UUID
    event_type: str  # Dotted notation: "performance.metric.recorded"
    timestamp: datetime
    
    @abstractmethod
    def to_json(self) -> str: ...
    
    @classmethod
    @abstractmethod
    def from_json(cls, json_str: str) -> "IEvent": ...
```

### 3. Pluggable Implementations

Three implementation strategies for different scenarios:

- **NoOp**: Zero overhead when events are disabled
- **InMemory**: Local processing and testing
- **Redis**: Distributed production systems

## Event Types and Patterns

### Event Type Naming Convention

Events use dotted notation for hierarchical organization:

```
validation.started
validation.phase.completed
validation.error.occurred
performance.metric.recorded
performance.phase.start
performance.operation.complete
```

### Event Categories

1. **Lifecycle Events**: Track process lifecycles
   - `*.started`, `*.completed`, `*.failed`

2. **Performance Events**: Monitor system performance
   - `performance.metric.*`, `performance.phase.*`

3. **Validation Events**: Track validation processes
   - `validation.*`, `validation.phase.*`

4. **System Events**: Infrastructure and system events
   - `system.health.*`, `system.error.*`

## Producer/Consumer Pattern

### Event Producers

Producers publish typed events:

```python
class IEventProducer(Protocol):
    @abstractmethod
    async def publish(self, event: IEvent) -> None:
        """Publish a typed event."""
```

### Event Consumers

Consumers subscribe to event patterns:

```python
class IEventConsumer(Protocol):
    @abstractmethod
    def subscribe(self, event_pattern: str, handler: EventHandler) -> SubscriptionID:
        """Subscribe to events matching pattern."""
```

### Pattern Matching

Supports wildcard patterns for flexible subscriptions:
- `validation.*` - All validation events
- `*.error.*` - All error events
- `performance.metric.recorded` - Specific event type

## Integration with Monitoring

### Event-Driven Performance Coordinator

The `EventDrivenPerformanceCoordinator` publishes monitoring data as events:

```python
# Phase tracking
self._event_producer.publish(PerformanceEvent(
    event_type="performance.phase.start",
    context_id=context_id,
    field_path=field_path,
    operation="validation",
    duration_ms=0,
    phase=phase,
    status="started"
))
```

### Validation Monitoring Service

Subscribes to validation events for external monitoring:

```python
# Subscribe to validation lifecycle
self.event_publisher.subscribe("validation.*", self._handle_validation_event)
self.event_publisher.subscribe("validation.phase.*", self._handle_phase_event)
```

## Distributed Event Processing

### Redis-Based Distribution

For production systems, Redis provides:
- Pub/Sub for real-time event distribution
- Channel-based topic organization
- Automatic failover and reconnection

### Event Serialization

All events support JSON serialization for network transport:

```python
def to_json(self) -> str:
    return json.dumps(asdict(self), default=str)

@classmethod
def from_json(cls, json_str: str) -> "PerformanceEvent":
    data = json.loads(json_str)
    # Type conversion logic
    return cls(**data)
```

## Future Integration Points

### 1. Distributed Tracing
- Events will carry trace context (trace_id, span_id)
- OpenTelemetry integration through event metadata

### 2. Metrics Aggregation
- Performance events feed into Prometheus/InfluxDB
- Real-time aggregation through stream processing

### 3. Alerting
- Event patterns trigger alert rules
- Complex event processing for anomaly detection

### 4. Audit Trail
- All events persisted for compliance
- Event replay for debugging and analysis

## Best Practices

### 1. Event Design
- Keep events immutable
- Include enough context for standalone processing
- Use semantic versioning for event schemas

### 2. Performance
- Use NoOp producers in performance-critical paths
- Batch events when possible
- Implement backpressure handling

### 3. Error Handling
- Events should never throw exceptions
- Failed event publishing should not break application flow
- Implement retry logic with exponential backoff

### 4. Testing
- Use InMemory implementations for unit tests
- Test event serialization/deserialization
- Verify pattern matching behavior

## Migration Guide

### From Dict-Based Events to Typed Events

Before:
```python
self._event_publisher.publish({
    "event_type": "performance.phase.start",
    "phase": phase,
    "timestamp": time.time(),
})
```

After:
```python
self._event_producer.publish(PerformanceEvent(
    event_type="performance.phase.start",
    context_id=self._context_id,
    field_path=field_path,
    operation="monitoring",
    duration_ms=0,
    phase=phase,
    status="started"
))
```

## Conclusion

The event system provides a robust foundation for distributed monitoring, observability, and cross-service communication. Its typed nature ensures reliability, while the pluggable architecture supports various deployment scenarios from local development to distributed production systems.