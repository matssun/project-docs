

# **A Blueprint for a High-Assurance AI Agent System**

## **1\. The Foundational Challenge: From "Foolproof" to High-Assurance AI**

The request for a "foolproof" AI agent system requires a re-evaluation of fundamental assumptions about artificial intelligence. The term "foolproof" implies an absolute guarantee of correctness and an infallible system, a state that is not currently achievable with modern large language models (LLMs) and agentic systems. This report does not present a plan for an unattainable "foolproof" system but rather a detailed blueprint for a "high-assurance" or "auditably reliable" system. This strategic re-alignment is a prerequisite for building robust, enterprise-grade AI applications in mission-critical or regulated environments. The foundational challenges that necessitate this shift are rooted in the inherent characteristics of current AI technologies.

### **1.1. The "Foolproof" Fallacy and the Inevitability of Non-Determinism**

The primary obstacle to a "foolproof" system is the intrinsic non-deterministic nature of AI agents, particularly those powered by LLMs.1 Unlike traditional software, which operates on fixed logic, a generative agent can produce different valid responses to the same input, a behavior that complicates validation and auditing.2 This non-determinism stems from a variety of factors, including sampling parameters, decoding strategies, and internal heuristics, which make the reasoning behind an answer opaque and fragile.1 The behavior of a concurrent algorithm can vary on different runs due to a race condition, and probabilistic algorithms, which depend on random number generators, are not guaranteed to produce a correct output every time.3 Applying deterministic verification methods to such non-deterministic systems is a significant challenge, as the unpredictability of the output can render traditional regression tests useless, potentially compromising an entire test suite.4

The pursuit of absolute certainty is further complicated by the continuous "arms race" between AI models and the methods used to detect their outputs.5 As models become more sophisticated, they more accurately mimic human language, making it increasingly difficult to discern between human and machine-generated content. Claims of foolproof detection are often overly optimistic, if not misleading, as any new detection method is quickly overcome by a new generation of models trained to evade it.5 This dynamic landscape means that any guarantee of reliability is, at best, a probabilistic one. While researchers are exploring methods to provide probabilistic safety envelopes, such as in "Guaranteed Safe AI" frameworks, these are fundamentally constrained by the fact that the "world model is not the real world." Proving a system's safety in the physical world is exceedingly complex due to the difficulty of creating a precise model and the impracticality of obtaining complete data for all initial conditions.6 A guarantee of a 1% failure rate for a system with catastrophic potential, such as one producing a bioweapon, is insufficient when adversaries are actively seeking to exploit any vulnerability.7

### **1.2. The New Paradigm: Building for Verifiability and Auditable Trust**

Given the inherent limitations of internal self-correction, the path to a reliable AI agent system lies in an external, verifiable control plane. The core thesis of this blueprint is that reliability is not an inherent property of the LLM agent itself but an architectural property of the entire system. This means that the system must be built with a structured approach to manage risks and ensure transparency and accountability throughout its lifecycle.8 The system's decisions must be transparent and explainable, and every action must be traceable back to a clear source.8

The crucial architectural principle is to separate the roles of generation and verification. An LLM agent, with its non-deterministic nature, is uniquely suited to handle complex, ambiguous, and unstructured problems, serving as a creative engine for generating possible solutions.1 However, the research indicates that LLMs perform poorly at self-verification and that reliance on external, auditable verifiers is critical for improving accuracy and trust.11 The verification system, often a deterministic, rule-based or formal-logic system, acts as a rigorous check on the LLM's probabilistic outputs. This two-part architecture leverages the LLM's strengths in generation while mitigating its weaknesses in self-critique, creating a causal loop of accountability and assurance. By establishing clear ownership and a culture of proactive risk management, an organization can ensure ongoing oversight and a rapid response to issues.8

### **1.3. The Inevitable "Human-in-the-Loop" Imperative**

A high-assurance system must be designed with the explicit understanding that for high-stakes, mission-critical scenarios, the ultimate authority and failsafe is a human operator. The concept of a "foolproof" system often implies full autonomy, but the evidence suggests that the highest level of assurance is achieved when AI agents are designed to augment human expertise rather than replace it entirely.13 Frameworks such as LangGraph support the integration of "human-in-the-loop" workflows, allowing an agent to suspend its operation and request human input when it encounters an uncertain or unexpected scenario.14

