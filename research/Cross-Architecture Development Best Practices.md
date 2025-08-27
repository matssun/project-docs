

# **Report on Best Practices for a Multi-Architecture Development Environment**

### **1\. Executive Summary: From Ad-Hoc to Automated**

#### **1.1. The Current State: A Diagnosis of Fragility**

The current development environment, characterized by source code residing on a shared Dropbox folder, presents a series of fundamental vulnerabilities that jeopardize the software development lifecycle. The primary motivation for this setup, as articulated, is the perceived benefit of "immediate" updates and the ability to perform parallel work on a single Git branch.1 While seemingly convenient, this approach introduces a critical layer of fragility, as the underlying file synchronization system is not designed to function as a collaborative source code repository.2 The observation of "mismatch between the different architectures" when executables are created is not an isolated problem but a direct symptom of a flawed foundational architecture. The root cause lies in the ad-hoc nature of the shared workspace, which fundamentally subverts the principles of a distributed version control system (DVCS) and an automated, reproducible build process.

#### **1.2. The Strategic Solution: A Three-Pillar Approach**

To address these vulnerabilities and establish a robust, scalable development environment, a strategic migration is necessary, built upon three core pillars:

* **Pillar 1: Embrace Git as the Single Source of Truth.** The foundation of a reliable development environment must be a dedicated source code management (SCM) system. By moving the codebase from a shared filesystem to a Git repository, the team can formalize a collaboration workflow that ensures every developer operates from a consistent, verifiable, and conflict-minimized source. This transition empowers a modern workflow, such as Trunk-Based Development, which naturally aligns with the team's current desire for parallel work while providing the necessary guardrails for code integrity.4  
* **Pillar 2: Standardize the Build Process with Containerization.** The "it works on my machine" problem, particularly acute in multi-architecture environments, is effectively solved through containerization. Tools like Docker, specifically with the buildx extension, provide a consistent and portable build environment that encapsulates all dependencies. This approach eliminates environmental variances and natively supports the creation of multi-architecture executables and container images from a single source.6  
* **Pillar 3: Automate with CI/CD.** A Continuous Integration/Continuous Delivery (CI/CD) pipeline serves as the final enforcement mechanism and quality gate. This automated workflow triggers a build and test sequence for every code change, ensuring that the codebase remains "green" (stable and deployable) at all times.7 By integrating multi-architecture builds into the pipeline, the system can automatically validate that all executables for all target platforms are built correctly, providing immediate feedback and preventing downstream deployment failures.

### **2\. Foundational Analysis: The Perils of Shared Filesystem Workspaces**

#### **2.1. Incompatibility with Distributed Version Control (DVCS)**

The current reliance on a shared Dropbox folder for source code is a critical misapplication of technology. Dropbox is a consumer-grade file synchronization service designed for sharing static content, not for managing the dynamic, concurrent changes inherent in a software codebase.2 This approach creates a false sense of security and control, as it fundamentally contradicts the core principles of a distributed version control system (DVCS) like Git.

A DVCS is designed on a peer-to-peer model where every developer possesses a complete, self-contained copy of the entire repository history.8 This architecture provides immense benefits, including the ability to work offline, perform common operations instantaneously, and maintain reliable, redundant backups across every developer's machine.8 The use of a shared filesystem, in contrast, creates a single, central point of failure that bypasses these advantages. The file sharing platform's own APIs and developer communities confirm that they are built for integrating file-sharing functionality, not for serving as a backend for a Git repository.2

The perception of "immediate updates" is an illusion. While a file change may be visible on a remote machine's file explorer, the actual synchronization of the file content across the network can be subject to significant latency and bandwidth constraints, particularly with large files or frequent updates.1 This creates a subtle but dangerous form of state inconsistency. A developer's local build process might begin operating on a file that has not been fully synced, or a concurrent write from another machine could introduce a partial or corrupted file state. This silent latency undermines the integrity of the local build environment and is a primary source of the very inconsistencies the user is experiencing.

#### **2.2. The Architectural Mismatch and the Risk of Data Corruption**

The issue of executable "mismatch" is not merely a consequence of compiling on different hardware. It is a profound symptom of the instability of the shared file system itself. When multiple users perform concurrent read and write operations on the same files—a routine occurrence in a shared development environment—the underlying file system's cache management and locking mechanisms are susceptible to race conditions.10

