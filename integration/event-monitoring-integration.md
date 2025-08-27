# Event and Monitoring Integration Guide

## Overview

This guide details how the event system and monitoring infrastructure work together to provide comprehensive observability for the modular Python platform. The integration enables real-time performance tracking, distributed monitoring, and event-driven observability patterns.

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
├─────────────────────────────────────────────────────────────┤
│                  Monitoring Infrastructure                   │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────┐│
│  │Performance       │  │ValidationMonitoring│  │Health     ││
│  │Coordinators      │  │Service            │  │Checkers   ││
│  └────────┬─────────┘  └────────┬──────────┘  └─────┬──────┘│
│           │ publishes           │ subscribes         │       │
├───────────▼─────────────────────▼────────────────────▼──────┤
│                      Event System                            │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────┐ │
│  │Event Producers  │  │Event Bus         │  │Event       │ │
│  │(Typed Events)   │──▶(Redis/InMemory)  │──▶Consumers   │ │
│  └─────────────────┘  └──────────────────┘  └────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Key Integration Points

### 1. EventDrivenPerformanceCoordinator

The coordinator publishes performance metrics as typed events:

```python
class EventDrivenPerformanceCoordinator(IPerformanceCoordinator):
    def __init__(self, event_producer: IEventProducer):
        self._event_producer = event_producer
    
    def start_phase(self, phase: str, field_path: FieldPath) -> None:
        # Publish phase start event
        event = PerformanceEvent(
            event_type="performance.phase.start",
            context_id=self._context_id,
            field_path=field_path,
            operation="monitoring",
            duration_ms=0,
            phase=phase,
            status="started"
        )
        self._event_producer.publish(event)
```

### 2. ValidationMonitoringService

Subscribes to validation events for external monitoring:

```python
class ValidationMonitoringService:
    def __init__(self, event_publisher: IEventPublisher, 
                 coordinator_factory: IPerformanceCoordinatorFactory):
        # Create event-driven coordinator
        self.coordinator = coordinator_factory.create_coordinator(
            MonitoringMode.EVENT_DRIVEN,
            event_publisher=event_publisher
        )
        
        # Subscribe to validation events
        self._setup_event_subscriptions()
    
    def _setup_event_subscriptions(self):
        # Subscribe to all validation events
        self.event_publisher.subscribe(
            "validation.*", 
            self._handle_validation_event
        )
```

### 3. Metrics Collection via Events

Metrics are published as events for aggregation:

```python
def record_metric(self, metric_name: str, value: float):
    event = PerformanceEvent(
        event_type="performance.metric.recorded",
        context_id="system",
        field_path=FieldPath("metrics"),
        operation=metric_name,
        duration_ms=value,  # Reuse duration for metric value
        phase="measurement",
        status="recorded"
    )
    self._event_producer.publish(event)
```

## Event Flow Examples

### Example 1: Validation Performance Tracking

```
1. ValidationContext starts validation
   └─> Publishes "validation.started" event
   
2. ValidationMonitoringService receives event
   └─> Calls coordinator.start_phase("validation")
   
3. EventDrivenPerformanceCoordinator
   └─> Publishes "performance.phase.start" event
   
4. Metrics aggregator consumes performance event
   └─> Updates performance dashboards
```

### Example 2: Health Check Monitoring

```
1. HealthCheckManager performs checks
   └─> Publishes "health.check.completed" events
   
2. Monitoring consumers aggregate health data
   └─> Update system health dashboard
   
3. Alert manager evaluates health status
   └─> Triggers alerts if thresholds exceeded
```

### Example 3: Distributed Request Tracking

```
1. Request enters system with trace_id
   └─> All events include trace_id
   
2. Performance events across services
   └─> Correlated by trace_id
   
3. Distributed trace reconstruction
   └─> Complete request flow visualization
```

## Configuration Patterns

### 1. Development Configuration

```python
# In-memory event system for local development
event_producer = InMemoryEventProducer()
coordinator = EventDrivenPerformanceCoordinator(event_producer)

# Direct monitoring for immediate feedback
monitoring_service = ValidationMonitoringService(
    event_publisher=event_producer,
    coordinator_factory=factory,
    monitoring_mode=MonitoringMode.DIRECT
)
```

### 2. Production Configuration

```python
# Redis-based event system for distribution
redis_config = RedisConfig(host="redis.internal", port=6379)
event_producer = RedisEventProducer(redis_config)

# Event-driven monitoring for scalability
monitoring_service = ValidationMonitoringService(
    event_publisher=event_producer,
    coordinator_factory=factory,
    monitoring_mode=MonitoringMode.EVENT_DRIVEN
)
```

### 3. Testing Configuration

```python
# NoOp for performance testing
event_producer = NoOpEventProducer()
coordinator = NoopPerformanceCoordinator()

# Zero overhead monitoring
monitoring_service = ValidationMonitoringService(
    event_publisher=event_producer,
    coordinator_factory=factory,
    monitoring_mode=MonitoringMode.DISABLED
)
```

