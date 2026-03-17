import json
import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db.models import Sum

from .models import Booking
from .payment_models import Payment
from .stripe_utils import create_stripe_checkout_session, verify_stripe_webhook


def is_customer(user):
    return user.is_authenticated and user.role == 'Customer'


@login_required
@user_passes_test(is_customer, login_url='home')
def payment_page(request, booking_id):
    """Display payment summary page for a booking."""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)

    # Security: only allow payment for accepted bookings
    if booking.status not in ('Accepted', 'Pending Payment'):
        messages.error(request, "This booking is not eligible for payment.")
        return redirect('customer_booking_history')

    # Prevent duplicate payments
    existing_payment = Payment.objects.filter(
        booking=booking,
        payment_status='Completed'
    ).first()

    if existing_payment:
        messages.info(request, "Payment has already been completed for this booking.")
        return redirect('customer_booking_history')

    context = {
        'booking': booking,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'booking/payment_page.html', context)


@login_required
@user_passes_test(is_customer, login_url='home')
@require_POST
def create_checkout_session(request, booking_id):
    """Create a Stripe Checkout Session and redirect to Stripe."""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)

    # Security checks
    if booking.status not in ('Accepted', 'Pending Payment'):
        messages.error(request, "This booking is not eligible for payment.")
        return redirect('customer_booking_history')

    # Prevent duplicate payments
    existing_payment = Payment.objects.filter(
        booking=booking,
        payment_status='Completed'
    ).first()

    if existing_payment:
        messages.info(request, "Payment has already been completed for this booking.")
        return redirect('customer_booking_history')

    try:
        # Update booking status to Pending Payment
        booking.status = 'Pending Payment'
        booking.save()

        # Create Stripe Checkout Session
        session = create_stripe_checkout_session(booking, request)

        # Create a pending payment record
        Payment.objects.create(
            booking=booking,
            customer=request.user,
            amount=booking.estimated_price,
            payment_method='Card',
            stripe_payment_id=session.id,
            payment_status='Pending',
        )

        return redirect(session.url, code=303)

    except stripe.error.StripeError as e:
        messages.error(request, f"Payment error: {str(e)}")
        return redirect('payment_page', booking_id=booking.id)
    except Exception as e:
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect('payment_page', booking_id=booking.id)


@login_required
@user_passes_test(is_customer, login_url='home')
def payment_success(request):
    """Handle successful payment redirect from Stripe."""
    session_id = request.GET.get('session_id')
    booking_id = request.GET.get('booking_id')

    if not session_id or not booking_id:
        messages.error(request, "Invalid payment session.")
        return redirect('customer_booking_history')

    try:
        booking = get_object_or_404(Booking, id=booking_id, customer=request.user)

        # Retrieve the Stripe session to verify payment
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid':
            # Update the payment record
            payment = Payment.objects.filter(
                booking=booking,
                stripe_payment_id=session_id,
            ).first()

            if payment:
                payment.payment_status = 'Completed'
                payment.stripe_payment_id = session.payment_intent
                payment.save()
            else:
                # Create payment record if webhook hasn't done it yet
                Payment.objects.create(
                    booking=booking,
                    customer=request.user,
                    amount=booking.estimated_price,
                    payment_method='Card',
                    stripe_payment_id=session.payment_intent,
                    payment_status='Completed',
                )

            # Update booking status
            booking.status = 'Confirmed'
            booking.save()

            context = {
                'booking': booking,
                'payment': Payment.objects.filter(
                    booking=booking,
                    payment_status='Completed'
                ).first(),
            }
            return render(request, 'booking/payment_success.html', context)
        else:
            messages.warning(request, "Payment is still being processed. Please wait.")
            return redirect('customer_booking_history')

    except stripe.error.StripeError as e:
        messages.error(request, f"Error verifying payment: {str(e)}")
        return redirect('customer_booking_history')
    except Exception as e:
        messages.error(request, "Error processing payment confirmation.")
        return redirect('customer_booking_history')


@login_required
@user_passes_test(is_customer, login_url='home')
def payment_cancel(request):
    """Handle cancelled payment redirect from Stripe."""
    booking_id = request.GET.get('booking_id')
    booking = None

    if booking_id:
        try:
            booking = Booking.objects.get(id=booking_id, customer=request.user)
            # Revert booking status back to Accepted if it was Pending Payment
            if booking.status == 'Pending Payment':
                booking.status = 'Accepted'
                booking.save()

            # Mark any pending payments as Failed
            Payment.objects.filter(
                booking=booking,
                payment_status='Pending'
            ).update(payment_status='Failed')
        except Booking.DoesNotExist:
            pass

    context = {
        'booking': booking,
    }
    return render(request, 'booking/payment_cancel.html', context)


@login_required
@user_passes_test(is_customer, login_url='home')
def customer_payments(request):
    """Display payment history for the logged-in customer."""
    payments = Payment.objects.filter(
        customer=request.user
    ).select_related('booking', 'booking__vendor').order_by('-created_at')

    context = {
        'payments': payments,
    }
    return render(request, 'booking/customer_payments.html', context)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhook events."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    if not sig_header:
        return HttpResponse(status=400)

    try:
        event = verify_stripe_webhook(payload, sig_header)
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        booking_id = session.get('metadata', {}).get('booking_id')

        if booking_id:
            try:
                booking = Booking.objects.get(id=booking_id)

                # Update or create payment record
                payment, created = Payment.objects.get_or_create(
                    booking=booking,
                    stripe_payment_id=session.get('id'),
                    defaults={
                        'customer': booking.customer,
                        'amount': booking.estimated_price,
                        'payment_method': 'Card',
                        'payment_status': 'Completed',
                    }
                )

                if not created:
                    payment.payment_status = 'Completed'
                    payment.stripe_payment_id = session.get('payment_intent', payment.stripe_payment_id)
                    payment.save()

                # Update booking status
                booking.status = 'Confirmed'
                booking.save()

            except Booking.DoesNotExist:
                pass

    elif event['type'] == 'payment_intent.payment_failed':
        session = event['data']['object']
        # Mark related payments as failed
        Payment.objects.filter(
            stripe_payment_id=session.get('id'),
            payment_status='Pending'
        ).update(payment_status='Failed')

    return HttpResponse(status=200)