A detailed analysis of this problem, as documented in a Microsoft Support article, reveals that data corruption can occur when a user's local cache of file attributes is not updated in time to reflect changes made by another user.10 This can result in one user's changes silently overwriting another's, leading to a corrupted or inconsistent file state.10 In the context of a software project, this means that even if a developer's local Git branch is theoretically correct, the physical files in the working directory may be silently corrupted or inconsistent due to the shared filesystem's operational flaws.

While a DVCS like Git is designed to prevent data loss at the repository level, its integrity is dependent on the reliability of the local working directory. When the working directory is compromised by an unstable file system, the entire build process is built on a foundation of sand. This underlying file system fragility, not just the multi-architecture difference, is the most profound source of the non-reproducibility and "mismatches" observed during the build process.

### **3\. The New Paradigm: A Git-Centric Development Workflow**

#### **3.1. Embracing Distributed Version Control as the Single Source of Truth**

The migration to a Git-centric workflow is a prerequisite for building a stable and scalable development environment. Unlike a centralized model, a DVCS like Git ensures that every developer possesses a full, local copy of the repository and its entire change history.8 This provides a single, verifiable, and consistent source of truth for the codebase, independent of the underlying filesystem's quirks.

The core benefits of this approach are substantial:

* **Offline Productivity:** Developers can work productively on commits, branches, and history exploration without a network connection, pushing their changes only when they are ready to share them.8  
* **Speed and Efficiency:** Most routine operations, such as committing changes or viewing the project's history, are performed locally and are therefore instantaneous, without the latency of network communication.8  
* **Reliable Backups:** The distributed nature of Git means that every developer's local repository effectively serves as a full backup of the codebase, eliminating the risk of a single point of failure.8  
* **Flexible Workflows:** Git's architecture supports a wide range of collaborative models, from simple centralized workflows to complex integration-manager patterns.11

#### **3.2. Best Practices in Branching and Collaboration**

Once a Git-based workflow is established, the next step is to choose a branching strategy. While many options exist, two are most common: Gitflow and Trunk-Based Development (TBD).4

* **Gitflow:** This model, popularized in the past, relies on multiple, long-lived branches (e.g., main, develop, and various feature branches). This complexity can lead to larger, less frequent merges, increasing the likelihood and severity of merge conflicts.4  
* **Trunk-Based Development (TBD):** This is the recommended modern approach. TBD is a simpler, more agile practice where developers merge small, frequent commits directly into a single, core main or trunk branch.4 This model significantly reduces the risk of merge conflicts and makes them easier to resolve when they do occur, as the changesets are minimal.4 TBD also requires and enables Continuous Integration, a critical component for ensuring code stability.4 The user's current workflow of "parallell work... on the same git branch" is an informal and incomplete version of TBD that can be formalized with proper tooling and process.

### **4\. Solving the Multi-Architecture Build Problem: Strategies and Tools**

#### **4.1. Overview of Multi-Platform Build Concepts**

The ability to create executables for different machine architectures is a non-trivial challenge that requires a fundamental shift in the build process. A clear understanding of core concepts is essential:

* **Native Compilation:** This is the most common form of compilation, where a compiler running on a machine with a specific architecture (e.g., an x86 machine) produces an executable designed to run on that same architecture.13  
* **Cross-Compilation:** This is the process of compiling code on a host machine for a different target architecture (e.g., building an ARM executable on an x86 machine).13 This is a core requirement for any robust multi-platform build system.  
* **Emulation:** This technique involves using software (e.g., QEMU) to allow a host machine to execute code compiled for a different target architecture.6 This is often used during the build process to run intermediate steps or tests for the target platform.

#### **4.2. Containerization: The Modern Solution for Cross-Platform Development**

Containerization, particularly with Docker, provides a powerful solution to the multi-architecture build problem by abstracting the build environment from the host machine.6 A Docker container bundles the application and all its dependencies into a single, isolated unit, ensuring that the build process is identical and reproducible across all developer machines, regardless of their native operating system or CPU architecture.6

##### **4.2.1. The Role of Docker buildx**

