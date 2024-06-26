#### Project Description

Online payment services, such as PayPal, allow users to connect their online accounts to their bank accounts, debit and credit cards. In such systems, users can usually transfer money from their bank accounts to the online account, receive payments to this account from other users, push money from the online account to their bank accounts, among others.
For simplicity, we will assume in this project that all registered users start with a specific amount of money (e.g., £1000) and no connections to bank accounts exist.
Note: This is pretended money, and no connection to real sources of money should exist.

To register, a user must provide a username, a first and last name, an email address and a password. Each user has a single online account whose currency is selected upon registration. Users can choose to have their account in GB Pounds, US dollars or Euros. In any case, the system should make the appropriate conversion to assign the right initial amount of money (e.g., if the baseline is £1000, then the initial amount should be 1000 \* GBP_to_USD_rate US dollars).
A user can instruct the system to make a direct payment to another user. If this request is accepted (i.e., the recipient of the payment exists and there are enough funds), money is transferred (within a

single Django transaction) to the recipient immediately. Users should be able to check for notifications regarding payments in their accounts.
A user can instruct the system to request payment from some other user. A user should be able to check about such notifications for payment requests. They can reject the request or, in response to it, make a payment to the requesting user.
Users can access all their transactions, that is, sent and received payments and requests for payments as well as their current account balance.
An administrator can see all user accounts and all transactions.
A separate RESTful web service must implement currency conversion. The exchange rates will be statically assigned (hard-coded) in the RESTful service source code.

#### Getting Started

To run WebApp locally, follow these steps:

- Python installed on your machine. You can download it from [here](https://www.python.org/downloads/).

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```bash
    cd <cloned directory>
    ```

3. Install Virtual Environment:

    ```bash
    python -m venv venv
    ```

4. Activate Virtual Environment:

    ```bash
    Windows: . venv/Scripts/activate 
    Linux: source venv/bin/activate
    ```

5. Install the project dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

6. Run the following command to apply migrations:

    ```bash
    python manage.py makemigrations 
    python manage.py migrate
    ```

7. Start the development server:

    ```bash
    python manage.py runserver
    ```

8. Open your web browser and go to [http://127.0.0.1:8000/]  to view the project.

- If you encounter any issues or have questions, feel free to reach out to me.


