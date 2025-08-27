

# **A Strategic Framework for Modern, Professional Python Test Conventions**

## **Executive Summary**

This report presents a new, professional standard for software testing within the existing Python codebase. The current testing practices, characterized by an excessive reliance on mocks, have led to brittle, high-maintenance tests that fail to provide a true sense of security. This new standard addresses this problem by grounding test conventions in a modern, risk-management philosophy that aligns with object-oriented principles.

The core recommendations are:

1. **Shift to a Risk-Based Philosophy:** Testing is not a simple task of finding bugs, but a strategic discipline for identifying and mitigating business risks. The scope and type of tests should be determined by the criticality of the functionality being validated.1  
2. **Embrace the Testing Trophy:** Transition from the rigid Test Pyramid to the more flexible Testing Trophy heuristic. This prioritizes a robust layer of integration tests to validate object interactions, complemented by a solid base of static analysis and fast unit tests.2  
3. **Adopt the Right Tools:** Mandate the use of pytest and pytest-mock for all new test development. These tools offer a more concise syntax, powerful fixtures, and simplified mocking, which will significantly reduce boilerplate and improve maintainability.4  
4. **Implement Code Conventions:** Enforce strict conventions at the code level, including the Arrange-Act-Assert (AAA) pattern and descriptive, human-readable naming conventions (e.g., GIVEN-WHEN-THEN).6  
5. **Differentiate Test Doubles:** Educate the team on the precise taxonomy of test doubles, distinguishing between stubs (for state verification) and mocks (for behavior verification) to avoid misapplication and test fragility.8

By implementing these conventions, the team will build a test suite that is faster, more reliable, and easier to maintain. This strategic shift will produce higher-quality software and restore confidence in the test suite as a robust safety net for the application.

---

## **Part 1: Foundational Principles of Modern Software Testing**

### **The Paradigm Shift: From Procedural to Object-Oriented Testing**

Traditional software testing methodologies were designed for procedural or functional programming paradigms, where the primary focus was on verifying how functions or procedures manipulated data. However, with the widespread adoption of object-oriented programming (OOP), this approach is no longer sufficient. An object-oriented system is not a collection of independent functions; it is a complex web of interacting objects and classes.10

Modern testing, therefore, must shift its focus to Object-Oriented Testing (OOT), a process designed specifically for applications built with OOP principles like encapsulation, inheritance, and polymorphism. The purpose of OOT is to validate how individual objects behave in isolation and, most importantly, how they interact with one another.10 The control flow in an object-oriented program is characterized by "message passing among objects" 10, and testing must ensure that this communication results in the desired outcomes. The goal is to not only find technical errors but also to identify and address design flaws, ensuring that the system's architecture and object interactions comply with the intended design.10

### **Testing as a Risk Management Discipline**

A professional testing practice is not merely about finding bugs. It is a fundamental component of a comprehensive risk management strategy for software development.1 The purpose of testing is to identify, mitigate, and manage the risks associated with an application's design and code. The goal is to actively make the software fail in a controlled environment to uncover potential defects before they cause problems in production.12

A critical philosophical principle to internalize is the "Absence of Errors Fallacy".12 This principle states that while testing can show the presence of defects, it can never prove their complete absence. Even after multiple tests, an application can never be considered 100% bug-free. Moreover, a product can be 99% bug-free but still be unusable if it fails to meet core user requirements.12 The most valuable tests are those that are designed to validate that the software meets its specified requirements and mitigates the most critical risks to the product, the customer, and the business.1 Test scope should, therefore, be determined not by exhaustive coverage—which is impossible—but by an understanding of these identified risks.1 This risk-based approach ensures that testing efforts are focused on what matters most, maximizing return on investment.

### **The Strategic Hierarchy of Testing: Beyond the Pyramid**

