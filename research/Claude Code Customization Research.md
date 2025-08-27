

# **An Expert Report on Engineering Agentic Workflows with Claude Code: Custom Commands, Hooks, and Best Practices**

## **1\. The Agentic Paradigm and the Imperative for Customization**

### **1.1 Defining Agentic Workflows**

Claude Code is not a simple command-line chatbot; it is an agentic coding tool that fundamentally redefines the relationship between a developer and their environment. As a foundational component of modern AI-native development, Claude Code "lives in your terminal, understands your codebase, and helps you code faster" by performing multi-step tasks through natural language commands.1 This is distinct from earlier, more limited tools, as it can operate with deep codebase awareness, execute commands, and make coordinated changes across multiple files without manual context selection.2 It is capable of strategic, multi-step reasoning, where it can be instructed to start with a plan, create a

TODO list, and then proceed to complete tasks sequentially.3 This capability to plan and execute positions it as a true "collaborator," capable of turning "hours-long workflows into a single command".2

This powerful functionality, however, introduces a fundamental tension. The inherent autonomy of an AI agent, its ability to make decisions and execute actions on its own, must be balanced with the human developer's need for control and deterministic outcomes. While the agent's ability to operate autonomously is its core value proposition, it can also lead to unpredictable or undesirable results, such as producing unmaintainable "spaghetti" code or failing to adhere to an existing architectural pattern.4 This paradox—a highly capable tool that can be highly unreliable without proper guidance—underscores a critical need for a robust governance layer. Custom commands and hooks are not merely convenience features; they are the essential components of this governance layer, transforming the raw power of the agent into a predictable, production-ready tool.

### **1.2 The Case for Customization: From Vibe Coding to Engineered Workflows**

Unstructured, ad-hoc use of Claude Code is analogous to "vibe coding," where a developer relies on intuition and a loose conversational style to guide the agent. While this approach can be useful for brainstorming or rapid prototyping, it frequently leads to issues with code quality, maintainability, and architectural consistency.4 The professional application of Claude Code demands a more rigorous, engineered approach. Customization is the pathway to this discipline.

The most effective workflows documented by the community rely on a "detailed template" and a "mandatory process" to prevent the agent from "hallucinating files or messing up \[the\] folder structure".6 This structured approach is a direct response to the tool's tendency to produce code that does not meet a professional quality bar.4 The community-driven solution is to treat prompt engineering and agent interaction with the same rigor as software design, with some developers dedicating 75-80% of their workflow to meticulous planning before any code is generated.5

The ultimate purpose of these customization features is to encode human expertise and architectural guidance directly into the system. A senior developer's deep understanding of a codebase—the specific patterns, conventions, and architectural constraints—can be captured in a reusable format that the AI can understand and follow. This transforms the tool from a simple code generator into a force multiplier for human expertise. When a developer can encode their knowledge into a single command or a series of hooks, they can replicate their most effective workflows consistently across an entire team or project, solving the "Goldilocks problem" of task sizing by making detailed specification a repeatable, automated process.7 This elevates the team's overall productivity and quality floor, allowing a project's success to be rooted in the fact that a developer "knew exactly how to do what it needed to do" and was able to make the AI "just follow my lead".8

## **2\. The Architecture of Customization: Foundations and Hierarchy**

### **2.1 The Project's Brain: CLAUDE.md and Project Memory**

The CLAUDE.md file is the most critical component for maintaining context and ensuring consistent, high-quality output from the agent. It is a living document that serves as the project's persistent memory, storing background knowledge that the agent references at the beginning of every session.3 This externalization of project knowledge is a direct solution to a key limitation of the agent: its tendency to "forget" what it has read when the chat transcript is compacted.4 By treating the filesystem as an extended context window, developers can provide a stable, reliable source of truth that the agent can revisit and learn from repeatedly.

Best practices for the CLAUDE.md file emphasize a structured, deliberate approach.10 The file should be treated as critical project infrastructure, committed to the repository, and included in code review processes.3 The file can contain:

* A concise and structured overview of the project's purpose and architecture.  
* Documented common commands, such as npm run build or npm test.  
* Explicit definitions of coding conventions and style guides, for example, "Use ES modules (import/export), not CommonJS (require)".10  
* Explanations of project workflows, such as Git branching or testing strategies.  
* Pointers to core architectural files and documentation.

