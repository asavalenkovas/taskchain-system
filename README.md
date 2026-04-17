# TaskChain System

TaskChain System is a production task management application built with Django.

The main idea of the project is to manage task flow across multiple workstations and additionally record important task events using a blockchain-inspired audit trail. The system is designed for manufacturing environments where tasks move through different stages such as CNC, welding, painting, and quality control.

## Main idea

The system allows users to:

- create production task chains across multiple workstations
- manage task execution flow
- restrict access based on user roles
- store important events as linked blocks
- verify whether the block chain history has been modified

## Core features

### 1. Task management
- tasks are created under a specific project
- tasks are assigned to specific machines or workstations
- one part can have multiple production stages

### 2. Task sequence and dependencies
- tasks are linked through `depends_on`
- the next task becomes available only when the previous one is completed
- this helps enforce the correct production flow

### 3. User roles
The system supports different user roles:

- **manager** – can view the dashboard and create tasks
- **operator** – can only view tasks assigned to their own workstation
- **superuser** – full system access

### 4. Blockchain-inspired audit trail
Each important event in the system is saved as a block, for example:

- `TASK_CREATED`
- `TASK_STATUS_CHANGED`
- `TASK_PRIORITY_CHANGED`
- `TASK_MACHINE_CHANGED`
- `TASK_REORDERED`

Each block contains:
- its own `hash`
- previous block `prev_hash`

This makes it possible to detect history tampering and maintain data integrity.

### 5. Chain verification
The system includes a `verify_chain` function that:

- recalculates each block hash
- checks whether hashes match
- checks whether the chain is continuous

## Example production workflow

System configuration (machines and projects) is managed through the Django admin panel.

- Machines are created and maintained by the administrator
- Projects are also created in the admin panel

Machines represent abstract workstations and are not limited to specific types.  
They can reflect any real production environment.

A single task can move through multiple stages defined by the manager.

Each stage is represented as a separate task assigned to a machine.

Tasks are created by a manager and linked together into a sequence.  
Tasks can depend on one another, which means later stages cannot start before earlier stages are completed.

## Technologies used

- Python
- Django
- SQLite
- HTML
- CSS

## Project structure

- `tasks` – task logic, machines, dashboard, production workflow
- `ledger` – blocks, hash calculation, chain verification
- `accounts` – user profiles and roles
- `config` – project settings and URL configuration

## Why this project is different

This is not just a simple CRUD task application.

The system combines:

- role-based production task management
- workstation-specific task queues
- dependency-based workflow
- blockchain-inspired event logging
- linked hash verification for auditability

This makes the project closer to a lightweight MES-style production management system.

## How to run the project

# 1. Clone repository
git clone https://github.com/asavalenkovas/taskchain-system.git
cd taskchain-system

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Apply migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver

# 8. Open in browser
http://127.0.0.1:8000/