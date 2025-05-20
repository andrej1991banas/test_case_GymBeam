# Golemio Library Data Extractor
## Overview
This repository contains a **Python script** designed to extract data about city libraries from the **Golemio API**, as part of the **GymBeam Data Engineer Case Study 2025** (Task 2: Data Integration). The extractor retrieves 10 specified parameters about libraries and is configured to run daily at 7:00 AM Prague time (CEST). 

## Extracted Parameters
The script extracts the following parameters from the Golemio API:

- Library ID
- Library Name
- Street
- Postal Code (PSČ)
- City
- Region (Kraj)
- Country
- Latitude
- Longitude
- Opening Hours

# Repository Structure
```plain
Case_Study_Banas/GymBeam
│
├── config.json                        #configuration file for extractor_libraries
├── config_library_id.json              #configuration file for extractor_library_by_id
├── main.py                              #main script to run extractors
├── extractor_libraries.py              #  Python script for data extraction for number of libraries
├── extractor_library_by_id.py           # Main Python script for data extraction for library by ID
├── requirements.txt                     # Python dependencies
├── library_by_id.json                   # file of extracted data with extractor_library_by_id.py
├── libraries.json                       # file of extracted data with extractor_libraries.py
└── README.md                            # This file
```
# Prerequisites
To run the script, you need:

Python 3.8 or higher
Access to the Golemio API (requires an API key from Golemio)
Git installed for cloning the repository
A scheduling tool (e.g., cron on Linux, Task Scheduler on Windows, or a cloud service like AWS Lambda)

# Installation

Clone the Repository:
```plain
git clone https://github.com/andrej1991banas/test_case_GymBeam.git
```

Redirect to the directory of the cloned repository
```plain
cd your_folder_directory
```

Install Dependencies:Install required Python packages listed in requirements.txt:
```plain
pip install -r requirements.txt
```

# Usage

Run the Extractor:Execute the Python script to extract library data:
```plain
python main.py
```
The script will:

Connect to the Golemio API
Retrieve library data
Save the output as a JSON file in the / directory (e.g., /library_by_id.json)


Output Format:The output JSON file contains the following columns:
"id",
"name",
"street_address",
"postal_code",
"address_locality",
"district",
"address_country",
"latitude",
"longitude",
"opening_time"


# Scheduling Daily Updates:

**The extractor is designed to run daily at 7:00 AM Prague time (CEST). You can schedule it using:**


## Windows Task Scheduler:
Create a task to run python main.py daily at 7:00 AM.
Ensure the Python environment is properly configured.

**Open Task Scheduler**
Press Win + S and type "Task Scheduler". Click on Task Scheduler to open it.
In Task Scheduler, click Create Basic Task from the right-hand "Actions" panel.

**Create a New Task**
**Provide a name and description:**
- Give your task a name (e.g., "Run Python Script").
- Provide a brief description if necessary.


**Choose when to start the task:**
- Select the frequency of the task (e.g., Daily, Weekly, One Time).


**Set the start date and time:**
- Specify when you'd like the task to begin.
- In our case it will be **7am CEST**

**Choose the action:**
- select **Start a program**

**Set the program/script**
- for Program/script, input the path to the Python axecuable.
  ```plain
  C:\Users\YourUsername\AppData\Local\Programs\Python\Python39\python.exe
  ```
**Add arguments**
- in the **Add arguments (optional)** field, provide the path to your script
  ```plain
  C:\PythonScripts\example_script.py
  ```
**Start in (optional):**
- Use the folder directory containing the script
 ```plain
 C:\PythonScripts
```

**Finalize and Save**
- Review all the confiurations in the summary window
- Clisk **Finish** to create the task





Data Flow
The following diagram illustrates the data extraction process:

The script sends a request to the Golemio API.
The API returns JSON data about libraries.
The script processes the data, extracting the 10 required parameters.
The processed data is saved as a JSON file in the **"root" directory.**



Evaluation
This repository is part of the GymBeam Data Engineer Case Study 2025. Reviewers fro this project:
**jakub.uhrina@gymbeam.com**
**ladislav.safarik@gymbeam.com**

License
This project is licensed under the MIT License. See the LICENSE file for details.
**Owner: Andrej Banas**