In addition to the primary CLAUDE.md file, some developers use a more modular approach, creating specialized memory files like PLANNING.md and TASK.md.11 This allows the agent to maintain a clear separation between the project's strategic roadmap (

PLANNING.md) and the log of completed and pending work (TASK.md). The process of externalizing knowledge to these files transforms Claude Code from a stateless assistant into a powerful collaborator that can remember architectural decisions and project-specific conventions from one session to the next.

### **2.2 Navigating the Settings Hierarchy**

Claude Code's configuration system is a layered architecture that allows for granular control over agent behavior at different scopes. Settings are managed through a hierarchy of JSON files, with more specific settings overriding general ones.3 Understanding this hierarchy is essential for both individual developers and for teams managing a shared project.

The primary configuration files are:

* **\~/.claude/settings.json**: This is the user-specific, machine-wide configuration file. It contains default settings that apply to every project on a developer's machine.12  
* **.claude/settings.json**: This is the project-specific configuration. It is typically version-controlled and shared with the entire team, making it the ideal location for team standards, such as allowed tools or project-specific command aliases.12  
* **.claude/settings.local.json**: This file is for local, project-specific overrides and is typically added to .gitignore. It is the perfect place to store personal preferences or sensitive information like API keys that should not be committed to a repository.12

This multi-layered system is a deliberate design choice that enables a robust, scalable configuration strategy. It allows a developer to maintain personal, global settings while simultaneously adhering to project-specific standards that are version-controlled and shared with the team. The existence of multiple locations, including \~/.claude.json which is often recommended for reliability, can appear confusing at first but is a result of this layered, legacy-compatible design.14 The table below provides a clear overview of this hierarchy and its intended use cases.

| File Path | Scope | Use Case | Version Control Status |
| :---- | :---- | :---- | :---- |
| \~/.claude/settings.json | Machine-wide (User) | Personal defaults, machine-specific configurations. | Not version controlled. |
| .claude/settings.json | Project-specific (Team) | Team standards, project-specific workflows, shared allowedTools. | Version controlled. |
| .claude/settings.local.json | Project-specific (Personal) | Personal overrides, secrets, local test commands. | .gitignore recommended. |

## **3\. Architecting Your Command Library**

### **3.1 Creating Custom Slash Commands**

Custom slash commands are a powerful feature that allows developers to create reusable, shareable prompt templates.10 They are a fundamental tool for encoding institutional knowledge and automating complex, multi-step tasks. These commands are Markdown files stored within a

commands/ directory, and the filename becomes the command name (e.g., refactor.md becomes /project:refactor).10

The content of a custom command file is a meticulously crafted system prompt that provides the agent with specific, detailed instructions. The value of these commands is their ability to go far beyond simple aliases; they are designed to contain "CRITICAL MANDATORY RULES" and guide the agent through a defined process.6 A command like

/prime.md, for instance, doesn't just ask the agent to start; it mandates a systematic approach to understanding the codebase by forcing it to read README.md, git ls-files, and specific project documentation files like PLANNING.md and TASK.md.11

Other examples of powerful custom commands include:

* /commit-and-push.md: A command that automates a semantic git commit and push, and can even intelligently suggest splitting changed files into separate commits for clarity.11  
* /code-review.md: This command can transform the agent into an expert code reviewer, instructing it to analyze the code for security, performance, and best practices, and then to provide a prioritized report with a severity scale.11  
* /fix.md: A generic but effective command that reads a terminal error, uses search tools to find a fix, and then re-runs the command to verify the solution.11

Custom commands are the primary mechanism for capturing a developer's most effective workflows and making them repeatable and accessible to an entire team. They serve as a shared library of best practices, ensuring that everyone can leverage a consistent, high-quality workflow.

### **3.2 The Scope of Commands: Machine-Wide vs. Project-Specific**

The commands/ directory can exist in two primary locations, each with a distinct scope and purpose. This design choice supports a layered workflow, allowing for both personal utilities and team-enforced standards.12

**Machine-wide Commands:**

* **Location:** \~/.claude/commands/  
* **Scope:** These commands are available in **all projects** on a developer's machine.12  
* **Use Case:** Ideal for general development commands that apply universally, such as /xtest for running tests or /xquality for enforcing code quality checks.12 These are personal utility commands that accelerate a developer's individual workflow across all their projects.