The traditional approach to structuring a test suite is often visualized as the Testing Pyramid. This heuristic, a foundational framework in software testing, emphasizes a large base of fast and reliable unit tests, a middle layer of slower integration tests, and a small, minimal top layer of end-to-end (E2E) tests. The primary focus of the Testing Pyramid is to balance test speed and maintenance cost.2

While the Test Pyramid remains a useful model, a more modern and context-aware heuristic has emerged: the Testing Trophy. The Testing Trophy, an evolution of the Pyramid, shifts the focus from speed and cost to the value and Return on Investment (ROI) of different types of tests. It places a greater emphasis on the integration layer, considering it the most valuable for a modern, object-oriented system because it validates the seamless interaction between components. The Trophy also de-emphasizes E2E tests, which are slow and brittle, and includes static code analysis as a foundational layer to catch potential issues before any tests are run.2

The Testing Trophy is not a rigid prescription but a flexible framework that guides smart, context-driven decisions about how to test software.2 For an object-oriented codebase, this model is particularly effective. Unit tests form a stable base by validating individual components in isolation. Integration tests, now the centerpiece, ensure that these components work together as intended, focusing on message passing and data flow between objects.10 Finally, E2E tests are used sparingly to cover only the most critical, user-centric workflows.3 The strategic order of testing in a professional development lifecycle is to move from the smallest, most isolated tests to the largest, most integrated ones: Unit testing first, followed by Integration, and then Functional/E2E testing.13

A comparison of these two models provides a clear rationale for the recommended approach:

| Feature | Test Pyramid | Testing Trophy |
| :---- | :---- | :---- |
| **Primary Goal** | Balance of speed and cost 2 | Focus on value and ROI 2 |
| **Primary Layers** | Unit \> Integration \> E2E 3 | Integration \> Unit \> Static \> E2E 3 |
| **Focus Area** | Unit tests as the foundation | Integration tests as the centerpiece |
| **Rationale** | Fast tests are cheap to maintain | High-value tests provide more confidence |
| **Applicability** | General software development | Modern, service-oriented systems 3 |
| **Key Consideration** | Quantity of tests at each layer | Quality and ROI of tests at each layer |

---

## **Part 2: Deconstructing the "Over-Mocking" Problem**

### **The "Mock-Reality Gap": Why Over-Mocking is a Problem**

The overuse of mocks is a symptom of a deeper problem and a significant liability to a codebase. Mocks are designed to simulate the behavior of complex or external dependencies to allow for isolated unit testing.15 However, when used excessively, they create a false sense of security and lead to tests that are brittle, fragile, and ultimately unhelpful.16

A primary pitfall of over-mocking is the "mock-reality gap".16 Mock objects are typically limited to simple, predefined return values and cannot realistically replicate the complex, dynamic, or unpredictable nature of real-world dependencies. The actual behavior of a dependency might involve complex state changes, side effects, race conditions, or intermittent failures that are impossible to simulate with a mock. Consequently, a test that relies on a simplified mock may pass, even though the real implementation would fail in a production environment.16

Furthermore, over-mocking leads to tests that are tightly coupled to the implementation details of the system under test, rather than its observable behavior.18 If a developer refactors the production code, for example, by renaming a private method or changing the order of internal calls, a mock-based test will likely fail, even if the final, observable behavior of the application remains correct.15 This creates "brittle" tests that require constant maintenance and discourage developers from making healthy changes to the codebase.19 This dynamic diminishes the value of the test suite from a safety net to a maintenance burden.15

The prevalence of over-mocking in a codebase often signals a deeper architectural issue. When a test is difficult to write without mocking a large number of dependencies, it is often a sign that the class being tested has too many responsibilities.20 A class with a long list of dependencies in its constructor, or one that interacts with too many different services, violates the Single Responsibility Principle and has low cohesion. In this scenario, the testing challenge is not a problem with the testing culture itself, but a symptom of a poorly designed system. The proper solution is to refactor the production code to be more modular and cohesive, allowing for smaller, more focused tests that require fewer, if any, mocks.20

