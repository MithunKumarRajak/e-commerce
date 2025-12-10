

from decouple import config


def paypal(request):
    """Provide PayPal client id to templates from environment.

    Falls back to a default sandbox id if not provided so local dev keeps working.
    """
    client_id = config('PAYPAL_CLIENT_ID', default='sb')
    if not client_id:
        client_id = 'sb'
    return {
        'PAYPAL_CLIENT_ID': client_id,
    }


def razorpay(request):
    """Provide Razorpay API key to templates from environment.

    Falls back to empty string if not provided.
    """
    key_id = config('RAZORPAY_KEY_ID', default='')
    return {
        'RAZORPAY_KEY_ID': key_id,
    }
