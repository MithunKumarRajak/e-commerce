from decouple import config


def paypal(request):
    """Provide PayPal client id to templates from environment.

    Falls back to a default sandbox id if not provided so local dev keeps working.
    """
    default_client_id = 'Afc2YSc_RXQxN32Cm3R5uVWthMj-JHB3KSoR3LjVXAH5_e8gpCnFSglhaEJHVUI3CUNITv0V10YIbjxA'
    return {
        'PAYPAL_CLIENT_ID': config('PAYPAL_CLIENT_ID', default=default_client_id),
    }