This design philosophy treats human intervention not as a failure of the system but as a core feature of its reliability. The blueprint detailed in this report is predicated on a layered defense architecture where the system is built to recognize its own limitations, gracefully degrade, and transfer control to a human when its confidence in a decision is low or when a pre-defined threshold is met.16 Binding every action to an identity—whether an end-user or an agent—provides a unified directory view for security teams and ensures clear accountability and traceability, which is critical for compliance and auditability.17

## **2\. Architectural Blueprint: The Multi-Agent Control Plane**

A single-agent system cannot be foolproof. Instead, this blueprint proposes a multi-layered, defense-in-depth architecture where specialized agents operate under the orchestration of a centralized control plane. This model separates the roles of generation, orchestration, and verification, creating a system of checks and balances at every stage of the development and execution lifecycle.

### **2.1. The Governing Agent: A Centralized Control Layer**

At the heart of the system is the Governing Agent, which is a deterministic, rule-based system. Unlike an LLM-based agent, which can struggle with ambiguity and unpredictability, a rule-based agent operates on a set of predefined, explicit instructions that follow an "if-then" logic structure.10 This provides a transparent and auditable foundation for the entire system's operations. The Governing Agent acts as a central orchestrator and a durable, graph-based state machine that maintains a persistent state across all agent interactions.14 This allows it to remember past decisions, monitor multi-step progress, and track all inputs and outputs for every step of a workflow run.14 Its primary function is to receive an initial query, apply a known set of rules to determine the correct multi-agent workflow, and then dispatch the task to the appropriate specialized agents in a predefined, auditable sequence.

### **2.2. The Specialized Agents: Division of Labor**

The specialized agents are the workhorses of the system, powered by LLMs. They are designed for specific, complex tasks that require contextual understanding, reasoning, and problem-solving capabilities.10 These agents can be equipped with a wide range of external tools to interact with APIs, databases, and other systems in a secure and governed manner.17 Their primary value lies in their ability to handle complexity and unstructured data, from analyzing a natural language query to generating code or a test plan. Frameworks like LangChain and LlamaIndex provide the necessary tools for building these agents, enabling capabilities such as Retrieval-Augmented Generation (RAG) to enhance their knowledge with external data and multi-agent communication for complex collaboration.20

### **2.3. The Verification Agents: The Engine of Reliability**

The most critical component of this architecture is the Verification Agent. These agents are separate from the Specialized Agents and are specifically designed to validate the outputs of the LLM-based agents. They are the guardians of the system's integrity, using formal methods and deterministic checks to provide a layer of assurance that the LLM's outputs are correct, safe, and compliant with all predefined specifications.22 This addresses the fundamental limitation that LLMs are not reliable at self-verification.11 The Verification Agents can be symbolic solvers, code compilers, or specialized tools that check a plan against a formal logic or an output against an executable representation of the LLM's reasoning.1

The following table maps the user's requested lifecycle stages to this multi-agent architecture, providing a clear blueprint for implementation.

**Table 1: AI Agent Lifecycle Control & Verification Matrix**

| Lifecycle Stage | Responsible Agent | Core Function | Verification Mechanism | Key Metrics |
| :---- | :---- | :---- | :---- | :---- |
| Pre-Analysis | Governing Agent & Pre-Analysis Agent | Formalizing the user's ambiguous query and generating a structured plan. | Intent Analysis 24 & Translation of natural language plan into formal logic (e.g., Linear Temporal Logic).25 | Plan coherence, completeness, and logical consistency.26 |
| Post-Analysis | Verification Agent | Validating the generated plan against formal constraints before any action is taken. | Formal methods 22 and code-based verification of the LLM's reasoning.1 | Plan validity, adherence to preconditions, and absence of logical errors. |
| Pre-Coding | Governing Agent & Specialized Agent | Generating the code or sequence of actions necessary to execute the validated plan. | Enforcing preconditions and tool usage rules via agent contracts.27 | Adherence to path conditions and correct tool invocation order. |
| Post-Coding | Verification Agent | Validating the generated code or final output against the system's goals. | Enforcement of postconditions and audit of toolchain execution logs.17 | Correctness, completeness, and compliance with all final requirements. |
| Pre-Testing | Specialized Agent | Generating comprehensive test cases from a formal model of the system. | Model-based testing 22 and continuous integration of formal verification checks.28 | Test coverage, bug detection rate, and consistency of test outcomes. |
| Post-Testing | Verification Agent | Continuously monitoring the system in production to detect performance degradation. | Custom performance metrics 16, drift detection using control charts 16, and recovery metrics. | Task completion rate, response quality, and consistency scores.16 |

