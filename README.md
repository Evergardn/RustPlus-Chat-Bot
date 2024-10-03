# RustPlus-Chat-Bot
This bot is designed to interact with Rust game servers, providing various functions through chat commands. It automatically connects to the server and monitors important events, and can also perform a number of useful operations for players. The bot uses the RUST+ library and interacts with the game's command system.

# Tutorial how to use (free-version)

# Step 1: Download and extract files
  1. Download the archive with the program to your computer.
  2. Unzip the archive to your desktop. This can be done using built-in Windows tools or third-party archivers such as WinRAR or 7-Zip.
  3. Make sure that the folder with the program is on the desktop and is called, for example, `RustPlus-Chat-Bot`.

# Step 2: Opening a Command Prompt
  1. Press the key combination `Win + R` to open the Run window.
  2. Type `cmd` and press `Enter` to open the command line **or**:
   - Right-click on the Start menu and select **Windows PowerShell** (or **Command Prompt**).
   
# Step 3: Move to the program directory
  1. In the command line that opens, enter the following command to go to the program folder:
     ```bash
     cd Desktop/RustPlus-Chat-Bot
     ```
     This command will take you to the folder on your desktop where the program files are located.

# Step 4: Creating a virtual environment Python
  1. At the command prompt, run the following command to create the virtual environment:
     ```bash
     py -m venv venv
     ```
     This will create an isolated virtual Python environment so that all of the program's dependencies are installed locally and do not conflict with other projects.
     
# Step 5: Activate venv (virtual enviroment)
  1. Activate the virtual environment (if you are using Windows):
     ```bash
     .\venv\Scripts\activate
     ```
     If you are using PowerShell, first run the following command to enable script execution:
     ```bash
     Set-ExecutionPolicy RemoteSigned
     ```
     Then activate the virtual environment again:
     ```bash
     .\venv\Scripts\activate
     ```

  2. Download obligatory libraries:
     ```bash
     pip install rustplus python-dotenv
      ```

# Step 6: Run the program
  1. Go to the `manage` directory where the launch file is located:
     ```bash
     cd manage
     ```
  2. Run the command to start the program:
     ```bash
     py main.py
     ```

 Completion
After completing these steps, the program should start working. If everything went well, you will see corresponding messages on the command line. 

 Adviсe:
- If something doesn't work, make sure you have activated the virtual environment and entered the commands correctly.
- If errors occur, check that the files are unpacked correctly and the dependencies are installed.
- Check that u download python on the page: [python.org](https://www.python.org/)
