# AI Agent Governance System - Implementation Prompt

## 🎯 MISSION

You are implementing a **formal AI agent governance system** with mathematical rigor, comprehensive documentation, and zero tolerance for untyped data structures. This system will govern AI agent behavior through dynamic contracts with Linear Temporal Logic (LTL) verification capabilities.

---

## 📋 MANDATORY PRE-WORK SEQUENCE

**CRITICAL**: Before implementing ANY task, you MUST complete this sequence in order:

### Step 1: Read Project Overview and Context
```
1. Read: docs/plans/ai-agent/human-agent-governance-process-part1.md
   - Process Overview and Analysis
   - Executive summary and formal process templates
   - Current task analysis and verification results

2. Read: docs/plans/ai-agent/human-agent-governance-process-part2.md
   - Implementation Architecture
   - Research-based agent architecture definition
   - Configuration-driven dynamic agent contract system

3. Read: docs/plans/ai-agent/human-agent-governance-process-part3.md
   - Implementation Roadmap
   - Final implementation roadmap with phases and milestones
   - Complete resource planning and success criteria

4. Review: docs/plans/ai-agent/tasks/ (all task files)
   - Understand the overall implementation roadmap
   - See how your assigned task fits in the bigger picture
   - Note dependencies and integration points
```

### Step 2: Study Codebase Rules and Standards
```
3. Read THOROUGHLY: docs/plans/ai-agent/coding-rules.md
   - **ZERO TOLERANCE for violations** - PR rejection for critical rule violations
   - Pay special attention to:
     * Object-oriented design enforcement (NO Dict[str, Any])
     * Validation system rules (ValidationManager patterns)
     * Import rules (NO conditional imports)
     * Error handling patterns (error_handling module integration)
   - These rules are NON-NEGOTIABLE

4. Read: docs/plans/ai-agent/testing-strategy.md
   - Testing Trophy methodology over Test Pyramid
   - AAA pattern requirements
   - Mock usage guidelines
   - Integration testing approaches
```

### Step 3: Understand Current Codebase
```
5. Read: CLAUDE.md (project root)
   - Architecture principles
   - Development workflow
   - Project structure

6. Read: components/common/CLAUDE.md
   - Common components workspace architecture
   - Module dependencies and integration patterns
   - Critical development rules

7. Read: components/common/validation/CLAUDE.md
   - Validation system architecture (CRITICAL for implementation)
   - ValidationManager patterns
   - Info object ownership rules
   - Error handling integration
```

### Step 4: Study Your Assigned Task
```
8. Read your assigned task specification document in docs/plans/ai-agent/tasks/
   - Understand formal requirements (FR-X.Y.Z)
   - Review acceptance criteria
   - Note dependencies and integration requirements
   - Understand deliverables and success metrics
```

### Step 5: Verification Checkpoint
**STOP HERE** - Before proceeding, confirm you understand:
- [ ] The formal verification approach and LTL requirements
- [ ] Object-oriented design enforcement (zero Dict[str, Any] tolerance)
- [ ] ValidationManager-centered architecture patterns
- [ ] Your specific task requirements and acceptance criteria
- [ ] Testing strategy and quality requirements
- [ ] Architecture compliance requirements

---

## ⚠️ CRITICAL IMPLEMENTATION RULES

### Architectural Compliance
- **ALWAYS** follow the dependency hierarchy: Foundation → Core → Infrastructure → Domain
- **ALWAYS** use protocols from core_interfaces
- **ALWAYS** use error_handling module for ALL errors
- **ALWAYS** use ValidationManager as primary validation interface
- **NEVER** create circular dependencies
- **NEVER** bypass established patterns

### Object-Oriented Design Enforcement
```python
# ❌ FORBIDDEN - Will cause PR rejection
metadata = {"key": "value"}
config = {"setting": "value"}  
def process(data: Dict[str, Any]) -> Any:

# ✅ REQUIRED - Fully typed objects
@dataclass(frozen=True)
class ExecutionMetadata:
    timestamp: datetime
    agent_id: str
    execution_duration: float

class AgentConfiguration(BaseModel):
    claude_model: str = Field(...)
    max_tokens: int = Field(4000, ge=1)
    class Config:
        extra = "forbid"
```

### Validation System Integration
- **ALWAYS** create ValidationManager once at service startup
- **ALWAYS** pass validation contexts down through application layers
- **NEVER** create ValidationManager at mid-level services
- **NEVER** use ValidationFactory/ValidationProcess directly
- **ALWAYS** let validation module create ALL Info objects and ErrorRecord

### Error Handling Integration
- **ALWAYS** use error_handling module for ALL errors
- **NEVER** raise raw exceptions (ValueError, etc.)
- **ALWAYS** provide complete error context
- **ALWAYS** integrate with validation system error bridge

---

## 🏗️ IMPLEMENTATION METHODOLOGY

### Phase 1: Analysis and Planning
1. **Task Analysis**: Break down formal requirements into implementation steps
2. **Architecture Design**: Design fully typed objects and protocol interfaces
3. **Integration Planning**: Plan ValidationManager and error_handling integration
4. **Testing Strategy**: Plan comprehensive tests following Testing Trophy methodology