## **3\. Phase 1: Pre-Execution Verification and Plan Validation**

The most critical phases in a high-assurance system are those that occur before any execution. This is where the agent's intent and plan are validated, ensuring that it has correctly understood the task and that its proposed course of action is sound, secure, and compliant.

### **3.1. The Pre-Analysis Agent: Formalizing Ambiguity**

The first step in any agentic workflow is for the system to understand the user's intent from an often-ambiguous query.24 The Pre-Analysis Agent, a Specialized Agent under the guidance of the Governing Agent, is tasked with this. It uses a structured prompt to classify the user's query into a predefined set of intents and then generates a multi-step plan in natural language. The plan, however, is not immediately executed. Instead, it is passed to a Verification Agent.

This Verification Agent uses a framework like VerifyLLM to translate the natural language plan into a formal, verifiable representation, such as Linear Temporal Logic (LTL).26 LTL is a formal language that can capture temporal dependencies and logical constraints, providing a rigorous representation of the plan's requirements.29 This process forces the agent's inherently fuzzy reasoning into a structured, auditable format before it can act. The Verification Agent analyzes the LTL formula to systematically identify critical plan inconsistencies, such as position errors, missing prerequisites, and redundant actions.25 The rationale behind this step is that a common failure mode for LLMs is acting on an incorrect interpretation of an ambiguous prompt.2 The solution is not to simply improve the prompt but to introduce a formal, verifiable step that validates the agent's

*understanding* of the problem. This is a second-order validation, ensuring the LLM's internal representation of the task aligns with all safety and business requirements before it proceeds to execute any actions.

### **3.2. The Pre-Coding Agent: Verifying Reasoning via Executable Code**

Once the plan has been validated, the system moves to the pre-coding phase. In this stage, the LLM is not asked to generate the final, deployable code. Instead, it is tasked with expressing its multi-step reasoning in an executable format, such as a Python function with assertions.1 This approach, referred to as "code-as-reasoning," transforms the LLM's fragile natural language Chain-of-Thought into a robust, machine-verifiable proof.1

The generated code, which serves as a "machine-verifiable proxy" for the LLM's logic, is then passed to a Verification Agent. This agent executes the code and runs a series of unit tests to check if the logic is sound.1 If the code fails, the LLM's reasoning is demonstrably flawed, and the process is halted. This approach is particularly valuable for complex, multi-step tasks where the correctness of the reasoning is paramount.1 The power of this methodology lies in its ability to leverage the LLM's emergent reasoning capabilities to generate a deterministic artifact—the code—that can be verified by a separate, deterministic process, such as a compiler or a unit test. This multi-layered approach leverages the strengths of both paradigms while mitigating their weaknesses, providing a foundational layer of verifiability before any final code is deployed.

## **4\. Phase 2: Post-Execution Validation and State Auditing**

Post-execution validation is crucial for ensuring that the agent's actions achieved the desired outcome and maintained system integrity. This phase provides the final, auditable proof of correctness.

### **4.1. The Post-Coding Agent: Enforcing Correctness with Agent Contracts**

The Post-Coding Agent, a dedicated Verification Agent, is responsible for evaluating the final output of the Specialized Agent (e.g., the generated code or a data analysis report) against a formal "Agent Contract".27 These contracts, which are defined by the rule-based Governing Agent, establish clear requirements for the entire process. An Agent Contract is composed of three critical components:

* **Preconditions:** These must be satisfied before the agent begins its task, such as a user providing a valid order ID in a refund request.27  
* **Pathconditions:** These define the required sequence of actions and decisions that must occur during the agent's execution. This is a crucial element for auditability, as it ensures that the agent used only approved tools, followed the correct logical flow, and managed the system's state evolution as specified.27  
* **Postconditions:** These specify the required state of the system after the execution is complete, guaranteeing properties of the output such as correctness, completeness, and adherence to security or regulatory requirements.27

