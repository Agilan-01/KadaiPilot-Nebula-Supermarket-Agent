# 🛒 KadaiPilot AI — Nebula Supermarket Ops Agent

<p align="center">

**Telegram-first AI Agent for Indian Kirana & Supermarket Operations**

Natural Language • Inventory • Billing • GST • Khata • Analytics • Persistent Memory

</p>

---

## 📌 Overview

**KadaiPilot AI** is an agent-first supermarket operations assistant designed for the **Nebula Supermarket Ops Agent** challenge.

The system allows a supermarket owner or operator to manage day-to-day store operations directly through **Telegram using natural language**.

Instead of building a traditional admin dashboard with forms, tables, and CRUD screens, KadaiPilot uses Telegram as the primary interface and an AI agent as the orchestration layer.

The agent interprets natural-language requests, determines the required operation, calls the appropriate business tools, validates the result, updates the persistent database, and communicates the result back to the user.

### Example

A store owner can simply send:

> "I need 2 kg sugar, 1 atta packet and 4 Maggi."

The agent can understand the request, identify the products, create a draft bill, calculate the applicable taxes, and wait for confirmation before finalizing the sale.

---

# 🎯 Project Objective

The objective of KadaiPilot is to demonstrate how an AI agent can operate a realistic Indian supermarket while maintaining deterministic business rules.

The system focuses on:

- Natural-language store operations
- Persistent inventory
- Conversational billing
- GST-aware pricing
- Customer khata management
- Safe stock handling
- Persistent operational memory
- PDF invoice generation
- Weekly sales analytics
- Telegram-based interaction

The AI is responsible for **reasoning and orchestration**, while important business rules remain inside deterministic application tools.

---

# ✨ Key Features

## 🤖 AI Agent

KadaiPilot uses an AI agent to interpret natural-language supermarket requests.

The agent can:

- Understand conversational requests
- Decide which business tool is required
- Ask clarification questions
- Perform multi-step operations
- Read tool results
- Continue reasoning based on database state
- Maintain conversational context
- Use persistent business memory

Example:

```text
User:
Show me the low-stock items and tell me what I should reorder.

Agent:
[Checks inventory]
[Identifies low-stock products]
[Returns the relevant products]
