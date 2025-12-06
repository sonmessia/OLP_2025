---
sidebar_position: 3
title: Commit Convention
---

<!--
 Copyright (c) 2025 Green Wave Team

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# Git Commit Convention

Welcome to the GreenWave git commit guide.

:::note Why do we need this?
**Git History is Documentation.**
A clean commit history helps reviewers understand what you did, speeds up debugging, and allows us to automatically generate **ChangeLogs**.
:::

We strictly follow the **[Conventional Commits](https://www.conventionalcommits.org/)** specification.

## 1. The Format

Each commit message consists of a **Header**, a **Body** (optional), and a **Footer** (optional).

```text
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

**Example:**

```text
feat(ai): implement new reward function based on CO2 levels

The old function only considered traffic flow. This new logic adds
a 50% weight for environmental impact using PM2.5 sensor data.

Closes #123
```

## 2. Header (Required)

The first line must not exceed **72 characters**.

### `type`

Must be one of the following:

| Type           | Description                                               | Example                                  |
| :------------- | :-------------------------------------------------------- | :--------------------------------------- |
| **`feat`**     | A new feature (MINOR version)                             | `feat(iot): add traci connection`        |
| **`fix`**      | A bug fix (PATCH version)                                 | `fix(backend): resolve timeout error`    |
| **`docs`**     | Documentation only changes                                | `docs: update setup guide`               |
| **`style`**    | Formatting, missing semi-colons, etc. (no code change)    | `style(ai): format code with black`      |
| **`refactor`** | A code change that neither fixes a bug nor adds a feature | `refactor(infra): optimize docker build` |
| **`perf`**     | A code change that improves performance                   | `perf(db): add index to query`           |
| **`test`**     | Adding missing tests or correcting existing tests         | `test(ai): add unit test for agent`      |
| **`chore`**    | Changes to the build process or auxiliary tools           | `chore(deps): upgrade numpy`             |
| **`ci`**       | Changes to our CI configuration files and scripts         | `ci: fix commitlint workflow`            |

### `scope`

Specific to **GreenWave**, indicating the module affected:

- **`infra`**: Docker, MongoDB, Orion-LD, Server.
- **`backend`**: API, Python scripts, Data ingestion.
- **`ai`**: RL Agents, Model training, TensorFlow/PyTorch.
- **`iot`**: SUMO, TraCI scripts, Sensors.
- **`frontend`**: Dashboard, UI.
- **`docs`**: README, Wiki.
- **`deps`**: `requirements.txt`, `package.json`, etc.

### `subject`

A short description of the change.

- ✅ **DO**: Use the **imperative mood** ("add", "change", "fix", "remove").
- ❌ **DON'T**: Use past tense ("added", "changed", "fixed").
- ❌ **DON'T**: Capitalize the first letter (unless it's a proper noun).
- ❌ **DON'T**: End with a period (.).

## 3. Body (Optional)

- Use when the subject is not enough to explain the _why_.
- Use the imperative mood.
- Explain **why** this change is necessary, not **how** (the code explains the how).

## 4. Footer (Optional)

Used for:

- **Breaking Changes**: Start with `BREAKING CHANGE: <description>`.
- **Referencing Issues**: `Closes #123`, `Fixes #456`.

## 5. Automation Tools

You don't have to remember all these rules! We have set up tools to help you.

### Option 1: CLI (Recommended)

Run the following command to start an interactive commit wizard:

```bash
npm run commit
```

It will guide you through the process:

```text
? Select the type of change that you're committing: (Use arrow keys)
❯ feat:     A new feature
  fix:      A bug fix
...
? What is the scope of this change: (ai)
? Write a short, imperative tense description: (implement reward function)
```

### Option 2: Manual Commit

If you use standard `git commit`, **Husky** will verify your message. If it doesn't match the rules, the commit will be rejected.

## 6. Cheat Sheet

| ❌ Bad               | ✅ Good                                        | Reason                      |
| :------------------- | :--------------------------------------------- | :-------------------------- |
| `Fixed bug`          | `fix(backend): resolve null pointer exception` | Missing scope, too vague.   |
| `Added new AI model` | `feat(ai): add dqn model implementation`       | Wrong tense ("Added").      |
| `update readme.`     | `docs: update install instructions in readme`  | Trailing period, too short. |
| `WIP`                | _(Don't commit WIP to main)_                   | Meaningless.                |

:::tip Pro Tip
Think of the commit message as completing this sentence:
**"If applied, this commit will..."**

- ... **add** a new feature. (Makes sense)
- ... **added** a new feature. (Grammatically incorrect in this context)
  :::

Happy Committing!