The docker buildx tool is a modern, streamlined solution for managing multi-architecture builds. It automates a process that was once manual and complex, allowing for the creation of multi-platform images with a single command.6

At its core, buildx leverages a manifest list, which is a single image tag that points to multiple, distinct images, each compiled for a specific architecture.6 When a user pulls this image, the Docker Engine automatically selects the correct variant based on the host's architecture.6 This eliminates the need for developers or end-users to manually manage separate image tags for each platform. The older, manual approach, which required building and pushing each image separately before combining them with the

docker manifest create command, is now largely superseded by the efficiency of buildx.19

##### **4.2.2. Emulation vs. Native Builders: Performance Trade-offs**

There are two primary strategies for multi-architecture builds using buildx, each with its own performance characteristics:

* **QEMU Emulation:** This is the simplest strategy, as it requires only a single host machine. By using QEMU, the build process can run a foreign architecture's binaries during the build, allowing an x86 machine, for example, to build an ARM image.6 While simple, this method introduces a performance overhead due to the emulation layer.17  
* **Multi-Node Builders:** This strategy is the most performant and reliable for complex or CPU-intensive builds. It involves creating a buildx builder instance that is backed by multiple native machines—for example, one x86 machine and one ARM machine.6 The build process is then distributed to the appropriate native machine, avoiding the performance penalty of emulation. This approach is ideal for CI/CD pipelines where multiple machines with different architectures are available.20

#### **4.3. Advanced Build Systems for Cross-Compilation**

For projects with significant complexity, particularly those written in C++, using a dedicated build system is essential. These systems, designed for scalability and cross-platform compatibility, can be integrated into the containerized build process.

##### **4.3.1. CMake: The De Facto Standard for C++**

CMake is a powerful and comprehensive software build system that serves as the de facto standard for C++ development.4 It provides a single-source solution for building on multiple platforms and natively supports cross-compilation.21

A key mechanism in CMake for managing cross-compilation is the use of a toolchain file.22 This file explicitly tells CMake everything it needs to know about the target platform, including the location of the compiler, linker, and system libraries.22 This separation of the build environment (the host) from the target environment ensures that the build process is clean, predictable, and reproducible, regardless of where it is executed.23

##### **4.3.2. Bazel: Scalability for the Monorepo**

For extremely large, multi-language, and multi-platform projects, Bazel is an increasingly popular choice. Used by industry leaders like Google and Dropbox, Bazel is built for speed and correctness, rebuilding only what is absolutely necessary with advanced caching and parallel execution.24

The user's experience with a shared Dropbox folder, a consumer product from the same company that uses Bazel for its mission-critical infrastructure, presents a powerful case study. This striking contrast highlights the strategic importance of selecting a tool that is fit for purpose, rather than attempting to adapt a consumer-grade solution to a professional-grade problem. The very problems of reproducibility and scalability the user is facing are solved internally by the very company whose product they are misusing, demonstrating the stark difference between an ad-hoc, informal setup and a professionally engineered development workflow.

### **5\. The Automation Imperative: Integrating with a CI/CD Pipeline**

#### **5.1. Core Principles of CI/CD**

Continuous Integration (CI) and Continuous Delivery/Deployment (CD) are modern software development practices that automate the process of building, testing, and deploying code.7 A CI/CD pipeline is a series of automated steps that act as a quality gate, ensuring that only validated code moves forward.7 CI's practice of frequently integrating code changes into a shared repository and automatically validating them is a perfect complement to Trunk-Based Development, as it ensures the

main branch remains stable and always ready for deployment.4

#### **5.2. Designing a Multi-Architecture CI/CD Pipeline**

A robust CI/CD pipeline for a multi-architecture project should be designed to automatically build and test for all target platforms upon every code push. The key to this is a **matrix strategy**, a feature available in modern CI/CD tools like GitHub Actions.27 A matrix allows a single workflow to define a set of jobs that run concurrently with different configurations (e.g.,

architecture: \[amd64, arm64\]), abstracting away the complexity of managing separate build configurations for each platform.27

#### **5.3. Practical Implementations with GitHub Actions**

A GitHub Actions workflow provides an ideal and highly practical solution for implementing this architecture. The process involves a series of sequential and parallel steps:

