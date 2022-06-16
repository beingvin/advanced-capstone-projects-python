from flask import current_app, render_template, url_for, request, abort, Blueprint, session
from extention import mongodb_client
from bson import ObjectId, json_util
import stripe

stripe_mng = Blueprint("stripe_mng", __name__, static_folder="static", template_folder="templates") 


@stripe_mng .route('/stripe_pay',  methods=['POST'])
def stripe_pay():
    fetch_cart_items = request.json 
    cart_items = []
    for i in fetch_cart_items.items():
        for k in i[1]:
            # print(k)
            id = k["id"]
            quantity = k["quantity"]
            collection = mongodb_client.db.items.find_one({"_id":ObjectId(id)})
            # print(collection['title'])
            name = collection['title'] 
            brand = collection['brand'] 
            price = int(collection['price']+"00")
            items = {
            "price_data": {
                "currency": "INR",
                "product_data": { "name": f"{name}\n - brand - {brand}"},
                "unit_amount": price,
            },
            "quantity": quantity
            }
            cart_items.append(items)
    
    # print(cart_items)
 
    stripe.api_key = current_app.config['STRIPE_API_KEY']
 
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items = cart_items,
        mode='payment',
        success_url=url_for('main.mng_cart.stripe_mng.thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('main.home', _external=True)
    )
    return {
        "url":session["url"]
    }



@stripe_mng .route('/stripe_webhook', methods=['POST'])
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

@stripe_mng .route('/thanks')
def thanks():
    if "username" in session:
        return render_template('thanks.html')
    else:
       return render_template('main.home')

