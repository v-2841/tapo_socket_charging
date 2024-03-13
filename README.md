# Charging Control Readme
This repository contains code for controlling a Tapo socket based on battery percentage of the host system. It ensures the socket is turned on when the battery falls below a certain threshold and turned off when the battery reaches a certain level while charging.

## Setup
1. Clone the repository and navigate to it in the command line:
```bash
git clone git@github.com:v-2841/tapo_socket_charging.git
cd tapo_socket_charging
```
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate
```
3. Install dependencies from the requirements.txt file:
```bash
pip install -r requirements.txt
```

## Usage
The `charging.py` script monitors the battery percentage of the host system and controls the Tapo socket accordingly.
To use the script, run the following command in virtual environment:
```bash
python charging.py
```

### Command Line Arguments
-   `--add-to-taskschd`: Adds the script to Windows Task Scheduler to run at user logon.
-   `--remove-from-taskschd`: Removes the script from Windows Task Scheduler.

## Code Structure
The code consists of two main Python scripts:
1.  `charging.py`: This script monitors the battery percentage and controls the Tapo socket accordingly.
2.  `taskschd.py`: This script contains functions to add and remove the main script from Windows Task Scheduler.

## License
This project is licensed under the MIT License - see the LICENSE file for details.