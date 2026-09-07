📱 Telegram-First Interface

Telegram is the primary interface.

There is intentionally no:

Web dashboard
Admin panel
Separate billing website
CRUD form interface

The supermarket operator interacts with the system using Telegram messages.

Example:

/start

What products do we have?

How much Maggi is left?

Add 5 packets of Maggi to my bill.

Remove 2 packets.

Show the bill.

Finalize using UPI.
📦 Inventory Management

KadaiPilot maintains product-level inventory information.

Each product can contain:

Product name
SKU
Category
HSN code
GST rate
Unit
Loose/packaged status
Cost price
Selling price
MRP
Current quantity
Reorder level

Supported units include common supermarket units such as:

kg
g
litre
ml
packet
piece
dozen
Inventory operations

The agent can:

Search products
Add products
Receive stock
Check stock
Check low-stock items
Track selling price
Track cost price
Track reorder levels

Example:

User:
How much Tata Salt do we have?

Agent:
[Reads current quantity from database]
🧾 Conversational Billing

KadaiPilot supports multi-item conversational billing.

Example:

User:
Create a bill for 2 kg sugar,
1 packet of atta,
and 4 Maggi.

The agent creates a draft bill.

The user can then modify it.

User:
Remove the atta.
User:
Change Maggi to 6 packets.
User:
Show my bill.

The bill can be finalized only after the user confirms the transaction.

🔄 Draft Bill Workflow

KadaiPilot separates draft billing from finalized sales.

Natural-language order
        ↓
Draft bill
        ↓
Edit / Remove / Add items
        ↓
Preview bill
        ↓
User confirmation
        ↓
Finalize sale
        ↓
Atomic stock deduction
        ↓
Invoice generation
Important behavior

Stock is not permanently deducted while the bill is only a draft.

Stock is updated when the sale is finalized.

This prevents abandoned or incorrectly edited bills from corrupting inventory.

💰 Payment Methods

KadaiPilot supports common supermarket payment modes:

Cash
UPI
Card

Example:

Finalize the bill and pay by UPI.

The selected payment method is recorded with the finalized sale.

🧮 GST & Tax Calculation

The system supports product-level GST configuration.

Each SKU can contain:

HSN code
GST rate
Taxable price
Product quantity

For intra-state sales, GST is split into:

GST
├── CGST
└── SGST

Example:

Taxable value = ₹100
GST = 5%

CGST = ₹2.50
SGST = ₹2.50

Total = ₹105.00

Tax calculations are performed by deterministic application code rather than allowing the language model to invent tax values.

Money calculations use decimal arithmetic and controlled rounding.

👤 Khata / Customer Credit

KadaiPilot supports customer credit management.

A store operator can record credit using natural language.

Example:

Put ₹500 on Ramesh's credit.

The system records the credit entry.

The operator can then ask:

How much does Ramesh owe?

A payment can be recorded:

Ramesh paid ₹300.

The outstanding balance can then be queried again.

Khata capabilities
Customer creation
Credit entries
Payment entries
Outstanding balance
Customer history
📊 Sales & Store Analysis

KadaiPilot can retrieve store sales information and generate analysis.

Examples:

Show today's sales.
How much did we sell today?
Show low-stock products.
Generate this week's sales analysis.

The system can generate a real PowerPoint presentation for weekly analysis.

📄 PDF Invoice Generation

After a successful sale finalization, KadaiPilot generates a real PDF invoice.

The invoice can contain:

Store name
GSTIN
Invoice number
Date
Customer
Product details
Quantity
Unit price
Taxable value
GST
CGST
SGST
Total amount
Payment method

The PDF is generated using:

ReportLab

The resulting file can be sent directly to the customer/operator through Telegram.

📈 Weekly PPTX Analysis

KadaiPilot can generate a weekly sales analysis deck.

The presentation is generated programmatically using:

python-pptx
matplotlib

Possible analysis includes:

Sales summary
Revenue trends
Product performance
Category performance
Inventory observations
Low-stock products

The output is a real .pptx file rather than a text-only response.

🧠 Persistent Memory

KadaiPilot separates conversational state from persistent business state.

Persistent information includes:

Products
Customers
Draft Bills
Sales
Khata Entries
Owner Preferences
Chat Sessions
Chat Messages
Stock Movements

This information is stored in the database.

🔁 /new Session Reset

The /new command starts a fresh conversational session.

However, it does not erase persistent business information.

For example:

User:
I prefer UPI payments.

/new

User:
What payment method do I usually use?

Persistent preferences can still be retrieved from the database.

This demonstrates the distinction between:

Conversation State

and:

