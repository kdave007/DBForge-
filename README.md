# DBForge - DBF to PostgreSQL Converter

A Python-based tool to convert DBF files to PostgreSQL tables using MVC architecture.

## 🏗️ Project Structure
```
dbf_to_postgres/
│── config.ini          # Configuration file
│── data/              # Directory for DBF files
│── scripts/           # Generated SQL scripts
│── models/            # Data models
│   ├── dbf_model.py
│   ├── postgres_model.py
│── controllers/       # Business logic
│   ├── dbf_controller.py
│── views/             # User interface
│   ├── cli_view.py
│── utils.py           # Helper functions
│── main.py           # Application entry point
│── requirements.txt   # Project dependencies
│── build_executable.bat # Compilation script
```

## 🚀 Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the application:
   - Edit `config.ini` with your PostgreSQL credentials
   - Place your DBF files in the `data/` directory

3. Run the application:
   ```bash
   python main.py
   ```

## 📦 Building Executable
Run `build_executable.bat` to create a standalone executable.

## 🛠️ Dependencies
- dbfread: Reading DBF files
- psycopg2-binary: PostgreSQL interaction
- configparser: Configuration management
- argparse: CLI argument parsing