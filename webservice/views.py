from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status 
        
class CurrencyConverterAPIView(APIView):
    """
    Convert an amount from one currency to another using a given exchange rate.
    
    Parameters:
        amount (float): The amount to convert.
        from_currency (str): The currency of the amount.
        to_currency (str): The currency to convert to.
        exchange_rate (dict): A dictionary containing exchange rates between currencies.
    
    Returns:
        float: The converted amount.
    """
    exchange_rate = {
        'USD': {'GBP': 0.75, 'EUR': 0.85},
        'GBP': {'USD': 1.33, 'EUR': 1.14},
        'EUR': {'USD': 1.18, 'GBP': 0.88}
    }

    def get_conversion_rate(self, currency1, currency2):
        """
        Get the conversion rate between two currencies.
        """
        if currency1 in self.exchange_rate and currency2 in self.exchange_rate[currency1]:
            return self.exchange_rate[currency1][currency2]
        else:
            raise ValueError("Exchange rate not available for the specified currencies.")

    def get(self, request, currency1, currency2, amount):
        """
        Convert an amount from one currency to another.
        """
        try:
            amount = float(amount)
            if currency1 == currency2:
                return Response({'converted_amount': amount}, status=status.HTTP_200_OK)
            else:
                conversion_rate = self.get_conversion_rate(currency1, currency2)
                converted_amount = amount * conversion_rate
                return Response({'converted_amount': converted_amount}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
