# How to Use RustPlus-Chat-Bot

This guide will walk you through the steps to set up and run the RustPlus-Chat-Bot. Follow these steps based on whether you are using PowerShell or Command Prompt (cmd) on your computer.

### Step 1: Verify Python Installation

Before proceeding, ensure Python is installed on your computer. You can check this by running the following command in either PowerShell or cmd:

```
python --version
```

If Python is not installed, download it from the [official Python website](https://www.python.org/downloads/).

### Step 2: Download and Unzip the Project

1. Download the RustPlus-Chat-Bot project as a ZIP file.
2. Unzip (extract) the file onto your **Desktop**.

### PowerShell Setup and Run

If you are using PowerShell, follow these steps:

#### For the First-Time Setup:

1. Open PowerShell.
2. Run the following command to set up the virtual environment, activate it, and install the required package:

   ```powershell
   cd .\Desktop\RustPlus-Chat-Bot\
   py -m venv venv
   .\venv\Scripts\activate
   pip install rustplus
   cd .\manage\
   ```

3. To start the bot, run:

   ```powershell
   py main.py
   ```

#### For Running Regularly:

1. Open PowerShell.
2. Run the following commands to activate the virtual environment and navigate to the manage folder:

   ```powershell
   cd .\Desktop\RustPlus-Chat-Bot\
   .\venv\Scripts\activate
   cd .\manage\
   ```

3. Start the bot:

   ```powershell
   py main.py
   ```

#### (Optional) To Run the Bot Once Per Day:

If you plan to run the bot just once per day, use the following single-line command:

```powershell
cd .\Desktop\RustPlus-Chat-Bot\ ; .\venv\Scripts\activate ; cd .\manage\ ; py main.py
```

---

### Command Prompt (cmd) Setup and Run

If you are using Command Prompt, follow these steps:

1. Open Command Prompt (cmd).
2. Run the following commands to set up the virtual environment, activate it, and install the required package:

   ```cmd
   cd Desktop/RustPlus-Chat-Bot
   py -m venv venv
   .\venv\Scripts\activate
   pip install rustplus
   cd manage
   ```

3. To run the bot for the first time and keep it running, add:

   ```cmd
   py main.py
   ```

   *If you don't plan to restart the bot regularly, simply add the last command after the setup.*

---

Now your RustPlus-Chat-Bot should be up and running!