Business Memory
🛡️ Business Safety & Guardrails

Critical business operations are protected by deterministic application logic.

The language model does not have unrestricted access to the database.

🔒 Overselling Protection

A sale cannot reduce inventory below zero.

The database uses a conditional stock update conceptually equivalent to:

UPDATE products
SET quantity = quantity - ?
WHERE id = ?
AND quantity >= ?

If sufficient stock is unavailable, the operation fails instead of creating negative inventory.

💵 Below-Cost Sale Protection

The system prevents selling a product below its configured cost price.

This protects the store from accidental loss caused by an incorrect conversational request.

🧾 Draft Bill Protection

Draft bills do not permanently reduce inventory.

Stock is modified only during successful finalization.

🔁 Idempotent Finalization

Telegram updates can potentially be delivered more than once.

KadaiPilot uses a unique finalization key to prevent the same sale from being created multiple times.

This protects against duplicate transactions.

🗄️ Transactional Operations

Critical database operations are performed transactionally.

A finalized sale connects:

Sale
+
Sale Items
+
Payment
+
Stock Deduction

This reduces the risk of inconsistent business state.

🧩 Agent Architecture

KadaiPilot follows an agent-first architecture.

The system is not implemented as a collection of hardcoded message branches.

Instead of:

if "stock" in message:
    inventory()
elif "bill" in message:
    billing()

the agent interprets the request and decides which tools should be used.

🏗️ System Architecture
                    ┌───────────────────────┐
                    │       Telegram        │
                    │         User          │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Telegram Service     │
                    │ python-telegram-bot   │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │       AI Agent        │
                    │   OpenAI Agents SDK   │
                    │      + OpenRouter     │
                    └───────────┬───────────┘
                                │
              ┌─────────────────┼──────────────────┐
              │                 │                  │
              ▼                 ▼                  ▼
       ┌─────────────┐   ┌─────────────┐    ┌─────────────┐
       │ Inventory   │   │ Billing     │    │ Khata       │
       │ Tools       │   │ Tools       │    │ Tools       │
       └──────┬──────┘   └──────┬──────┘    └──────┬──────┘
              │                 │                  │
              └─────────────────┼──────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      SQLAlchemy       │
                    │      Data Layer       │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │        SQLite        │
                    │       Database       │
                    └───────────┬───────────┘
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
        ┌─────────────────┐          ┌─────────────────┐
        │ PDF Generator   │          │ PPTX Generator  │
        │    ReportLab    │          │ python-pptx     │
        └─────────────────┘          │ + Matplotlib    │
                                     └─────────────────┘
🔄 Agent Control Loop

The agent follows an observe → reason → act pattern.

User Request
     ↓
Understand Request
     ↓
Check Required Information
     ↓
Ask Clarification if Necessary
     ↓
Select Appropriate Tool
     ↓
Execute Business Operation
     ↓
Observe Tool Result
     ↓
Continue if Another Action is Required
     ↓
Return Final Response

This allows the system to handle multi-step natural-language workflows.

📁 Project Structure
KadaiPilot_Nebula_Supermarket_Agent/
│
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── artifacts.py
│   ├── db.py
│   ├── models.py
│   ├── services.py
│   ├── tax.py
│   └── telegram_service.py
│
├── tests/
│   ├── __init__.py
│   └── test_business.py
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── run_bot.py
└── seed.py
🧰 Technology Stack
Layer	Technology
Programming Language	Python
User Interface	Telegram
Telegram Framework	python-telegram-bot
Agent Framework	OpenAI Agents SDK
LLM Provider	OpenRouter
Database	SQLite
ORM	SQLAlchemy
Environment Management	python-dotenv
PDF Generation	ReportLab
PowerPoint Generation	python-pptx
Data Visualization	Matplotlib
Testing	pytest
⚙️ Installation
Requirements

Install:

Python 3.10+
Telegram account
Telegram Bot
OpenRouter API key
Git
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/KadaiPilot-Nebula-Supermarket-Agent.git

Enter the project directory:

cd KadaiPilot-Nebula-Supermarket-Agent
2. Create a Virtual Environment
Windows
python -m venv .venv

Activate:

.venv\Scripts\Activate.ps1
Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
🔐 Environment Configuration

Create a .env file in the project root.

Copy .env.example:

copy .env.example .env

Then edit .env.

Example:

TELEGRAM_BOT_TOKEN=your_telegram_bot_token

OPENAI_API_KEY=your_openrouter_api_key

OPENAI_BASE_URL=https://openrouter.ai/api/v1

AI_MODEL=openai/gpt-4o-mini

