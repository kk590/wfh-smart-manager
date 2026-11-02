# WFH Manager: Multi-Agent Conversational Database Interface

A secure, multi-agent natural language interface for managing and querying employee and team databases (designed for tracking Work From Home allocations, team roles, and relations). It converts conversational text into validated, sandbox-tested SQLModel ORM code.

---

## 1. Problem Statement

Organizations need structured databases to track teams, reporting structures, and employee status. However, non-technical managers face major friction when interacting with these systems:

1. **The Interface Barrier:** Users do not know SQL or Python ORM syntax.
2. **The Schema Rigidity Barrier:** Traditional databases have strict schemas. If a manager needs to track custom, ad-hoc attributes (e.g. `"age"`, `"remote days"`, or `"secret name"`), they must ask developers to write migrations.
3. **The Safety Barrier:** Dynamically executing LLM-generated code against a database is highly risky. Dangerous imports (`os`, `sys`, `subprocess`) or destructive commands (`DROP TABLE`, `TRUNCATE`) could compromise the system.
4. **The Hallucination Barrier:** LLMs often hallucinate database query success, return hardcoded IDs, or generate code referencing non-existent tables/fields.
5. **The Access Control Barrier:** Modifying operations (creating users, changing departments, deleting records) must be gated by role permissions, preventing non-admin users from corrupting database state.
6. **The Dynamic CRUD Barrier:** The system must not only support static queries but also orchestrate full CRUD operations (Create, Read, Update, Delete) dynamically across newly created tables and custom attributes without breaking database integrity.

---

## 2. Solution & System Architecture

This project solves these issues by placing a security-hardened, multi-agent pipeline between the natural language interface and the physical database.

### System Workflow Description
When a user submits a natural language query, it flows sequentially through the following stages:

1. **Intent Parsing & Context Resolution:** The incoming conversational query is first received by the Intent Parser. This agent references the recent chat history to resolve context (such as pronouns or references to previous actions) and converts the vague conversational query into a structured database intent.
2. **Access Control Verification:** The structured intent is immediately sent to the Permission Checker. The system checks if the requested action attempts to modify data and verifies the user has the required role permissions.
3. **Code Generation:** A specialized Code Generator agent produces SQLModel ORM Python code that implements the requested database operation.
4. **Sandbox Validation:** The generated code is executed inside a restricted Python sandbox that blocks dangerous imports and validates the SQL operations before they touch the real database.
5. **Execution & Response:** Validated code runs against the database; results are streamed back to the frontend as NDJSON for live progress display.

---

## 3. Dynamic Schema Extension

The system supports ad-hoc attributes by automatically creating extension tables (e.g., `UserExtra` or `TeamExtra`) containing a foreign key pointing to the base table. It then invokes `create_all(engine)` to deploy the table on-the-fly.

* **Create Operations:** Standard attributes are inserted into the base tables (`User`/`Team`), while any custom attributes are simultaneously inserted into the corresponding extension tables, linking them via foreign key relations.
* **Read Operations:** The generated code queries records from the base tables and performs a SQL join (or references relationships) to fetch custom attributes from the extension tables, merging them back into a single consolidated result.
* **Update Operations:** Updates targeting standard attributes modify the base tables directly. Updates targeting dynamic attributes look up the associated record in the extension tables, updating them or creating a new extension record if it doesn't already exist.
* **Delete Operations:** When a user or team is deleted, the ORM code ensures that any related rows in the custom extension tables are cascade-deleted to prevent orphaned data records.

---

## 4. Technology Stack

* **Backend Engine:**
  * Python 3.10+
  * **FastAPI:** Server APIs & server-sent stream endpoint (`/chat`).
  * **SQLModel:** SQL database management combining SQLAlchemy and Pydantic.
  * **SQLite:** Relational database storage.
* **Frontend Dashboard:**
  * **Angular (v17+):** Single-page chat dashboard.
  * **Event Streams:** Reads NDJSON chunks in real-time, displaying live execution logs of the agent validation process.
* **Inference Tier:**
  * GitHub Models API. Uses a distributed routing strategy to balance rate limits (GPT-4o Mini, Codestral-2501, Phi-4).

---

## 5. How to Run the Application

### Backend Setup
1. Ensure you have Python 3.10+ installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your GitHub Token in a `.env` file in the root directory:
   ```env
   GITHUB_TOKEN=your_github_personal_access_token_here
   ```
4. Start the FastAPI backend server:
   ```bash
   python src/main.py
   ```
   The backend will start on `http://127.0.0.1:8000`.

### Frontend Setup
1. Navigate to the `frontend/` directory.
2. Install npm packages:
   ```bash
   npm install
   ```
3. Start the Angular development server:
   ```bash
   npm start
   ```
   The frontend will be accessible at `http://localhost:4200`.

### Running Tests
To verify the multi-agent pipeline and the CRUD functions:
```bash
python test_crud_pipeline.py
```