1. **Checkout Code and Setup Buildx:** The pipeline begins by checking out the code from the Git repository using actions/checkout. It then uses a dedicated action, docker/setup-buildx-action, to install and configure buildx, preparing the environment for multi-platform builds.27  
2. **Build and Push Platform-Specific Images:** A matrix-based job runs concurrently for each target architecture (e.g., linux/amd64 and linux/arm64). This job builds the container image for its specific architecture and pushes it to a container registry (e.g., Docker Hub, GitHub Package Registry, or Amazon ECR) with a unique tag that includes the architecture name.27  
3. **Create and Push the Manifest:** A separate job, configured to run after the successful completion of all architecture-specific build jobs, is responsible for creating the manifest list. This job uses the docker buildx imagetools create command, referencing the specific image digests generated in the previous step, to combine them under a single, human-readable tag (e.g., your-app:latest).27

This process ensures that a single code change triggers a full, automated validation cycle across all target architectures, providing immediate feedback and ensuring that every build is reproducible and correct before it is ever deployed.

### **6\. Recommendations and Implementation Roadmap**

The following is a strategic, phased roadmap for migrating from the current ad-hoc setup to a modern, professional development environment.

#### **6.1. A Phased Transition Plan**

* **Phase 1: Foundation.**  
  * **Action:** Migrate all source code from the shared Dropbox folder to a new Git repository on a service like GitHub.  
  * **Action:** Establish and enforce a Trunk-Based Development (TBD) branching strategy. All new work should be done in small, short-lived branches that are merged into main at least daily.  
* **Phase 2: Environment Standardization.**  
  * **Action:** Containerize the build environment. Create a Dockerfile that contains all necessary compilers, libraries, and tools for building the application.  
  * **Action:** Configure and test a single-architecture Docker build locally to ensure a fully reproducible build from a clean container.  
* **Phase 3: Automation and Multi-Arch.**  
  * **Action:** Implement a GitHub Actions CI/CD pipeline.  
  * **Action:** Add a buildx-based multi-architecture build job to the pipeline that automatically builds the application for all target architectures upon every push to the main branch. This is the culmination of the entire process, automating the validation of executable correctness.

#### **6.2. Tool and Workflow Recommendations Matrix**

The following tables provide a structured analysis of the recommended tools and strategies, enabling a data-driven decision-making process based on project size, language, and performance requirements.

**Table 1: Comparison of Build Systems**

| Tool | Key Features | Best For | Cross-Compilation Notes |
| :---- | :---- | :---- | :---- |
| **Docker buildx** | \- Multi-architecture builds via emulation or native builders. \- Containerizes the entire build environment. \- Creates a single manifest list for all architectures. | All projects, particularly those using containers for deployment. | The primary tool for managing multi-arch container images, using manifest lists and buildx. |
| **CMake** | \- Cross-platform and cross-architecture support. \- Language-agnostic, but de facto standard for C++. \- Out-of-source builds. | Projects written in C or C++, from small to large scale. | Requires a toolchain file to define compiler and library paths for the target architecture.22 |
| **Bazel** | \- Highly scalable and extensible. \- Optimized dependency analysis and parallel execution. \- Caching and remote execution support. | Extremely large, multi-language monorepos; projects requiring fast, reproducible builds at scale.24 | Natively handles multi-platform builds for various languages, including Go and C++, without separate tools.24 |

**Table 2: Multi-Architecture Build Strategies**

| Strategy | Pros | Cons | Best For |
| :---- | :---- | :---- | :---- |
| **QEMU Emulation** | \- Simple to set up on a single machine. \- Requires minimal changes to the build pipeline. | \- Slower performance due to CPU emulation. \- May not handle all complex build scenarios.17 | Small teams or personal projects with limited hardware resources; initial proof-of-concept builds.20 |
| **Multi-Node Builders** | \- Superior performance by leveraging native hardware. \- Avoids the overhead of emulation. \- Scalable for large, concurrent build jobs.6 | \- Requires access to and management of multiple machines with different architectures. | Large teams, enterprise environments, or projects where build speed is a critical factor.6 |
| **Cross-Compilation (in Dockerfile)** | \- Highly efficient if the language supports it (e.g., Go). \- The entire build process is self-contained within the Dockerfile.6 | \- Requires language-specific knowledge for cross-compilation. \- Not all languages or build systems support it transparently. | Languages like Go, which have excellent native cross-compilation support.6 |

