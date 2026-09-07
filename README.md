# 🛒 KadaiPilot AI — Nebula Supermarket Ops Agent

> **A Telegram-first AI operations agent for running an Indian kirana / supermarket through natural language.**

KadaiPilot AI is an agent-first supermarket operations assistant built for the **Nebula Supermarket Ops Agent** challenge.

Instead of providing a traditional admin dashboard or CRUD interface, KadaiPilot turns Telegram into the operating interface of the store. The AI agent interprets natural-language requests, reasons about the current store state, calls business tools, validates the operation, and returns the result directly in Telegram.

---

## 🚀 What Makes KadaiPilot Different?

KadaiPilot is designed around an **AI agent + business tools + persistent database** architecture.

The LLM does not directly modify inventory or financial records.

Instead:

```text
Telegram Message
       ↓
   AI Agent
       ↓
 Understand intent
       ↓
 Select business tool
       ↓
 Validate business rules
       ↓
 SQLite Database
       ↓
 Tool Result
       ↓
    AI Agent
       ↓
 Telegram Response