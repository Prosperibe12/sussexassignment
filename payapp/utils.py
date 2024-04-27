from abc import ABC, abstractmethod
import requests 

from register.models import Users, UserAccount
from payapp.models import Transaction

# currency conversion rate
def convert_currency(chosen_currency):
    '''
    This function converts user currency;
    currencies are USD, EUR, GBP
    '''
    # Exchange rates for GBP to EUR and USD
    exchange_rates = {'EUR': 1.17, 'USD': 1.27}  # these are example rates, they can be changed
    default_amount = 1000
    default_currency = 'GBP'
    # Convert default amount to chosen currency
    if default_currency == chosen_currency:
        return default_amount  # No conversion needed
    elif chosen_currency in exchange_rates:
        exchange_rate = exchange_rates[chosen_currency]
        converted_amount = int(default_amount * exchange_rate)
        return converted_amount
    else:
        raise ValueError("Chosen currency is not supported")

def api_currency_converter(amount, currency1, currency2):
    """
    make a get request to API Webservice
    """
    # base URL of your API
    base_url = 'http://localhost:8000/api/'

    # Make the GET request to the endpoint
    response = requests.get(f'{base_url}conversion/{currency1}/{currency2}/{amount}/')

    # Check the requeststatus code to see if successful
    if response.status_code == 200:
        # return the response content
        data = response.json()['converted_amount']
    else:
        # return the error message
        data = response.json()['error']
    return data 
    
class Command(ABC):
    
    @abstractmethod
    def execute(self):
        raise NotImplementedError("Subclass must override this")

class SendMoney(Command):
    '''
    The core class that handles money Transfer functionality. 
    the execute method orchestrates the entire transaction process, this can broken down into smaller, 
    more manageable functions. 
    '''
    # initialize variables
    def __init__(self, sender_email, recipient_email, amount, sender_pin):
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        self.amount = amount
        self.sender_pin = sender_pin

    def execute(self):
        try:
            # get sender and receipient object
            sender = Users.objects.get(email=self.sender_email)
            recipient = Users.objects.get(email=self.recipient_email)
        except Users.DoesNotExist:
            message = "User does not exist."
            return message

        # Check if sender has required amount
        sender_account = UserAccount.objects.get(user=sender)
        if sender_account.balance < self.amount:
            message = "Insufficient balance."
            return message

        # Check if sender's pin is correct
        if sender_account.pin != self.sender_pin:
            message = "Incorrect pin"
            return message

        # Perform currency conversion if necessary
        recipient_account = UserAccount.objects.get(user=recipient)
        if sender_account.currency != recipient_account.currency:
            # connect to currency converter that makes external API call
            convert_amount = api_currency_converter(self.amount, sender_account.currency, recipient_account.currency)
            converted_amount = int(convert_amount)
        else:
            converted_amount = self.amount

        # Update sender's balance
        sender_account.balance -= self.amount
        sender_account.save()

        # Update recipient's balance
        recipient_account.balance += converted_amount
        recipient_account.save()

        # Create transaction record
        transaction_creator = CreateTransaction(sender, recipient, converted_amount)
        transaction_creator.create_transaction()
        
        return True

class CreateTransaction:
    '''
    A Transaction class that creates a Transaction record. 
    This class will be instantiated from SendMoney.execute() method
    '''
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def create_transaction(self):
        transaction = Transaction.objects.create(
            amount=self.amount,
            Initiator=self.sender,
            Receiver=self.recipient,
            Transaction_status="Completed",
            Initiator_type="Debit",
            Receiver_type="Credit"
        )
        transaction.save()

class SendMoneyCommand(Command):
    
    def __init__(self, sender_email, recipient_email, amount, sender_pin):
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        self.amount = amount
        self.sender_pin = sender_pin

    def execute(self):
        sender = self.get_sender()
        recipient = self.get_recipient()
        if not isinstance(recipient, str):
            check_pin = self.validate_pin(sender)
            print("pin", check_pin)
            validate_balance = self.check_balance(sender)
            print("bal",validate_balance)
            if check_pin is True:
                print("i checked pin")
                if validate_balance is True:
                    print("i checked balance")
                    self.credit_recipient(recipient)
                    self.debit_sender(sender)
                    transaction_creator = CreateTransaction(sender, recipient, self.amount)
                    transaction_creator.create_transaction()
                    return True
                return validate_balance
            return check_pin
        return recipient

    def get_sender(self):
        try:
            return Users.objects.get(email=self.sender_email)
        except Users.DoesNotExist:
            return None

    def get_recipient(self):
        try:
            return Users.objects.get(email=self.recipient_email)
        except Users.DoesNotExist:
            message = "User does not exist."
            return message

    def validate_pin(self, sender):
        # validate senders pin
        if sender.useraccount.pin == self.sender_pin:
            return True
        message = "Incorrect pin"
        return message

    def check_balance(self, sender):
        # check that sender has required amount
        if sender.useraccount.balance >= self.amount:
            return True
        message = "Insufficient balance."
        return message

    def credit_recipient(self, recipient):
        # credit recipient account
        recipient.useraccount.balance += self.amount
        recipient.useraccount.save()

    def debit_sender(self, sender):
        # debit senders account
        sender.useraccount.balance -= self.amount
        sender.useraccount.save()