## Integration Patterns

### 1. Event Enrichment

Add monitoring context to events:

```python
class MonitoringEventEnricher:
    def enrich_event(self, event: IEvent) -> IEvent:
        # Add monitoring metadata
        if hasattr(event, 'context_id'):
            # Add performance context
            event.performance_context = self.get_current_performance()
        return event
```

### 2. Event Filtering

Filter events for monitoring:

```python
class MonitoringEventFilter:
    def should_monitor(self, event: IEvent) -> bool:
        # Only monitor important events
        if event.event_type.startswith("performance."):
            return True
        if event.event_type in ["validation.failed", "system.error"]:
            return True
        return False
```

### 3. Event Aggregation

Aggregate events into metrics:

```python
class MetricsAggregator:
    def aggregate_performance_events(self, events: List[PerformanceEvent]):
        # Calculate statistics
        durations = [e.duration_ms for e in events]
        return {
            "avg_duration": statistics.mean(durations),
            "p95_duration": numpy.percentile(durations, 95),
            "max_duration": max(durations)
        }
```

## Monitoring Event Types

### Performance Events

```python
# Phase lifecycle
performance.phase.start
performance.phase.end

# Operations
performance.operation.complete
performance.operation.failed

# Metrics
performance.metric.recorded
performance.metric.aggregated

# Resources
performance.resource.allocated
performance.resource.released
```

### Health Events

```python
# Component health
health.component.healthy
health.component.degraded
health.component.failed

# System health
health.system.check
health.system.status

# Thresholds
health.threshold.exceeded
health.threshold.recovered
```

### Monitoring Control Events

```python
# Configuration
monitoring.config.changed
monitoring.mode.switched

# Control
monitoring.enabled
monitoring.disabled
monitoring.sampled
```

## Best Practices

### 1. Event Design for Monitoring

- Include sufficient context for standalone processing
- Use consistent field names across event types
- Include timestamps at event creation
- Add trace_id for correlation

### 2. Performance Considerations

- Use sampling for high-frequency events
- Batch events when possible
- Implement circuit breakers for event publishing
- Monitor the monitoring system itself

### 3. Error Handling

- Never let monitoring break the application
- Gracefully degrade when event system unavailable
- Log monitoring failures separately
- Implement monitoring health checks

### 4. Testing Integration

```python
def test_monitoring_integration():
    # Use in-memory implementations
    producer = InMemoryEventProducer()
    
    # Perform monitored operation
    with Timer() as timer:
        result = perform_operation()
    
    # Verify events published
    events = producer.get_published_events()
    assert any(e.event_type == "performance.operation.complete" 
              for e in events)
```

## Troubleshooting

### Common Issues

1. **Missing Events**
   - Check event pattern subscriptions
   - Verify producer configuration
   - Ensure events are being published

2. **Performance Overhead**
   - Switch to NoOp coordinator
   - Enable sampling
   - Use async event publishing

3. **Event Storm**
   - Implement rate limiting
   - Use event deduplication
   - Configure batch publishing

### Debugging Tools

```python
# Event flow tracer
class EventFlowTracer:
    def trace_event(self, event: IEvent):
        logger.debug(f"Event flow: {event.event_type} at {event.timestamp}")

# Monitoring debugger
class MonitoringDebugger:
    def verify_integration(self):
        # Check all components connected
        assert self.event_producer.is_connected()
        assert self.coordinator.is_monitoring_enabled()
        assert len(self.monitoring_service._subscription_ids) > 0
```

## Migration Strategies

### From Direct to Event-Driven Monitoring

1. **Phase 1**: Add event publishing alongside direct monitoring
2. **Phase 2**: Migrate consumers to event-based metrics
3. **Phase 3**: Remove direct monitoring calls
4. **Phase 4**: Optimize event flow and aggregation

### Adding Monitoring to Existing Services

1. **Minimal Integration**:
   ```python
   # Just add coordinator
   coordinator = factory.create_coordinator(MonitoringMode.EVENT_DRIVEN)
   ```

2. **Full Integration**:
   ```python
   # Complete monitoring setup
   monitoring_service = ValidationMonitoringService(
       event_publisher=get_event_publisher(),
       coordinator_factory=get_coordinator_factory()
   )
   ```

## Future Enhancements

### 1. Complex Event Processing
- Pattern detection across events
- Anomaly detection algorithms
- Predictive monitoring

### 2. Enhanced Correlation
- Automatic service dependency mapping
- Request flow reconstruction
- Performance bottleneck detection

### 3. Advanced Aggregation
- Stream processing for real-time aggregation
- Machine learning for metric prediction
- Automated threshold adjustment

## Conclusion

The integration of events and monitoring creates a powerful observability platform. By publishing monitoring data as typed events, the system gains flexibility, scalability, and the ability to support advanced monitoring patterns. The event-driven approach enables real-time monitoring, historical analysis, and seamless integration with external monitoring systems.