# Python Generators — Seed Database

##  Project Objective
This project demonstrates how to use **Python with MySQL** to create and populate a database. 
The goal is to write a script (`seed.py`) that:
1. Connects to the MySQL server.
2. Creates a database named **`ALX_prodev`** if it does not exist.
3. Creates a table named **`user_data`**.
4. Loads and inserts data from a CSV file (`user_data.csv`).
5. Prepares the environment for a generator that will later stream data row by row.

---

##  Project Structure
python-generators-0x00/
│
├── 0-main.py # Provided test script
├── seed.py # Your implementation
├── user_data.csv # CSV file with sample user data
└── README.md # Project documentation



---

##  Requirements
- Python 3.8+
- MySQL server installed and running
- MySQL Connector for Python 
  Install with:
  ```bash
  pip install mysql-connector-python
  
##  How to Run
Make sure MySQL is running and accessible.
Update your username and password inside seed.py if necessary.
Run the script: ./0-main.py

Expected output example:
  connection successful
Table user_data created successfully
Data inserted successfully
Database ALX_prodev is present
[('550e8400-e29b-41d4-a716-446655440000', 'João Silva', 'joao.silva@example.com', Decimal('25.0')), ...]