The concept of path conditions is a key element of a high-assurance system. An agent could potentially arrive at a correct final output through an incorrect or insecure path, such as using an unapproved tool or mismanaging state.27 The Agent Contract provides the logical framework to link the pre-execution plan to the post-execution outcome, ensuring that not only the result but also the process used to achieve it is correct and auditable. This provides an authoritative mechanism for demonstrating compliance with a wide range of operational and regulatory requirements.

### **4.2. The Post-Testing Agent: Continuous Monitoring and Drift Detection**

A single, final test is insufficient for a high-assurance system. Unlike traditional software with fixed logic, an AI agent's performance can deteriorate over time as real-world conditions evolve beyond its training data.2 This phenomenon, known as "performance drift," can quietly degrade an agent's reliability and lead to inaccurate outputs, which can have real costs in business applications.2 The Post-Testing Agent is a continuous monitoring service designed to mitigate this risk.

This agent tracks a suite of specialized metrics that go beyond simple accuracy, including:

* **Task Completion Rate:** The percentage of tasks an agent successfully completes without human intervention.16  
* **Consistency Scores:** Measures the variance in responses to similar inputs.16  
* **Edge Case Performance:** Evaluates the agent's effectiveness when faced with unusual inputs.16  
* **Recovery Metrics:** Quantifies the agent's ability to recognize and correct its own mistakes, such as by requesting clarification when uncertain.16

By establishing baseline performance ranges using tools like control charts, the Post-Testing Agent can alert human operators when a metric drifts beyond an acceptable threshold.16 This is a continuous process of verification and adaptation, transforming reliability from a static state into a dynamic, managed property. This agent serves as the final, continuous safety net, providing a mechanism for early detection of degradation before it impacts operations.

## **5\. The Operational Backbone: Enterprise Frameworks and Governance**

The architectural blueprint detailed in this report requires a robust operational backbone to manage the complexity of a multi-agent system. This involves selecting the right orchestration framework and implementing enterprise-grade governance for all agent interactions.

### **5.1. Selecting the Right Orchestration Framework**

The complexity of a multi-agent system, with its need for stateful orchestration, human-in-the-loop workflows, and tool integration, necessitates a robust framework. Several leading open-source options are available, each with distinct strengths:

* **LangGraph:** A powerful framework that uses computational graphs to model multi-agent workflows.14 It stands out by maintaining a persistent state across interactions, allowing agents to remember past decisions and coordinate seamlessly.14 Its ability to pause operations for human input makes it ideal for the human-in-the-loop imperative.14  
* **LangChain:** A widely adopted orchestration framework that provides a generic interface for interacting with LLMs and integrating with external data sources and software workflows.20 LangChain supports multi-agent communication and provides centralized coordination capabilities.20  
* **LlamaIndex:** Excels in "agentic document workflows," providing a framework for agents to extract, analyze, and act on complex enterprise documents.13 It is particularly suited for tasks that require maintaining context and state across multiple steps, such as contract review or claims processing.13  
* **Mastra:** A TypeScript-based framework that offers a clear control flow with graph-based state machines. Its features, such as suspend()/resume(), are designed for durable human-in-the-loop workflows, providing a visual development approach that can simplify prototyping.15

Each of these frameworks offers modularity, enabling organizations to customize components like memory and execution, and provides the necessary tools for complex orchestration and API integration.32 The selection depends on the specific domain and workflow requirements. The following table provides a high-level comparison to guide the decision process.

**Table 2: Comparison of Enterprise Agent Orchestration Frameworks**

| Framework | Key Feature | Language | Suitability |
| :---- | :---- | :---- | :---- |
| **LangGraph** | Stateful Orchestration, Graph-based Flow, Human-in-the-loop | Python | Best for complex, multi-step workflows that require memory and state persistence. |
| **LangChain** | Data Connection (RAG), Multi-agent Communication, Flexible Chaining | Python, JavaScript | Best for general-purpose LLM applications and retrieval-augmented generation (RAG) tasks. |
| **LlamaIndex** | Document Processing, Agentic Workflows, Enterprise-grade Parsing | Python | Best for document-heavy workflows and knowledge-intensive tasks. |
| **Mastra** | Durable Graph-based State Machines, Human-in-the-loop, Built-in Tracing | TypeScript | Best for building robust, auditable workflows that require clear control flow and developer-friendly tools. |

