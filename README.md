# SQL Practice Questions Platform

A comprehensive platform for practicing SQL queries with automated validation, user progress tracking, and AI-powered assistance.

## 🚀 Overview

This platform helps users learn and practice SQL at multiple difficulty levels with intelligent feedback, hints, and explanations powered by local Llama AI models.

## ✨ Features

### Current Features
- ✅ Automated SQL query validation
- ✅ User progress tracking
- ✅ Flexible question configuration
- ✅ Logging and error tracking
- ✅ YAML-based configuration

### Roadmap Features
- 🔄 **Multi-Level Difficulty System** (Beginner → Expert)
- 🔄 **Local Llama AI Integration** for intelligent hints
- 🔄 **RESTful API** for platform integration
- 🔄 **Expanded Question Library** (40+ questions)
- 🔄 **Advanced SQL Topics** (Window Functions, CTEs, Recursive Queries)

## 📋 Quick Start

### Prerequisites
- Python 3.10+
- SQLite (included with Python)
- (Optional) Docker for containerized usage
- (Optional) Ollama for AI features

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/Practic_Questions_Platform.git
cd Practic_Questions_Platform

# Install dependencies
pip install -r requirements.txt

# Generate test data
python -m infra.DataGenerator

# Solve a question
python SQl_answer.py sql_basic_select
```

## 🐳 Docker Usage

The platform can be run in Docker containers for easy setup and consistent environments.

### Quick Start with Docker

```bash
# Build and run the platform
docker compose up --build

# Or run with Docker directly
docker build -t sql-practice-platform .
docker run --rm sql-practice-platform
```

### Docker Commands

```bash
# Generate test data only
docker compose run --rm data-generator

# Run interactively (for development)
docker compose run --rm interactive

# Run with persistent data
docker compose up -d

# View logs
docker compose logs -f

# Clean up
docker compose down -v
```

### Volume Mounts

The Docker setup supports persistent data through volume mounts:
- `./output` - Generated databases and CSV files
- `./users` - User progress tracking
- `./logs` - Application logs
- `./Questions` - Custom practice questions

## 📁 Project Structure

```
Practic_Questions_Platform/
│
├── Questions/                    # SQL practice questions
│   └── sql_basic_select/        # Question folder
│       ├── question             # Problem description
│       ├── example_solution.sql # Reference solution
│       └── Sloutions/           # Note: typo to be fixed (see TASK-011)
│           └── sloution_df.csv  # Expected output
│
├── infra/                        # Core infrastructure
│   ├── AnswerValidator.py       # SQL validation logic
│   ├── DataGenerator.py         # Test data generation
│   ├── user.py                  # User management
│   ├── logging_config.py        # Logging setup
│   └── config/
│       ├── config.yml           # Data generation config
│       └── questions_config.yml # Questions config
│
├── docs/                         # Documentation
│   ├── CODING_STANDARDS.md      # Coding guidelines
│   ├── AI_INTEGRATION.md        # AI setup guide
│   └── DIFFICULTY_LEVELS.md     # Level specifications
│
├── .github/
│   └── ISSUE_TEMPLATE/          # Issue templates for AI agents
│
├── output/                       # Generated data
├── logs/                         # Application logs
├── users/                        # User progress files
│
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Docker services orchestration
├── .dockerignore                # Docker build exclusions
├── PRODUCT_ROADMAP.md           # Development roadmap
├── requirements.txt             # Python dependencies
├── SQl_answer.py               # Main entry point
└── README.md                    # This file
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [PRODUCT_ROADMAP.md](PRODUCT_ROADMAP.md) | Complete development roadmap with AI agent tasks |
| [docs/CODING_STANDARDS.md](docs/CODING_STANDARDS.md) | Coding standards and quality guidelines |
| [docs/AI_INTEGRATION.md](docs/AI_INTEGRATION.md) | Local Llama AI integration guide |
| [docs/DIFFICULTY_LEVELS.md](docs/DIFFICULTY_LEVELS.md) | SQL difficulty level specifications |

## 🎯 Difficulty Levels

| Level | Topics | Time Limit | Hints |
|-------|--------|------------|-------|
| **BEGINNER** | SELECT, WHERE, ORDER BY, LIMIT | 5 min | 5 |
| **INTERMEDIATE** | JOINs, GROUP BY, Aggregations, Subqueries | 10 min | 3 |
| **ADVANCED** | Window Functions, CTEs | 15 min | 2 |
| **EXPERT** | Recursive CTEs, Query Optimization | 20 min | 1 |

## 🤖 AI Integration

The platform supports local Llama AI for:
- **Progressive Hints**: Context-aware hints that adapt to difficulty
- **Query Explanations**: Natural language explanations of SQL
- **Error Analysis**: AI-powered debugging assistance

### Quick AI Setup (Ollama)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull recommended model
ollama pull llama3.2:3b

# Verify installation
curl http://localhost:11434/api/tags
```

See [docs/AI_INTEGRATION.md](docs/AI_INTEGRATION.md) for complete setup guide.

## 🛠️ Development

### For Contributors

1. Review [PRODUCT_ROADMAP.md](PRODUCT_ROADMAP.md) for available tasks
2. Follow [docs/CODING_STANDARDS.md](docs/CODING_STANDARDS.md)
3. Use provided issue templates for task tracking

### For AI Agents

This repository includes structured task delegation for AI agents:

1. **Task Definitions**: See `PRODUCT_ROADMAP.md` for detailed task specifications
2. **Issue Templates**: Use `.github/ISSUE_TEMPLATE/` templates for creating tasks
3. **Coding Standards**: Follow guidelines in `docs/CODING_STANDARDS.md`
4. **Quality Requirements**: 80%+ test coverage, type hints, docstrings

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest tests/ -v --cov=infra

# Lint code
flake8 infra/

# Type check
mypy infra/
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests following the coding standards.

---

*For detailed development tasks and AI agent instructions, see [PRODUCT_ROADMAP.md](PRODUCT_ROADMAP.md)*