### **A Precise Taxonomy of Test Doubles**

To address the conceptual confusion at the root of the over-mocking problem, it is essential to establish a precise and shared vocabulary. The overarching term for any object that replaces a production object for testing purposes is a **Test Double**.9 This term encompasses several distinct types, each with a specific purpose.

* **Dummy Objects:** These are objects that are passed around, typically to fill a parameter list, but are never actually used in the test.9  
* **Fake Objects:** These objects have a working implementation but take shortcuts that make them unsuitable for production use. An InMemoryDatabase is a classic example of a fake object.9  
* **Stubs:** These test doubles provide pre-canned, static answers to calls made during a test. Their purpose is to control the state of the system under test by providing predictable return values. Stubs do not perform any verification of interactions.9  
* **Spies:** A spy is a type of stub that also records information about how it was called, such as the number of calls or the arguments passed to a method. Spies are used for behavior verification, much like a mock.9  
* **Mocks:** These are the most powerful and opinionated test doubles. A mock is pre-programmed with explicit *expectations* about the calls it is expected to receive. If these expectations are not met, the test will fail. Mocks are specifically designed for **behavior verification**—verifying that the system under test made the correct calls on its collaborators.9

The fundamental issue with over-mocking is the conflation of stubs and mocks.8 Many popular mocking frameworks make it exceptionally easy to create a mock object that can act as a stub. This ease of use can be seen as a "gateway drug".18 Developers, needing only to provide a canned return value (a stub's purpose), will use a full-featured mocking framework to do so. This can then lead them to use the framework's behavior verification features, which tightly couples the test to the internal implementation details of the production code. This is a primary reason why tests become brittle and a maintenance burden. The appropriate approach is to use a simple stub or fake for tests that focus on state verification, and to reserve the use of mocks for the specific and limited cases where the interaction itself is the behavior being tested.

The following table provides a clear reference for the distinct types of test doubles and their appropriate use cases:

| Test Double | Purpose | Verification Style | When to Use |
| :---- | :---- | :---- | :---- |
| **Dummy** | Fill parameter lists 9 | N/A | When a function requires an argument that is not relevant to the test |
| **Fake** | Create a working, lightweight substitute 9 | State Verification 9 | For dependencies with complex state, like a database, where an in-memory version is feasible |
| **Stub** | Provide canned answers 9 | State Verification 9 | When the test needs to control the return value of a dependency, but not verify its call 21 |
| **Spy** | Record information about calls 9 | Behavior Verification 9 | When you need to verify that a method was called, but a full mock is not required |
| **Mock** | Verify expected interactions 9 | Behavior Verification 9 | When the core purpose of the test is to ensure a specific interaction took place |

---

## **Part 3: The Python Test Standard: Tools and Conventions**

### **Choosing a Professional Testing Framework: Why pytest is the Modern Standard**

The choice of a testing framework is a strategic decision that directly influences the quality, maintainability, and efficiency of a test suite. For a modern, professional Python codebase, pytest is the recommended framework. While unittest is a standard library module, pytest offers a superior developer experience and a more modern approach that will make it easier for the team to adopt and maintain the new conventions.

| Feature | pytest | unittest |  |  |
| :---- | :---- | :---- | :---- | :---- |
| **Syntax** | Concise and readable.4 Uses standard | assert statements.4 | Verbose and boilerplate-heavy.4 Requires | TestCase classes and specific assertion methods like self.assertEqual().22 |
| **Fixtures** | Powerful, simple, and reusable fixture model.4 | Relies on setUp() and tearDown() methods, which can become complex.23 |  |  |
| **Parameterization** | Built-in, elegant support for running a test with multiple data sets.4 | Limited native support for parameterization.4 |  |  |
| **Assertion Introspection** | Provides a detailed, contextual explanation of why an assertion failed.4 | Requires explicit assertion methods to provide a clear failure message.4 |  |  |
| **Ecosystem** | Rich plugin ecosystem for enhanced functionality.4 | Part of the Python Standard Library, no installation required.4 |  |  |
| **Mocking** | Simplifies mocking with the mocker fixture via pytest-mock.5 | Requires manual import and use of unittest.mock's context managers or decorators.17 |  |  |

The choice of pytest is not simply a matter of technical preference; it is a strategic decision that facilitates a cultural shift toward better testing practices. The very design of pytest encourages cleaner, more focused, and more readable tests. Its concise syntax reduces the amount of boilerplate code, allowing developers to concentrate on the test's logic rather than the framework's structure.22 The powerful fixture system simplifies the process of setting up and tearing down test environments, which in turn encourages developers to write more isolated and deterministic tests. This inherent simplicity makes it easier for the team to adopt and adhere to the new standards, ensuring that the new conventions are not only documented but are actively practiced.

### **Practical Conventions for Code and Structure**

To establish a professional standard, consistency and clarity are paramount. The following conventions should be adopted for all new test development.

#### **Test Logic Structure: The Arrange-Act-Assert (AAA) Pattern**

The Arrange-Act-Assert (AAA) pattern is a widely recognized and language-agnostic approach to structuring test logic. This pattern divides each test into three distinct phases to improve readability, maintainability, and separation of concerns.6

1. **Arrange:** This phase involves setting up the test environment. It includes creating the necessary objects, configuring dependencies (e.g., using test doubles), and setting up the initial state for the test to run.6  
2. **Act:** This is the single, focused action of the test. It involves executing the specific code or method under test.6 The action should be concise and directly address the behavior being validated.  
3. **Assert:** This final phase verifies the outcome of the Act phase. It uses assertion methods to confirm that the actual results match the expected values, whether it is a return value, a side effect, or a change in state.6

By following the AAA pattern, each test tells a clear, self-contained story. It is a simple yet powerful structure that ensures tests are easy to understand and debug, and it provides a consistent format that can be applied across all projects and developers.

#### **Test Naming Conventions**

Test names should be descriptive and reveal the intention of the test, rather than just its function.7 This practice improves the readability and maintainability of the test suite.

* **File and Class Naming:** Test files should be named test\_\*.py or \*\_test.py. Test classes should be prefixed with Test.25  
* **Method Naming:** Test method names must be descriptive. A highly effective convention is to follow the GIVEN-WHEN-THEN pattern, which aligns directly with the AAA structure.7  
  * **Poor Name:** test\_login  
  * **Good Name:** test\_given\_valid\_username\_and\_password\_when\_user\_logs\_in\_then\_access\_token\_is\_returned

This descriptive naming convention provides a clear, human-readable documentation of the test's purpose and its expected behavior.

#### **Project Structure and Imports**

A well-structured project is essential for managing test code and dependencies. A recommended layout is the src layout, where the application's top-level package resides in a sub-directory named src/ and test code is placed in a separate top-level tests/ directory.26

* **Rationale for src Layout:** This structure prevents accidental usage of in-development code by ensuring that tests are always run against the installed package.27 It also provides a clear separation between the application's source code and the test suite, which is a key best practice.26  
* **Imports:** Within the tests/ directory, all imports of application code should be absolute, referencing the top-level package (e.g., from my\_package.my\_module import MyClass).29 This practice avoids confusion with relative imports and ensures consistent import behavior.29

---

## **Part 4: Implementing the New Standard: A Roadmap**

### **The "Mocking Framework" for a pytest World: pytest-mock**

To further simplify the mocking process and reduce boilerplate, the use of pytest-mock is highly recommended. While unittest.mock is part of the standard library, pytest-mock is a thin wrapper that leverages pytest's superior fixture system to provide a more elegant and readable mocking experience.5

pytest-mock provides a mocker fixture that is automatically available to every test function. This eliminates the need for manual imports of patch and the use of context managers or decorators, as required by unittest.mock. The mocker fixture also automatically handles the cleanup and un-patching of mocked objects after a test is completed.5 This automated setup and teardown simplifies test code, making it easier to write focused, clean, and maintainable tests.

### **Practical Guidance for Deciding When to Mock**

With the new conventions and tools in place, the team needs a clear rulebook for when to use a mock versus when to use a real object or a different test double. The core principle is to use a mock only when a real object is impractical or impossible to use in a unit test.15

The most appropriate use cases for mocking are dependencies that are:

* **Non-deterministic:** A dependency that returns the current time, random numbers, or a value from a sensor.15  
* **Slow:** An object that performs network I/O, database queries, or file system operations.19  
* **Difficult to set up:** A dependency that requires a complex state to be replicated, such as a specific network error or an object that is not yet fully implemented.15

For dependencies that are none of the above—i.e., fast, deterministic, and easy to instantiate—the best practice is to use the real object in the test. This approach provides a truer sense of confidence because the test is validating the system's behavior using real components.19

### **Refactoring the Existing Test Suite**

The transition to the new standard does not require a complete rewrite of the existing test suite. A phased approach is more pragmatic and sustainable.

1. **Phase 1: New Test Development:** Immediately mandate that all new tests conform to the new conventions (AAA pattern, pytest, descriptive naming). This will prevent the existing problems from proliferating.  
2. **Phase 2: Targeted Refactoring:** Identify the most brittle and high-maintenance tests in the current suite—those with an excessive number of mocks or complex unittest setups. Refactor these specific tests using the new conventions. The benefits of refactoring these problematic tests will be immediately apparent to the team.  
3. **Phase 3: Integration-First Mindset:** When tests break due to a change in the codebase, use it as an opportunity to evaluate the test's value. Ask if an integration test would have been more appropriate than a fragile unit test with a mock. This gradual approach will shift the team's mental model toward the Testing Trophy heuristic, where validating the interaction between objects is prioritized over the rigid isolation of every single unit.

---

## **Conclusion and Recommendations**

A professional testing practice is a strategic asset for any software development team. The current testing conventions, plagued by an overuse of mocks, have created a brittle and unreliable test suite. This report outlines a new standard built on foundational principles of modern software testing, a strategic hierarchy of test types, and a precise taxonomy of test doubles.

By adopting the Testing Trophy heuristic and implementing the pragmatic, pytest-based conventions, the team can build a test suite that is a robust safety net rather than a maintenance burden. The new conventions will lead to a more reliable, maintainable, and readable test suite. The test suite will no longer be a source of frustration but a source of confidence, allowing the team to move faster and deliver a higher-quality product.

It is recommended to immediately implement a phased plan for this transition. A clear training session should be held to introduce the new philosophy, conventions, and tools. All new test development should adhere to the new standard, and a gradual refactoring of the most problematic existing tests should begin. By embracing a disciplined, strategic approach to testing, the team will produce higher-quality software and establish a technical practice that is truly professional and modern.

#### **Citerade verk**

1. A complete philosophy of software testing in under 50 words | by Paul Martin | Medium, hämtad augusti 18, 2025, [https://medium.com/@contextdependence/a-complete-philosophy-of-software-testing-in-under-50-words-d96bc416e142](https://medium.com/@contextdependence/a-complete-philosophy-of-software-testing-in-under-50-words-d96bc416e142)  
2. Using the Testing Trophy heuristic | by Michael Scotto | The Quality ..., hämtad augusti 18, 2025, [https://thequalityindex.com/using-the-testing-trophy-heuristic-41a9596b8cf3](https://thequalityindex.com/using-the-testing-trophy-heuristic-41a9596b8cf3)  
3. Understanding the Testing Pyramid and Testing Trophy: Tools, Strategies, and Challenges, hämtad augusti 18, 2025, [https://dev.to/craftedwithintent/understanding-the-testing-pyramid-and-testing-trophy-tools-strategies-and-challenges-k1j](https://dev.to/craftedwithintent/understanding-the-testing-pyramid-and-testing-trophy-tools-strategies-and-challenges-k1j)  
4. pytest vs Unittest, Which is Better? \- JetBrains Guide, hämtad augusti 18, 2025, [https://www.jetbrains.com/guide/pytest/links/pytest-v-unittest/](https://www.jetbrains.com/guide/pytest/links/pytest-v-unittest/)  
5. pytest-mock vs unittest.mock: Simplifying Mocking in Python Tests ..., hämtad augusti 18, 2025, [https://codecut.ai/pytest-mock-vs-unittest-mock-simplifying-mocking-in-python-tests/](https://codecut.ai/pytest-mock-vs-unittest-mock-simplifying-mocking-in-python-tests/)  
6. The Arrange, Act, and Assert (AAA) Pattern in Unit Test Automation ..., hämtad augusti 18, 2025, [https://semaphore.io/blog/aaa-pattern-test-automation](https://semaphore.io/blog/aaa-pattern-test-automation)  
7. Tips and Tricks \- Testing Naming Conventions \- GIVEN-WHEN ..., hämtad augusti 18, 2025, [https://testdriven.io/tips/0f25ebb7-d5c1-4040-b78e-ac48e8f0a014/](https://testdriven.io/tips/0f25ebb7-d5c1-4040-b78e-ac48e8f0a014/)  
8. Test Doubles: Mocks, Stubs, and More \- objc.io, hämtad augusti 18, 2025, [https://www.objc.io/issue-15/mocking-stubbing.html](https://www.objc.io/issue-15/mocking-stubbing.html)  
9. Test Double \- Martin Fowler, hämtad augusti 18, 2025, [https://martinfowler.com/bliki/TestDouble.html](https://martinfowler.com/bliki/TestDouble.html)  
10. Object Oriented Testing in Software Testing \- GeeksforGeeks, hämtad augusti 18, 2025, [https://www.geeksforgeeks.org/software-testing/object-oriented-testing-in-software-testing/](https://www.geeksforgeeks.org/software-testing/object-oriented-testing-in-software-testing/)  
11. Object-Oriented Analysis and Design(OOAD) \- GeeksforGeeks, hämtad augusti 18, 2025, [https://www.geeksforgeeks.org/software-engineering/object-oriented-analysis-and-design/](https://www.geeksforgeeks.org/software-engineering/object-oriented-analysis-and-design/)  
12. Principles of Software testing \- GeeksforGeeks, hämtad augusti 18, 2025, [https://www.geeksforgeeks.org/software-engineering/software-engineering-seven-principles-of-software-testing/](https://www.geeksforgeeks.org/software-engineering/software-engineering-seven-principles-of-software-testing/)  
13. Differences Between Functional, Unit and Integration Testing, hämtad augusti 18, 2025, [https://www.headspin.io/blog/unit-integration-and-functional-testing-4-main-points-of-difference](https://www.headspin.io/blog/unit-integration-and-functional-testing-4-main-points-of-difference)  
14. Unit Test vs Integration Test: What are the differences? | BrowserStack, hämtad augusti 18, 2025, [https://www.browserstack.com/guide/unit-testing-vs-integration-testing](https://www.browserstack.com/guide/unit-testing-vs-integration-testing)  
15. Mock object \- Wikipedia, hämtad augusti 18, 2025, [https://en.wikipedia.org/wiki/Mock\_object](https://en.wikipedia.org/wiki/Mock_object)  
16. The Risks of Mocking Frameworks: How Too Much Mocking Leads ..., hämtad augusti 18, 2025, [https://svenruppert.com/2024/11/05/the-risks-of-mocking-frameworks-how-too-much-mocking-leads-to-unrealistic-tests/](https://svenruppert.com/2024/11/05/the-risks-of-mocking-frameworks-how-too-much-mocking-leads-to-unrealistic-tests/)  
17. Python Mock Library: A Comprehensive Guide to Effective Testing \- GeeksforGeeks, hämtad augusti 18, 2025, [https://www.geeksforgeeks.org/python/python-mock-library/](https://www.geeksforgeeks.org/python/python-mock-library/)  
18. Prefer test-doubles over mocking frameworks \- Steve Dunn, hämtad augusti 18, 2025, [https://dunnhq.com/posts/2024/prefer-test-doubles-over-mocking/](https://dunnhq.com/posts/2024/prefer-test-doubles-over-mocking/)  
19. Mocks or real classes? \[duplicate\] \- unit testing \- Stack Overflow, hämtad augusti 18, 2025, [https://stackoverflow.com/questions/180413/mocks-or-real-classes](https://stackoverflow.com/questions/180413/mocks-or-real-classes)  
20. ArticleS.PaulPagel.OverMocking \- ButUncleBob.com, hämtad augusti 18, 2025, [http://butunclebob.com/ArticleS.PaulPagel.OverMocking](http://butunclebob.com/ArticleS.PaulPagel.OverMocking)  
21. Mocking and Stubbing for Effective Unit Test Generation \- Zencoder, hämtad augusti 18, 2025, [https://zencoder.ai/blog/effective-unit-tests-mocking-stubbing](https://zencoder.ai/blog/effective-unit-tests-mocking-stubbing)  
22. Pytest vs. Unittest: Which Is Better? | The PyCharm Blog, hämtad augusti 18, 2025, [https://blog.jetbrains.com/pycharm/2024/03/pytest-vs-unittest/](https://blog.jetbrains.com/pycharm/2024/03/pytest-vs-unittest/)  
23. pytest vs unittest comparison of testing frameworks \- Knapsack Pro, hämtad augusti 18, 2025, [https://knapsackpro.com/testing\_frameworks/difference\_between/pytest/vs/unittest](https://knapsackpro.com/testing_frameworks/difference_between/pytest/vs/unittest)  
24. Speed Up Unit Test Coding with the Arrange-Act-Assert Test Pattern \- DragonSpears, hämtad augusti 18, 2025, [https://www.dragonspears.com/blog/speed-up-unit-test-coding-with-the-arrange-act-assert-test-pattern](https://www.dragonspears.com/blog/speed-up-unit-test-coding-with-the-arrange-act-assert-test-pattern)  
25. codefresh.io, hämtad augusti 18, 2025, [https://codefresh.io/learn/unit-testing/unit-testing-in-python-quick-tutorial-and-4-best-practices/\#:\~:text=Using%20Proper%20Naming%20Conventions\&text=readability%20and%20maintainability.-,By%20convention%2C%20test%20classes%20should%20start%20with%20the%20word%20%E2%80%9CTest,of%20what%20the%20test%20does.](https://codefresh.io/learn/unit-testing/unit-testing-in-python-quick-tutorial-and-4-best-practices/#:~:text=Using%20Proper%20Naming%20Conventions&text=readability%20and%20maintainability.-,By%20convention%2C%20test%20classes%20should%20start%20with%20the%20word%20%E2%80%9CTest,of%20what%20the%20test%20does.)  
26. Good Integration Practices \- pytest documentation, hämtad augusti 18, 2025, [https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html)  
27. src layout vs flat layout \- Python Packaging User Guide, hämtad augusti 18, 2025, [https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)  
28. Typical Directory structure for python tests \- GitHub Gist, hämtad augusti 18, 2025, [https://gist.github.com/tasdikrahman/2bdb3fb31136a3768fac](https://gist.github.com/tasdikrahman/2bdb3fb31136a3768fac)  
29. Structuring Your Project \- The Hitchhiker's Guide to Python, hämtad augusti 18, 2025, [https://docs.python-guide.org/writing/structure/](https://docs.python-guide.org/writing/structure/)