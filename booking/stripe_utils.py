import stripe
from django.conf import settings
from django.urls import reverse


def get_stripe_client():
    """Initialize and return Stripe with the secret key."""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe


def create_stripe_checkout_session(booking, request):
    """
    Create a Stripe Checkout Session for a booking payment.
    Returns the session object or raises an exception.
    """
    stripe_client = get_stripe_client()

    # Build absolute URLs for success and cancel
    success_url = request.build_absolute_uri(
        reverse('payment_success')
    ) + f'?session_id={{CHECKOUT_SESSION_ID}}&booking_id={booking.id}'

    cancel_url = request.build_absolute_uri(
        reverse('payment_cancel')
    ) + f'?booking_id={booking.id}'

    # Create checkout session
    session = stripe_client.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': f'Booking #{booking.id} - {booking.vendor.business_name}',
                    'description': f'{booking.event_type} on {booking.event_date} | {booking.number_of_guests} guests',
                },
                'unit_amount': int(booking.estimated_price * 100),  # Stripe expects amount in paise
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            'booking_id': str(booking.id),
            'customer_id': str(booking.customer.id),
        },
        customer_email=booking.customer.email,
    )

    return session


def verify_stripe_webhook(payload, sig_header):
    """
    Verify the Stripe webhook event signature.
    Returns the event object if valid, raises an exception if not.
    """
    stripe_client = get_stripe_client()
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    event = stripe_client.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )
    return event