**Project-specific Commands:**

* **Location:** .claude/commands/ (in the project's root directory)  
* **Scope:** These commands are only available in the **current project**.12  
* **Use Case:** Best for project-specific workflows, team standards, and domain-specific logic.12 Since they are located within the project directory, they can be version-controlled and shared with the entire team, ensuring that a consistent workflow is available to everyone working on the codebase.

The following table provides a clear comparison of the two command scopes, offering a strategic guide for managing a command library in a professional, team-based environment.

| Location | Scope | Ideal Use Case | Version Control Status |
| :---- | :---- | :---- | :---- |
| \~/.claude/commands/ | All projects | General utilities, personal automation. | Not version controlled. |
| .claude/commands/ | Current project only | Team workflows, project-specific standards. | Version controlled. |

## **4\. Automating with Hooks: Real-time Governance and Control**

### **4.1 Understanding Hook Events and Their Purpose**

Hooks are a powerful, event-driven mechanism that allows external scripts to execute in response to specific Claude Code events. They provide the most advanced layer of control and are essential for real-time governance, security, and the enforcement of dynamic rules that are too complex for static commands.12 The documentation explicitly warns that hooks "execute arbitrary shell commands on your system automatically" and must be used with caution, which underscores their dual role as a powerful tool and a potential security risk.13

Hooks are configured in the same JSON settings files as other configurations (.claude/settings.json, etc.).13 They respond to a variety of events, including:

* **UserPromptSubmit**: This hook runs immediately after a user submits a prompt but before the agent processes it. It can be used to add additional context to the prompt, validate its content, or even block certain types of queries.13  
* **PreToolUse**: This is arguably the most critical hook for security and control. It runs before Claude executes any tool, such as a file edit, a git command, or any other bash command.3 This provides a final opportunity to audit and block potentially dangerous or unwanted actions before they occur, addressing concerns about granting "auto execute" permissions to the agent.9  
* **PostToolUse**: This hook runs after a tool has completed its execution successfully. It can be used to provide feedback to the agent or to trigger a subsequent action based on the outcome of the tool call.3  
* **Stop and SubagentStop**: These hooks are triggered when the main agent or a sub-agent attempts to stop its task. This provides a mechanism to prevent premature task completion, for example, by implementing an "anti-stop" hook that forces the agent to continue until a TODO list is complete.3

The behavior of a hook is determined by its exit code, which allows it to communicate its status back to the agent. An exit code of 0 signals success, an exit code of 2 typically signals a blocking error, and other non-zero codes indicate a non-blocking error.13 This provides a programmatic way for a hook to control the agent's flow, either by stopping an action, providing feedback, or injecting additional context.

### **4.2 Practical Hook Implementations**

Hooks can be used to implement sophisticated, real-time automation and governance layers. The file logger hook, for instance, is a simple but "purely educational" example that logs all Edit, Write, and MultiEdit operations to an external file.12 This provides a transparent audit trail of the agent's actions without blocking them, serving as an excellent starting point for understanding hook mechanics.

For more advanced use cases, hooks can be used to:

* **Implement a pre-commit hook**: A PreToolUse hook could be configured to run a linter or a test suite before allowing a git commit to proceed, ensuring code quality standards are met automatically.13  
* **Create an anti-stop hook**: A developer can build a script for the Stop event that inspects the agent's progress against a TODO list. If the list is not complete, the hook can return an exit code that blocks the stop event, forcing the agent to continue.7 This addresses the issue of the agent prematurely concluding a complex task.

The ability of hooks to provide feedback and block actions is fundamental to building a robust, deterministic system. The following table provides a summary of the complex, nuanced behaviors of different hook events based on their exit code, as documented in the research.

| Hook Event | Exit Code 0 Behavior | Exit Code 2 Behavior | Other Exit Code Behavior |
| :---- | :---- | :---- | :---- |
| PreToolUse | Success; stdout shown to user. | Blocks tool call; stderr shown to Claude. | Non-blocking error; stderr shown to user. |
| PostToolUse | Success; stdout shown to user. | stderr shown to Claude (tool already ran). | Non-blocking error; stderr shown to user. |
| UserPromptSubmit | Success; stdout added to context. | Blocks prompt processing; stderr shown to user. | Non-blocking error; stderr shown to user. |
| Stop | Success; stdout shown to user. | Blocks stoppage; stderr shown to Claude. | Non-blocking error; stderr shown to user. |
| SubagentStop | Success; stdout shown to user. | Blocks stoppage; stderr shown to subagent. | Non-blocking error; stderr shown to user. |

## **5\. Engineering Your Workflow: Advanced Best Practices**

### **5.1 The Strategic Approach: Research, Plan, Implement**

The most successful practitioners of AI-native development have moved beyond the single-prompt approach in favor of a structured, multi-step process.5 This workflow, which positions the human as the strategic architect and the AI as the tactical implementer, is a symbiotic loop that maximizes productivity and minimizes errors. The process typically follows a

Research \-\> Plan \-\> Implement cycle.

1. **Explore/Research**: The first step is to instruct the agent to gather information without writing any code. The agent can read relevant files, run git ls-files to understand the project structure, or examine URLs to gather external context.6 This allows the agent to build a foundational understanding of the codebase before attempting any changes.  
2. **Plan**: Once the agent has sufficient information, it is instructed to create a detailed, step-by-step implementation plan. Using a command like /plan.md or a prompt that includes the word "think" encourages deeper consideration.10 This plan can then be reviewed by the human developer, and in some advanced workflows, a second AI agent is even used to validate the plan for insights or improvements.6  
3. **Implement**: Only after the plan is approved is the agent instructed to begin writing the code. This ensures that the agent works from an agreed-upon blueprint, greatly reducing the risk of "going off the rails".6 The final stage of the implementation involves a  
   Commit command that handles the full git workflow, from writing a descriptive commit message to creating a pull request.10

This multi-step process directly addresses the "Goldilocks problem" of task sizing.7 By breaking down large tasks into smaller, manageable steps, the human developer maintains control over the strategic direction while leveraging the agent's speed for tactical execution. The human is no longer just a prompter but a technical architect, and the process of writing the detailed specification, which can be time-consuming, is made more efficient when the agent itself aids in the planning process.8

### **5.2 TDD with an AI Agent**

Test-Driven Development (TDD) is a particularly powerful application of a structured, engineered workflow. By providing the agent with a "clean, verifiable target," the developer enforces structure and dramatically improves the quality of the generated code.5 The TDD workflow transforms the agent from a chaotic intern into a predictable collaborator.

The process involves these steps:

1. **Write Tests**: The developer's first instruction is to have Claude Code write the tests for the desired functionality. The prompt explicitly states the goal, such as, "We are doing TDD. Write the tests for a function that does X. These tests should fail initially".10  
2. **Confirm Failure**: The agent is then instructed to run the tests and confirm that they fail as expected.  
3. **Commit Tests**: The developer commits the tests to the repository. This is a crucial step that ensures the requirements are captured and that the tests will not be modified by the agent.10  
4. **Write Code**: The final instruction is to write the implementation code with the sole goal of making all the tests pass. The agent will then iterate, writing code, running tests, analyzing failures, and adjusting the code until success is achieved.10

Community feedback confirms that "With context, good rules, and TDD you can achieve spectacular results".5 This approach directly addresses the critique of unmaintainable code by defining a clear success metric before a single line of implementation is written.

### **5.3 Delegating with Sub-Agents**

For larger, more complex projects, the concept of sub-agents introduces a new dimension of scale and organization. A developer can delegate work to a sub-agent, which operates with its own independent context window and can be fine-tuned for specific domains.15

The benefits of this approach are significant:

* **Context Management**: Each sub-agent maintains its own conversation context, which prevents the main session's context window from being overloaded.15 This helps mitigate the issue of the agent "forgetting" its purpose or context during long-running tasks.4  
* **Parallel Development**: Sub-agents enable "true parallel development without conflicts".3 Multiple Claude instances can work on different features simultaneously, with each maintaining its own understanding of its specific task.  
* **Domain Specialization**: Sub-agents can be provided with a "specific system prompt" or fine-tuned for a particular domain, such as front-end development, backend API design, or security auditing.15 This allows the developer to assemble an "AI team" where each member has a specialized role.

## **6\. Overcoming Challenges: Quality, Maintainability, and Control**

### **6.1 The Code Quality Gap**

A pervasive and well-documented challenge with AI-generated code is the gap between functionality and maintainability. A senior developer on a public forum bluntly stated that they had to "rewrite every single line of code that Claude Code produced" because it did not meet their quality bar for clean, elegant, and well-structured code.4 The code often lacks logical abstractions, consistent naming, and a clear separation of concerns, making it "hard to debug and maintain".4

The underlying issue is that the agent's training may prioritize rapid, user-validating output over diligent, architecturally sound solutions.4 While the agent is an excellent "idea generator," it is not a source of production-ready code without serious oversight.5 The mitigation strategies are a direct result of the structured workflows discussed in this report: using TDD to enforce structure, providing a detailed

CLAUDE.md file with a style guide, and maintaining human oversight to review every diff and catch "spaghetti" code before it becomes a problem.4

### **6.2 The Context and Memory Problem**

Another significant challenge is the agent's memory. The agent can "forget nearly everything it read in your codebase but behave confidently like it has" once a conversation is compacted.4 It may also "imagine" that it has run a build or encountered an error when it has not, leading to a hallucinated debugging process.8 This lack of persistent memory is a major obstacle to long-running, multi-session tasks.

The solution to this problem is to treat the agent as if it has no internal memory and to manage context externally. This can be achieved by:

* **Breaking down tasks**: Instead of a single, complex prompt, a developer should break down a large project into "small simple things".8  
* **Re-priming the agent**: The /prime.md command is a crucial tool for re-injecting context at the beginning of every session.11  
* **Utilizing the filesystem**: The most robust solution is to use the filesystem itself as a persistent context store, with CLAUDE.md, PLANNING.md, and other documentation files serving as the external, human-readable memory that the agent can access repeatedly.3

### **6.3 The Human Factor**

Ultimately, Claude Code is a tool, not an oracle. A senior developer offered a perfect analogy, stating that an AI tool is a "chainsaw".5 In the hands of a skilled lumberjack, a chainsaw can do amazing things, but in the hands of someone inexperienced, it can create a mess.5 The power and speed of the agent are directly proportional to the skill and discipline of the developer guiding it. The experienced developer remains the architect of the project, responsible for providing clear direction, maintaining oversight, and ensuring that the final output meets the required standards.

The table below summarizes the most common challenges encountered when using Claude Code and the corresponding mitigation strategies discussed in this report.

| Challenge | Root Cause | Mitigation Strategy |
| :---- | :---- | :---- |
| **Low Code Quality** | Agent lacks architectural guidance and clean code standards. | Use TDD to define success; provide a CLAUDE.md file with a style guide; manually review every diff. |
| **Loss of Context** | Agent's internal memory compacts, leading to "forgetting." | Treat the filesystem as an external memory; use a /prime command to re-inject context; break down tasks into smaller, manageable steps. |
| **Unpredictable Behavior** | Agent operates autonomously without a governance layer. | Use custom commands to encode deterministic, multi-step workflows; use hooks to implement security and governance policies. |
| **Unmaintainable Code** | Agent prioritizes speed over clean abstractions. | Prioritize readability and maintainability; use a structured Research \-\> Plan \-\> Implement workflow. |

## **7\. Conclusion: The Path to AI-Native Development**

### **7.1 Synthesis of Key Takeaways**

The research confirms that to move beyond ad-hoc use and truly harness the power of Claude Code, a developer must adopt an engineered, architecturally-aware approach. This report has demonstrated that custom commands and hooks are not optional features but are, in fact, the necessary governance layer that transforms a powerful but raw agent into a predictable and reliable collaborator. The most effective workflows are structured, human-in-the-loop processes that leverage the agent for its speed while maintaining human control over the strategic and architectural direction. This is achieved through the systematic use of the CLAUDE.md file as a persistent memory, custom commands as containers for institutional knowledge, and hooks as a real-time governance and security layer.

### **7.2 The Future of Agentic Workflows**

The principles of governance, context management, and workflow engineering discussed in this report are not unique to Claude Code. They are universally applicable to the next generation of AI agents and tools. As these tools become more capable and autonomous, the role of the developer will evolve from a direct code writer to an AI-native architect. The ability to design, implement, and manage deterministic workflows will become a core competency for any professional seeking to remain at the forefront of software development. The path to AI-native development lies in understanding that a tool's power is only as great as the system of control with which it is integrated.

#### **Works cited**

1. Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows \- all through natural language commands. \- GitHub, accessed on August 23, 2025, [https://github.com/anthropics/claude-code](https://github.com/anthropics/claude-code)  
2. Claude Code: Deep coding at terminal velocity \\ Anthropic, accessed on August 23, 2025, [https://www.anthropic.com/claude-code](https://www.anthropic.com/claude-code)  
3. Cooking with Claude Code: The Complete Guide \- Sid Bharath, accessed on August 23, 2025, [https://www.siddharthbharath.com/claude-code-the-complete-guide/](https://www.siddharthbharath.com/claude-code-the-complete-guide/)  
4. My hot take: the code produced by Claude Code isn't good enough \- Reddit, accessed on August 23, 2025, [https://www.reddit.com/r/ClaudeAI/comments/1m4t7qk/my\_hot\_take\_the\_code\_produced\_by\_claude\_code\_isnt/](https://www.reddit.com/r/ClaudeAI/comments/1m4t7qk/my_hot_take_the_code_produced_by_claude_code_isnt/)  
5. Claude Code vs. Clean Code: Why AI Struggles with Maintainable ..., accessed on August 23, 2025, [https://medium.com/@limsing/claude-code-vs-clean-code-why-ai-struggles-with-maintainable-software-and-how-to-fix-it-c167199dac1d](https://medium.com/@limsing/claude-code-vs-clean-code-why-ai-struggles-with-maintainable-software-and-how-to-fix-it-c167199dac1d)  
6. My Best Workflow for Working with Claude Code : r/ClaudeAI \- Reddit, accessed on August 23, 2025, [https://www.reddit.com/r/ClaudeAI/comments/1m3pol4/my\_best\_workflow\_for\_working\_with\_claude\_code/](https://www.reddit.com/r/ClaudeAI/comments/1m3pol4/my_best_workflow_for_working_with_claude_code/)  
7. The unbearable slowness of AI coding \- Hacker News, accessed on August 23, 2025, [https://news.ycombinator.com/item?id=44976437](https://news.ycombinator.com/item?id=44976437)  
8. Getting good results from Claude Code | Hacker News, accessed on August 23, 2025, [https://news.ycombinator.com/item?id=44836879](https://news.ycombinator.com/item?id=44836879)  
9. Claude Code Top Tips: Lessons from the First 20 Hours | by Waleed Kadous \- Medium, accessed on August 23, 2025, [https://waleedk.medium.com/claude-code-top-tips-lessons-from-the-first-20-hours-246032b943b4](https://waleedk.medium.com/claude-code-top-tips-lessons-from-the-first-20-hours-246032b943b4)  
10. Claude Code Beginners' Guide: Best Practices \- Apidog, accessed on August 23, 2025, [https://apidog.com/blog/claude-code-beginners-guide-best-practices/](https://apidog.com/blog/claude-code-beginners-guide-best-practices/)  
11. Share Your Claude Code Commands\! : r/ClaudeAI \- Reddit, accessed on August 23, 2025, [https://www.reddit.com/r/ClaudeAI/comments/1l3gouj/share\_your\_claude\_code\_commands/](https://www.reddit.com/r/ClaudeAI/comments/1l3gouj/share_your_claude_code_commands/)  
12. Claude Code: Advanced AI Development Platform Guide, accessed on August 23, 2025, [https://www.paulmduvall.com/claude-code-advanced-tips-using-commands-configuration-and-hooks/](https://www.paulmduvall.com/claude-code-advanced-tips-using-commands-configuration-and-hooks/)  
13. Hooks reference \- Anthropic \- Anthropic API, accessed on August 23, 2025, [https://docs.anthropic.com/en/docs/claude-code/hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)  
14. Claude Code Configuration Guide | ClaudeLog, accessed on August 23, 2025, [https://www.claudelog.com/configuration/](https://www.claudelog.com/configuration/)  
15. This Claude Code Workflow Will 10x Your Coding Output \- YouTube, accessed on August 23, 2025, [https://www.youtube.com/watch?v=W5f4M3te4Mg](https://www.youtube.com/watch?v=W5f4M3te4Mg)