### **5.2. Implementing Enterprise-Grade Tool Governance**

Agents are only as trustworthy as the governance behind the tools they use.17 A high-assurance system requires a layered enterprise toolchain that ensures every interaction with an external system is secure and auditable. This governance model must be centralized, as managing permissions and policies on a per-agent basis is an old and risky model.17 The Azure AI Foundry model provides an excellent example of a robust approach to tool governance.17

Key principles of enterprise tool governance include:

* **Centralized API Management:** A powerful control plane, such as Azure API Management (APIM), provides a centralized mechanism for publishing tools and enforcing consistent policies, including authentication, rate limits, and payload validation.17 This keeps policy logic out of the tool code itself, simplifying changes and ensuring consistency.17  
* **Identity Binding:** Every tool invocation must be bound to an identity, whether a user or an agent, for a clear audit trail.17 This provides security teams with a unified view of all agents and their actions, which is essential for auditability and risk management.17  
* **Tool as an API Product:** Tools should be treated as formal API products with clear contracts, inputs, outputs, and error behaviors.17 This approach ensures that tools are self-describing, making them easier for agents to discover and integrate with at runtime without manual wiring.17 Smaller, single-purpose tools are easier to test and monitor for reliability.17

By implementing this governance framework, an organization can ensure that all agents operate within a secure and observable environment, balancing the speed of development with the critical need for security and control.17

## **6\. Conclusion and Strategic Recommendations**

The goal of a "foolproof" AI system is an aspirational concept that, in its literal sense, is not achievable with today's technology. The inherent non-determinism, the potential for hallucination, and the dynamic nature of AI models render a truly infallible system impossible. The strategic pivot from seeking absolute certainty to architecting for "high-assurance" and "auditable reliability" is not a compromise but a necessary and pragmatic step.

The blueprint presented in this report achieves this by shifting the focus from the internal capabilities of a single agent to the architectural integrity of a multi-agent system. Reliability is not a property of the generative model itself but is engineered through a series of external controls and continuous verification loops. The Governing Agent, with its deterministic rule-based logic, orchestrates the workflow, while the Verification Agents serve as a crucial second-order check on the probabilistic outputs of the Specialized Agents. The system is designed to formalize ambiguity, verify reasoning via executable code, and enforce correctness through Agent Contracts and continuous monitoring.

The ultimate guarantor of system safety and correctness in high-stakes domains is the human operator. The system is designed to augment human expertise, not to replace it, providing the human-in-the-loop with the tools to pause, verify, and assume control when needed.

Based on this analysis, the following strategic recommendations are provided for a team seeking to implement this blueprint:

1. **Phase I: Strategic Re-alignment.** The first step is to adopt the "high-assurance" mindset across the organization. This requires a fundamental shift away from expecting infallible performance from a single AI agent and towards a layered, defense-in-depth security model. This is a policy decision that must be made before any technical implementation begins.  
2. **Phase II: Pilot Implementation.** Begin with a small-scale, end-to-end pilot project on a well-defined, low-risk use case. This pilot should implement the core components of the multi-agent control plane, including a rule-based Governing Agent, a Specialized Agent, and at least one Verification Agent for pre-execution plan validation. Focus on proving the concept of verifiability before scaling.  
3. **Phase III: Governance and Policy.** Before transitioning from a pilot to an enterprise-scale system, a formal governance framework must be established. This includes developing clear policies for tool usage, identity management, and audit trails. Centralize API management and ensure every agent's action is auditable. This proactive approach ensures that as the system grows in complexity and capability, its security and reliability are maintained.

#### **Citerade verk**