DATABASE_URL=sqlite:///./smartstore.db

SHOP_NAME=KadaiPilot Supermarket

SHOP_GSTIN=33ABCDE1234F1Z5

SHOP_STATE=Tamil Nadu

SHOP_CITY=Coimbatore
⚠️ Security

Never commit your real .env file.

Never publish:

API keys
Telegram bot tokens
Passwords
Private credentials

The repository should contain:

.env.example

but not:

.env

The .gitignore file is configured to prevent sensitive and generated files from being committed.

🗄️ Initialize the Database

Run:

python seed.py

Expected output:

Database seeded.

The seed script creates demonstration products and customers.

🧪 Run Automated Tests

Run:

python -m pytest -q

Current test result:

3 passed

The automated tests cover important business behavior including:

Multi-item billing
Overselling protection
Idempotent finalization
▶️ Start the Telegram Bot

Run:

python run_bot.py

Expected:

Bot is running...

Keep this terminal open while using the bot.

💬 Example Usage
Start the Bot
/start
Product Search
What products do you have?
Inventory
How much Maggi is left?
Receive Stock
50 packets of Maggi arrived.

If additional information is required, the agent can ask for it.

Create a Bill
Create a bill for:

2 kg sugar
1 Aashirvaad atta 5kg
4 packets Maggi
Edit the Bill
Remove the atta.

Then:

Change Maggi to 6 packets.
Preview
Show my bill.
Finalize
Finalize the bill and pay by UPI.
Khata
Put ₹500 on Ramesh's credit.

Then:

How much does Ramesh owe?

Then:

Ramesh paid ₹300.
Low Stock
Show low stock products.
Daily Sales
Show today's sales.
Weekly Analysis
Generate this week's sales analysis deck.
❓ Ambiguous Request Handling

KadaiPilot is designed to ask clarification questions when the user's request does not contain enough information.

Example:

User:
Give me some rice.

Instead of blindly choosing a product or quantity, the agent can ask:

How much rice do you need, and should I use loose rice or packaged rice?

This is important for supermarket operations because natural-language requests can contain incomplete information.

🧪 Example End-to-End Workflow

A complete customer transaction can look like this:

User:
I need 2 kg sugar and 3 packets of Maggi.

        ↓

Agent:
Identifies products and quantities.

        ↓

Agent:
Creates draft bill.

        ↓

User:
Show the bill.

        ↓

Agent:
Calculates subtotal and applicable GST.

        ↓

User:
Add one Tata Salt.

        ↓

Agent:
Updates draft bill.

        ↓

User:
Finalize and pay by UPI.

        ↓

Agent:
Validates stock.

        ↓

Agent:
Validates selling price.

        ↓

Agent:
Calculates final GST.

        ↓

Agent:
Atomically deducts inventory.

        ↓

Agent:
Creates sale record.

        ↓

Agent:
Generates PDF invoice.

        ↓

Telegram:
Sends invoice to user.
🧱 Database Model

The application uses SQLAlchemy models backed by SQLite.

Important entities include:

Product
Customer
DraftBill
DraftLine
Sale
SaleLine
KhataEntry
OwnerPreference
ChatSession
ChatMessage
StockMove
📦 Product Data Model

A product stores important supermarket information such as:

Product
├── Name
├── SKU
├── HSN
├── GST Rate
├── Unit
├── Loose / Packaged
├── Cost Price
├── Selling Price
├── MRP
├── Quantity
└── Reorder Level

This allows the AI agent to ground its responses in actual store data.

💾 Persistence

SQLite provides persistent storage for the local deployment.

The database stores:

Inventory
Sales
Customers
Khata
Bills
Preferences
Chat History
Stock Movements

Restarting the Telegram bot does not erase the store database.

🧠 Memory Design

KadaiPilot has two types of state:

Session State

Temporary conversational context.

Persistent Business State

Long-lived operational information stored in SQLite.

This separation allows:

/new

to reset the conversational session while retaining business information.

🧪 Testing Strategy

The project includes automated business tests.

Current tests validate:

Test 1 — Multi-Item Billing

Ensures multiple products can be added to a bill and finalized correctly.

Test 2 — Oversell Protection

Ensures a sale cannot reduce inventory below zero.

Test 3 — Idempotent Finalization

Ensures duplicate finalization requests do not create duplicate sales.

Current result:

3 passed
📊 Business Rule Layer

Business rules are implemented in the application layer rather than relying entirely on the LLM.

This provides a separation between:

AI Reasoning

and:

Business Execution

The AI determines what should happen.

The business tools determine whether it is allowed to happen.

🔒 Security Considerations