### **7\. Conclusion: A Path to Reproducibility and Scalability**

The analysis demonstrates that the current reliance on a shared Dropbox folder for source code is a flawed architectural choice that introduces systemic instability and directly contributes to the observed multi-architecture build failures. The solution is not a simple tool change but a fundamental shift in the development paradigm. By adopting a Git-centric workflow, containerizing the build process with Docker and buildx, and automating validation with a CI/CD pipeline, the team can move from a fragile, ad-hoc process to a resilient, professional, and scalable one.

This transformation will solve the immediate problem of executable mismatches by ensuring that every build is performed in a consistent, controlled environment. Beyond this, it will fundamentally improve team collaboration, enhance code quality, and provide a reliable, auditable path from a code commit to a finished, deployable product, ready to run on any target architecture.

#### **Citerade verk**

1. File Sharing: The Pros & Cons with Basics to Eliminate Risk \- Bastionpoint Technology, hämtad augusti 26, 2025, [https://bastionpoint.com/blog/cybersecurity/file-sharing-basics-eliminate-risk/](https://bastionpoint.com/blog/cybersecurity/file-sharing-basics-eliminate-risk/)  
2. DBX Platform Developer Community & Support \- Dropbox.com, hämtad augusti 26, 2025, [https://www.dropbox.com/developers/support](https://www.dropbox.com/developers/support)  
3. Issues · dropbox/dropbox-sdk-js \- GitHub, hämtad augusti 26, 2025, [https://github.com/dropbox/dropbox-sdk-js/issues](https://github.com/dropbox/dropbox-sdk-js/issues)  
4. Trunk-based Development | Atlassian, hämtad augusti 26, 2025, [https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development)  
5. Trunk-Based Development Vs Git Flow: A Comparison | Assembla, hämtad augusti 26, 2025, [https://get.assembla.com/blog/trunk-based-development-vs-git-flow/](https://get.assembla.com/blog/trunk-based-development-vs-git-flow/)  
6. Multi-platform | Docker Docs, hämtad augusti 26, 2025, [https://docs.docker.com/build/building/multi-platform/](https://docs.docker.com/build/building/multi-platform/)  
7. Ultimate guide to CI/CD: Fundamentals to advanced implementation \- GitLab, hämtad augusti 26, 2025, [https://about.gitlab.com/blog/ultimate-guide-to-ci-cd-fundamentals-to-advanced-implementation/](https://about.gitlab.com/blog/ultimate-guide-to-ci-cd-fundamentals-to-advanced-implementation/)  
8. Distributed version control \- Wikipedia, hämtad augusti 26, 2025, [https://en.wikipedia.org/wiki/Distributed\_version\_control](https://en.wikipedia.org/wiki/Distributed_version_control)  
9. What is a distributed version control system? \- GitLab, hämtad augusti 26, 2025, [https://about.gitlab.com/topics/version-control/benefits-distributed-version-control-system/](https://about.gitlab.com/topics/version-control/benefits-distributed-version-control-system/)  
10. Data corruption when multiple users perform read and write operations to a shared file in the SMB2 environment \- Microsoft Support, hämtad augusti 26, 2025, [https://support.microsoft.com/en-us/topic/data-corruption-when-multiple-users-perform-read-and-write-operations-to-a-shared-file-in-the-smb2-environment-4bb67519-71b1-4588-c380-e4ceaa695418](https://support.microsoft.com/en-us/topic/data-corruption-when-multiple-users-perform-read-and-write-operations-to-a-shared-file-in-the-smb2-environment-4bb67519-71b1-4588-c380-e4ceaa695418)  
11. Distributed Workflows \- Git, hämtad augusti 26, 2025, [https://git-scm.com/book/ms/v2/Distributed-Git-Distributed-Workflows](https://git-scm.com/book/ms/v2/Distributed-Git-Distributed-Workflows)  
12. Distributed Workflows \- Pro Git, hämtad augusti 26, 2025, [http://iissnan.com/progit/html/en/ch5\_1.html](http://iissnan.com/progit/html/en/ch5_1.html)  
13. unix.stackexchange.com, hämtad augusti 26, 2025, [https://unix.stackexchange.com/questions/7022/what-is-the-difference-between-cross-compiling-and-native-compiling\#:\~:text=You%20use%20a%20cross%20compiler,compiler%20only%20produces%20native%20binaries.](https://unix.stackexchange.com/questions/7022/what-is-the-difference-between-cross-compiling-and-native-compiling#:~:text=You%20use%20a%20cross%20compiler,compiler%20only%20produces%20native%20binaries.)  
14. CROSS COMPILATION VS NATIVE COMPILATION \- Emblogic, hämtad augusti 26, 2025, [https://www.emblogic.com/blog/04/cross-compilation-vs-native-compilation/](https://www.emblogic.com/blog/04/cross-compilation-vs-native-compilation/)  
15. Cross-compilation \- .NET | Microsoft Learn, hämtad augusti 26, 2025, [https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/cross-compile](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/cross-compile)  
16. CrossCompiling \- Debian Wiki, hämtad augusti 26, 2025, [https://wiki.debian.org/CrossCompiling](https://wiki.debian.org/CrossCompiling)  
17. Build multi-architecture images for Arm workloads | Google Kubernetes Engine (GKE), hämtad augusti 26, 2025, [https://cloud.google.com/kubernetes-engine/docs/how-to/build-multi-arch-for-arm](https://cloud.google.com/kubernetes-engine/docs/how-to/build-multi-arch-for-arm)  
18. Mastering Docker for Cross-Platform Development with TypeScript | by @rnab | Jul, 2025, hämtad augusti 26, 2025, [https://arnab-k.medium.com/how-to-use-docker-for-cross-platform-development-a0fad8d1a1c1](https://arnab-k.medium.com/how-to-use-docker-for-cross-platform-development-a0fad8d1a1c1)  
19. Multi-arch build and images, the simple way | Docker, hämtad augusti 26, 2025, [https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/](https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/)  
20. Understanding Multi-arch Containers, Benefits and CI/CD Integration, hämtad augusti 26, 2025, [https://www.infracloud.io/blogs/multi-arch-containers-ci-cd-integration/](https://www.infracloud.io/blogs/multi-arch-containers-ci-cd-integration/)  
21. CMake \- Upgrade Your Software Build System, hämtad augusti 26, 2025, [https://cmake.org/](https://cmake.org/)  
22. cmake-toolchains(7) — CMake 4.1.0 Documentation, hämtad augusti 26, 2025, [https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html](https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html)  
23. Cross Compiling With CMake, hämtad augusti 26, 2025, [https://cmake.org/cmake/help/book/mastering-cmake/chapter/Cross%20Compiling%20With%20CMake.html](https://cmake.org/cmake/help/book/mastering-cmake/chapter/Cross%20Compiling%20With%20CMake.html)  
24. bazelbuild/bazel: a fast, scalable, multi-language and extensible build system \- GitHub, hämtad augusti 26, 2025, [https://github.com/bazelbuild/bazel](https://github.com/bazelbuild/bazel)  
25. Bazel to build, hämtad augusti 26, 2025, [https://bazel.build/](https://bazel.build/)  
26. What is CI/CD? \- Red Hat, hämtad augusti 26, 2025, [https://www.redhat.com/en/topics/devops/what-is-ci-cd](https://www.redhat.com/en/topics/devops/what-is-ci-cd)  
27. Building Multi-Platform Container Images with GitHub Actions | by ..., hämtad augusti 26, 2025, [https://medium.com/neudesic-innovation/building-multi-platform-container-images-with-github-actions-e495f9441ad3](https://medium.com/neudesic-innovation/building-multi-platform-container-images-with-github-actions-e495f9441ad3)  
28. Building multi-arch containers with GitHub Actions in AWS | Containers, hämtad augusti 26, 2025, [https://aws.amazon.com/blogs/containers/building-multi-arch-containers-with-github-actions-in-aws/](https://aws.amazon.com/blogs/containers/building-multi-arch-containers-with-github-actions-in-aws/)