1. Formalizing LLM Reasoning via Code-Based Verification | by ..., hämtad augusti 26, 2025, [https://sumeetmore.medium.com/formalizing-llm-reasoning-via-code-based-verification-6671478b4de0](https://sumeetmore.medium.com/formalizing-llm-reasoning-via-code-based-verification-6671478b4de0)  
2. AI Agents: Reliability Challenges & Proven Solutions \[2025\] \- Edstellar, hämtad augusti 26, 2025, [https://www.edstellar.com/blog/ai-agent-reliability-challenges](https://www.edstellar.com/blog/ai-agent-reliability-challenges)  
3. Nondeterministic algorithm \- Wikipedia, hämtad augusti 26, 2025, [https://en.wikipedia.org/wiki/Nondeterministic\_algorithm](https://en.wikipedia.org/wiki/Nondeterministic_algorithm)  
4. Eradicating Non-Determinism in Tests \- Martin Fowler, hämtad augusti 26, 2025, [https://martinfowler.com/articles/nonDeterminism.html](https://martinfowler.com/articles/nonDeterminism.html)  
5. The Fallacy of Foolproof AI-Generated Content Detection | by Dean Lofts \- Medium, hämtad augusti 26, 2025, [https://loftwah.medium.com/the-fallacy-of-foolproof-ai-generated-content-detection-5538c08244ca](https://loftwah.medium.com/the-fallacy-of-foolproof-ai-generated-content-detection-5538c08244ca)  
6. In response to critiques of Guaranteed Safe AI \- AI Alignment Forum, hämtad augusti 26, 2025, [https://www.alignmentforum.org/posts/DZuBHHKao6jsDDreH/in-response-to-critiques-of-guaranteed-safe-ai](https://www.alignmentforum.org/posts/DZuBHHKao6jsDDreH/in-response-to-critiques-of-guaranteed-safe-ai)  
7. Limitations on Formal Verification for AI Safety — LessWrong, hämtad augusti 26, 2025, [https://www.lesswrong.com/posts/B2bg677TaS4cmDPzL/limitations-on-formal-verification-for-ai-safety](https://www.lesswrong.com/posts/B2bg677TaS4cmDPzL/limitations-on-formal-verification-for-ai-safety)  
8. AI Governance Framework: Key Principles & Best Practices \- MineOS, hämtad augusti 26, 2025, [https://www.mineos.ai/articles/ai-governance-framework](https://www.mineos.ai/articles/ai-governance-framework)  
9. Rule-based AI: the backbone of automation \- Telnyx, hämtad augusti 26, 2025, [https://telnyx.com/learn-ai/rule-based-ai](https://telnyx.com/learn-ai/rule-based-ai)  
10. Rule-Based vs. LLM-Based AI Agents: A Side-by-Side Comparison \- TeckNexus, hämtad augusti 26, 2025, [https://tecknexus.com/rule-based-vs-llm-based-ai-agents-a-side-by-side-comparison/](https://tecknexus.com/rule-based-vs-llm-based-ai-agents-a-side-by-side-comparison/)  
11. The Achilles' heel of AI Agents: Reliability \- by Jian Zhang \- Medium, hämtad augusti 26, 2025, [https://medium.com/@jianzhang\_23841/reliability-of-ai-agents-f43a5dbf7642](https://medium.com/@jianzhang_23841/reliability-of-ai-agents-f43a5dbf7642)  
12. On the self-verification limitations of large language models on reasoning and planning tasks | OpenReview, hämtad augusti 26, 2025, [https://openreview.net/forum?id=4O0v4s3IzY](https://openreview.net/forum?id=4O0v4s3IzY)  
13. Introducing Agentic Document Workflows — LlamaIndex \- Build Knowledge Assistants over your Enterprise Data, hämtad augusti 26, 2025, [https://www.llamaindex.ai/blog/introducing-agentic-document-workflows](https://www.llamaindex.ai/blog/introducing-agentic-document-workflows)  
14. 11 Open Source AI Agent Frameworks That Will Transform Your Development (2025 Complete Guide) \- Latenode, hämtad augusti 26, 2025, [https://latenode.com/blog/11-open-source-ai-agent-frameworks-that-will-transform-your-development-2025-complete-guide](https://latenode.com/blog/11-open-source-ai-agent-frameworks-that-will-transform-your-development-2025-complete-guide)  
15. Mastra: The Typescript AI framework, hämtad augusti 26, 2025, [https://mastra.ai/](https://mastra.ai/)  
16. Effective governance frameworks for AI agents \- IBM Developer, hämtad augusti 26, 2025, [https://developer.ibm.com/articles/governing-ai-agents-watsonx-governance/](https://developer.ibm.com/articles/governing-ai-agents-watsonx-governance/)  
17. Agent Factory: Building your first AI agent with the tools to deliver ..., hämtad augusti 26, 2025, [https://azure.microsoft.com/en-us/blog/agent-factory-building-your-first-ai-agent-with-the-tools-to-deliver-real-world-outcomes/](https://azure.microsoft.com/en-us/blog/agent-factory-building-your-first-ai-agent-with-the-tools-to-deliver-real-world-outcomes/)  
18. What are AI agents? Definition, examples, and types | Google Cloud, hämtad augusti 26, 2025, [https://cloud.google.com/discover/what-are-ai-agents](https://cloud.google.com/discover/what-are-ai-agents)  
19. A practical guide to building agents \- OpenAI, hämtad augusti 26, 2025, [https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)  
20. What Is LangChain? Examples and definition \- Google Cloud, hämtad augusti 26, 2025, [https://cloud.google.com/use-cases/langchain](https://cloud.google.com/use-cases/langchain)  
21. LlamaIndex \- Build Knowledge Assistants over your Enterprise Data, hämtad augusti 26, 2025, [https://www.llamaindex.ai/](https://www.llamaindex.ai/)  
22. Formal Methods for Artificial Intelligence: Opportunities and Challenges \- Encyclopedia.pub, hämtad augusti 26, 2025, [https://encyclopedia.pub/entry/44342](https://encyclopedia.pub/entry/44342)  
23. Formal Methods & Automated Reasoning | Computer Science and Engineering at Michigan, hämtad augusti 26, 2025, [https://cse.engin.umich.edu/research/areas-of-research/formal-methods-automated-reasoning/](https://cse.engin.umich.edu/research/areas-of-research/formal-methods-automated-reasoning/)  
24. A Beginner's Guide to LLM Intent Classification for Chatbots \- Vellum AI, hämtad augusti 26, 2025, [https://www.vellum.ai/blog/how-to-build-intent-detection-for-your-chatbot](https://www.vellum.ai/blog/how-to-build-intent-detection-for-your-chatbot)  
25. VerifyLLM: LLM-Based Pre-Execution Task Plan Verification for Robots, hämtad augusti 26, 2025, [https://verifyllm.github.io/](https://verifyllm.github.io/)  
26. VerifyLLM: LLM-Based Pre-Execution Task Plan Verification for Robots \- arXiv, hämtad augusti 26, 2025, [https://arxiv.org/html/2507.05118v1](https://arxiv.org/html/2507.05118v1)  
27. Ensuring Trust in AI with Agent Contracts \- Relari, hämtad augusti 26, 2025, [https://www.relari.ai/docs/agent-contracts-whitepaper.pdf](https://www.relari.ai/docs/agent-contracts-whitepaper.pdf)  
28. How to integrate formal proofs into software development \- Amazon Science, hämtad augusti 26, 2025, [https://www.amazon.science/blog/how-to-integrate-formal-proofs-into-software-development](https://www.amazon.science/blog/how-to-integrate-formal-proofs-into-software-development)  
29. JohnSili/VerifyLLM \- GitHub, hämtad augusti 26, 2025, [https://github.com/JohnSili/VerifyLLM](https://github.com/JohnSili/VerifyLLM)  
30. VerifyLLM: LLM-Based Pre-Execution Task Plan Verification for Robots \- arXiv, hämtad augusti 26, 2025, [https://arxiv.org/pdf/2507.05118](https://arxiv.org/pdf/2507.05118)  
31. What Is LangChain? | IBM, hämtad augusti 26, 2025, [https://www.ibm.com/think/topics/langchain](https://www.ibm.com/think/topics/langchain)  
32. What Are Agentic AI Frameworks? (With Examples) \- Multimodal, hämtad augusti 26, 2025, [https://www.multimodal.dev/post/agentic-ai-frameworks](https://www.multimodal.dev/post/agentic-ai-frameworks)  
33. A New Concept for Authentication and Authorisation for AI Agents | by Michael Poulin, hämtad augusti 26, 2025, [https://medium.com/@m3poulin/a-new-concept-for-authentication-and-authorisation-for-ai-agents-c9014dcab076](https://medium.com/@m3poulin/a-new-concept-for-authentication-and-authorisation-for-ai-agents-c9014dcab076)