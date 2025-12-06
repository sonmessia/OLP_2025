---
sidebar_position: 1
title: Contributing Guide
---

# Contributing to GreenWave

First off, thank you for considering contributing to GreenWave! It's people like you that make this project such a great tool.

We welcome contributions from everyone. By participating in this project, you agree to abide by our [Code of Conduct](./code-of-conduct.md).

:::info
**Goal:** We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
  :::

## Getting Started

### 1. Create an Issue

Before you start writing code, please check the **Issues** board.

- If you find an existing issue that matches what you want to do, leave a comment to let us know you're working on it.
- If not, [open a new issue](https://github.com/your-org/greenwave/issues/new) to discuss your idea.

### 2. Fork the Repository

Fork the repository to your own GitHub account.

### 3. Create a Branch

Create a new branch for your changes. We recommend using a descriptive name:

```bash
git checkout -b feat/my-new-feature
# or
git checkout -b fix/login-bug
```

### 4. Code & Test

Make your changes in the codebase.

- Ensure your code follows our coding standards.
- Write unit tests if you are adding new logic.
- Run existing tests to make sure you haven't broken anything.

### 5. Commit Your Changes

We follow a strict **Commit Convention**. Please read our guide before committing:

:::tip
**[Read the Git Commit Convention Guide](./commit-convention.md)**
:::

### 6. Submit a Pull Request (PR)

Push your branch to your fork and submit a Pull Request to the `main` branch of the GreenWave repository.

- Provide a clear title and description.
- Link to the related issue (e.g., `Closes #123`).
- Wait for a code review!

## Coding Standards

### Frontend

- We use **React** with **TypeScript**.
- Styling is done via **Tailwind CSS**.
- Follow the existing folder structure.

### Backend

- We use **Python** (FastAPI/Django/etc - adjust based on actual stack).
- Follow **PEP 8** guidelines.

### AI/ML

- Document your model architecture.
- Provide training scripts and metrics.

:::warning
**Important:** PRs that do not pass the CI/CD checks (linting, tests) will not be merged.
:::

## Need Help?

If you have any questions, feel free to reach out to the maintainers or ask in the [Discussions](https://github.com/your-org/greenwave/discussions) tab.

Happy Coding! 🎉
