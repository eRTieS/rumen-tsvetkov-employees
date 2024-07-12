# Sirma Interview Task

## Task
### Pair of employees who have worked together

The program have to take a csv file as a input data.

CSV example:
    
    ```
    
    EmpID, ProjectID, DateFrom, DateTo
    
    143, 12, 2013-11-01, 2014-01-05
    
    218, 10, 2012-05-16, NULL
    
    143, 10, 2009-01-01, 2011-04-27
    
    ```

### Supported date formats
Date separator is not required and can be different characters.
Example date: 10 July 2024

10-07-2024, 10-Jul-2024, 10-July-2024, 07-10-2024, Jul-10-2024, July-10-2024, 2024-07-10, 2024-Jul-10, 2024-July-10

## Installation

1. Clone the repo
2. Tested with python version >= 3.11
3. Install dependencies
    * by poetry
        > poetry install
    * by pip
        > python -m venv sirma
        > 
        > source sirma/bin/activate
        > 
        > pip install requirements.txt

## Start the project

* Go to employee directory `cd employee`

### By CLI
1. Run the `employees.py`
    * add csv file as argument `python employees.py <path to csv>`
    * if no argument added, the program will ask you to type a path to the file

### BY web UI
1. Run `flask run`
2. Open `http://127.0.0.1:5000` in your web browser