The project follows several security practices:

API credentials are stored in environment variables.
.env is excluded from Git.
Database writes are performed through application tools.
Inventory updates are protected by database conditions.
Duplicate finalization is prevented.
Below-cost sales are rejected.
Invalid khata operations are rejected.
📈 Future Improvements

Potential extensions include:

🎤 Voice Orders

Allow customers to send Telegram voice notes.

🇮🇳 Indian Language Support

Support:

Tamil
Hindi
Malayalam
Telugu
Kannada
📷 Product Image Recognition

Identify products from photographs.

📦 Barcode Scanning

Scan product barcodes through Telegram.

⏳ Batch & Expiry Tracking

Support:

Batch numbers
Expiry dates
FEFO inventory
Expiry alerts
📈 Sales Forecasting

Use historical sales velocity to recommend reorder quantities.

🔔 Reorder Suggestions

Automatically recommend products that should be restocked.

💳 Khata Reminders

Generate reminders for customers with outstanding balances.

☁️ Production Database

Move from SQLite to PostgreSQL for larger deployments.

🎥 Recommended Demo Flow

For a project demonstration, the following sequence shows the major capabilities:

1. /start

2. Ask for available products

3. Check inventory

4. Receive stock

5. Create a multi-item bill

6. Edit the bill

7. Preview GST

8. Finalize using UPI

9. Receive PDF invoice

10. Add customer credit

11. Record customer payment

12. Check khata balance

13. Show low-stock products

14. Generate weekly PPTX analysis

15. Save an owner preference

16. Run /new

17. Demonstrate persistent memory
🎯 Nebula Assignment Coverage
Requirement	Implementation
Telegram interface	✅
Agent-first architecture	✅
Natural-language operations	✅
Product management	✅
Receive stock	✅
Inventory queries	✅
Low-stock detection	✅
Multi-item billing	✅
Bill editing	✅
GST calculation	✅
HSN per SKU	✅
CGST / SGST	✅
Cash payment	✅
UPI payment	✅
Card payment	✅
Khata credit	✅
Khata payment	✅
Customer balance	✅
Daily sales	✅
PDF invoice	✅
Weekly PPTX analysis	✅
Persistent memory	✅
Draft bill persistence	✅
Oversell protection	✅
Below-cost protection	✅
Idempotent finalization	✅
SQLite persistence	✅
Automated tests	✅
🏆 Design Highlights

KadaiPilot focuses on the difficult parts of supermarket automation rather than only implementing a chatbot interface.

Agent Orchestration

The AI decides which tools to call based on the user's request.

Grounded Business Data

Inventory, prices, taxes, sales, and customer balances come from persistent application state.

Deterministic Business Rules

Financial and inventory safeguards are enforced by code.

Conversational Workflows

Users can create and modify bills over multiple messages.

Persistent Memory

Business information survives new conversations and bot restarts.

Real Artifacts

The system generates actual PDF invoices and PowerPoint analysis files.

📌 Project Status

Current implementation:

Telegram Bot             ✅
AI Agent                 ✅
Inventory                ✅
Billing                  ✅
GST                      ✅
Khata                    ✅
SQLite Persistence       ✅
PDF Invoice              ✅
PPTX Analysis            ✅
Persistent Preferences   ✅
Business Tests           ✅

Automated tests:

3 passed
👨‍💻 Project Information

Project Name: KadaiPilot AI

Challenge: Nebula Supermarket Ops Agent

Platform: Telegram

Language: Python

Database: SQLite

Architecture: Agent-first

AI Framework: OpenAI Agents SDK

LLM Provider: OpenRouter

📜 License

This project was developed for the Nebula Supermarket Ops Agent hiring assignment.

⭐ Summary

KadaiPilot AI transforms Telegram into a conversational operating interface for an Indian supermarket.

The system combines:

Telegram
   +
AI Agent
   +
Business Tools
   +
Persistent Database
   +
GST-aware Billing
   +
Inventory Controls
   +
Khata
   +
PDF Invoices
   +
PPTX Analytics

The core principle is:

The AI reasons. The tools enforce the business rules.


### One correction before you upload

Your actual project currently has an `artifacts` directory as shown in your screenshot. If that directory contains generated PDFs/PPTX files, **don't upload those generated files** unless you specifically want sample artifacts in the repository.

Your GitHub root should look approximately like:

```text
📁 app
📁 tests
📄 .env.example
📄 .gitignore
📄 README.md
📄 requirements.txt
📄 run_bot.py
📄 seed.py

And not:

❌ .env
❌ .venv
❌ smartstore.db
❌ API keys
❌ Telegram token
