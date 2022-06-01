from flask import current_app, render_template, url_for, request, abort, Blueprint, session
import stripe

stripe_checkout = Blueprint("stripe_checkout", __name__, static_folder="static", template_folder="templates") 


@stripe_checkout.route('/stripe_pay')
def stripe_pay():

    stripe.api_key = current_app.config['STRIPE_API_KEY']

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': "price_1L3cOeDegv4tzqIHR9Ramsc6",
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('main.stripe_checkout.thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('main.home', _external=True)
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': current_app.config['STRIPE_PUBLIC_KEY']
    }


@stripe_checkout.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():

    endpoint_secret_key = current_app.config['STRIPE_ENDPOINT_SECRET']

    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = endpoint_secret_key
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])
        
    return {}

@stripe_checkout.route('/thanks')
def thanks():
    if "username" in session:
        return render_template('thanks.html')
    else:
       return render_template('main.home')