### Phase 2: Present Implementation Plan
**MANDATORY**: Present your complete implementation plan including:
- Fully typed data structures and protocols
- ValidationManager integration approach
- Error handling integration
- Testing approach
- File structure and module organization

**STOP AND ASK** if you have ANY questions about:
- Object-oriented design patterns
- ValidationManager integration
- Error handling requirements
- Testing methodology
- Architecture compliance

### Phase 3: Implementation
Only after plan approval:
1. **Create fully typed objects** (dataclasses, Pydantic models, protocols)
2. **Implement core functionality** following established patterns
3. **Integrate ValidationManager** following lifecycle patterns
4. **Integrate error_handling** for ALL error scenarios
5. **Write comprehensive tests** following Testing Trophy methodology

### Phase 4: Validation and Review
1. **Self-review** against coding rules checklist
2. **Run tests** and ensure ≥95% coverage
3. **Validate architecture compliance**
4. **Document implementation** with examples

---

## 🚨 STOP AND ASK CONDITIONS

**IMMEDIATELY STOP and ASK** if you encounter:

### Technical Issues
- Need to use `Dict[str, Any]` or untyped data structures
- Unclear ValidationManager integration requirements
- Error handling pattern questions
- Architecture dependency questions
- Testing approach uncertainties

### Requirement Clarifications
- Ambiguous formal requirements in task specification
- Missing integration details with existing modules
- Unclear acceptance criteria interpretation
- Performance requirement questions

### Code Quality Questions
- Type annotation challenges
- Protocol design questions
- Mock usage decisions
- Test structure questions

### Architecture Questions
- Module boundary questions
- Interface design decisions
- Dependency injection patterns
- Service lifecycle questions

**Request Template:**
```
IMPLEMENTATION QUESTION:
- **Context**: [Where you are in implementation]
- **Issue**: [Specific question or blocker]
- **Options Considered**: [What approaches you've considered]
- **Architecture Impact**: [How this affects overall design]
- **Request**: [Specific guidance needed]
```

---

## 📊 SUCCESS CRITERIA

### Code Quality Gates
- [ ] All coding rules followed (zero violations)
- [ ] Complete type annotation coverage
- [ ] ValidationManager properly integrated
- [ ] Error handling properly integrated
- [ ] Tests follow Testing Trophy methodology
- [ ] ≥95% test coverage achieved
- [ ] Architecture compliance validated

### Functional Requirements
- [ ] All formal requirements (FR-X.Y.Z) implemented
- [ ] All acceptance criteria met
- [ ] Integration requirements satisfied
- [ ] Performance requirements met
- [ ] Documentation complete with examples

### Review Readiness
- [ ] Self-review completed against all rules
- [ ] Implementation plan executed completely
- [ ] No STOP AND ASK conditions remaining
- [ ] Ready for formal code review

---

## 🔄 WORKFLOW EXECUTION

### 1. Pre-Implementation
```bash
# Confirm you have read and understand:
- Human agent governance process
- All coding rules (especially object-oriented enforcement)
- Testing strategy 
- Validation system architecture
- Your specific task specification
```

### 2. Implementation Planning
```bash
# Create comprehensive implementation plan covering:
- Fully typed data structures
- Protocol interfaces
- ValidationManager integration
- Error handling integration  
- Testing approach
- File organization
```

### 3. Plan Review
```bash
# Present plan for approval
# Address any questions or concerns
# Only proceed after explicit approval
```

### 4. Implementation Execution
```bash
# Follow approved plan exactly
# Maintain architecture compliance
# Integrate with existing systems properly
# Write tests continuously
```

### 5. Validation and Delivery
```bash
# Self-review against all rules
# Run complete test suite
# Validate architecture compliance
# Document implementation
```

---

## 📚 REFERENCE DOCUMENTS

### Essential Reading (MANDATORY)
- `docs/plans/ai-agent/human-agent-governance-process-part1.md` - **Process Overview and Analysis**
- `docs/plans/ai-agent/human-agent-governance-process-part2.md` - **Implementation Architecture**  
- `docs/plans/ai-agent/human-agent-governance-process-part3.md` - **Implementation Roadmap**
- `docs/plans/ai-agent/coding-rules.md` - **CRITICAL: Zero tolerance rules**
- `docs/plans/ai-agent/testing-strategy.md` - **Testing methodology**
- `components/common/validation/CLAUDE.md` - **Validation system architecture**

### Task-Specific Reading
- `docs/plans/ai-agent/tasks/phase{X}-{XX}-{task-name}.md` - **Your assigned task**

### Architecture Reference  
- `CLAUDE.md` - **Project architecture and workflow**
- `components/common/CLAUDE.md` - **Common components patterns**

### Implementation Reference
- Existing modules in `components/common/` - **Established patterns**
- Task specification dependencies - **Integration requirements**

---

## ⚡ START IMPLEMENTATION

**Only after completing ALL pre-work:**

1. **Confirm Understanding**: "I have read and understood all reference documents and am ready to implement [TASK_NAME]"

2. **Present Plan**: Provide comprehensive implementation plan following the methodology above

3. **Implement**: Execute approved plan with strict adherence to all rules and patterns

4. **Deliver**: Complete implementation meeting all success criteria

---

**Remember**: This is a formal system with mathematical rigor. Precision, type safety, and architectural compliance are paramount. When in doubt, STOP AND ASK.