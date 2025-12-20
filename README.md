# skeleton

Minimal Python project setup using a local virtual environment (`venv`) and `requirements.txt`.

## Requirements
- Python 3.x installed (recommended: both teammates use the same Python major/minor, e.g. 3.14.x)
- Internet access to install packages via `pip`

## Quick start (Windows)
From the project root:

### 1 Create a virtual environment
```powershell
py -m venv .venv

### 2 Activate it
powershell
Copy code
.\.venv\Scripts\Activate.ps1
If PowerShell blocks activation with “running scripts is disabled”, run (for your user only):

powershell
Copy code
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
Then try activation again.

### 3 Install dependencies
powershell
Copy code
python -m pip install --upgrade pip
pip install -r requirements.txt