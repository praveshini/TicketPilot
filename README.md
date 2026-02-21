# TicketPilot - IT Support Ticketing Engine

A FastAPI-based ticketing engine for IT support.


## Project Structure

```

├── app/
│   ├── main.py           # FastAPI application entry point
│   ├── api/
│   │   └── routes.py    # API route definitions
│   ├── core/
│   │   └── classifier.py # Ticket classification
│   ├── data/
│   │   └── queue.py     # Ticket  management
│   └── model/
│       └── model.py     # Data model
├── setup/
│   ├── setup.sh         # Setup script for Linux/Mac
│   └── setup.bat        # Setup script for Windows
├── simulator.py         
├── requirements.txt     # Python dependencies
└── README.md           
```


## Setup Instructions

### Option 1: Using Setup Scripts (Recommended)

#### Windows
```
cmd
cd setup
setup.bat
```

#### Linux/Mac
```bash
cd setup
bash setup.sh
# or
./setup.sh
```

### Option 2: Manual Setup

### 1. Fork  the Repository
### 2. Create Virtual Environment

#### Windows
```
cmd
python3 -m venv venv
```

#### Linux/Mac
```
bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

#### Windows
```
cmd
venv\Scripts\activate
```

#### Linux/Mac
```
bash
source venv/bin/activate
```

### 4. Install Dependencies

#### Standard Installation
```
bash
pip install -r requirements.txt
```


## 5. Running the Application

### Start the FastAPI Server

After setup, activate the virtual environment and run:

#### Windows
```
cmd
venv\Scripts\activate
python3 -m app.main
```

#### Linux/Mac
```
bash
source venv/bin/activate
python3 -m app.main
```
### Standard
```
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`


## Troubleshooting

### Port Already in Use
If port 8000 is busy, modify the port in `app/main.py`:
```
python
uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
```

### Virtual Environment Issues

#### Windows: Activation fails
- Ensure you're running Command Prompt or PowerShell
- Check that the `venv` folder was created properly


### Python 3.12+ Installation Issues

If you encounter errors like `Unsupported platform: 312` or `Rust not found`, it's because pip tried to compile packages from source. Use the following command instead:

```
bash
pip install --only-binary=:all: fastapi uvicorn pydantic requests
```

This ensures pip downloads prebuilt binary wheels and avoids requiring Rust compiler.

### Import Errors
If you encounter import errors, ensure:
1. Virtual environment is activated
2. All dependencies are installed (`pip list`)

---

## Contributors


### Setting Up Development Environment
1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Follow the "Setup Instructions" section above


### Submitting Changes
1. Commit your changes: `git commit -m "Add your message"`
2. Push to your fork: `git push origin feature/your-feature-name`
3. Create a Pull Request

(Update requirements.txt as required)



---

