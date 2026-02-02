```python
from flask import Flask, request, jsonify, render_template_string
import stripe
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'truelove-secret-key')

# Stripe configuration
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')

# HTML Template for the app
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>1TrueLove.org - Find Your Perfect Match</title>
<script src="https://js.stripe.com/v3/"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Arial', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
.container { max-width: 1200px; margin: 0 auto; padding: 20px; }
.header { text-align: center; padding: 40px 0; }
.header h1 { font-size: 3em; margin-bottom: 10px; }
.header p { font-size: 1.2em; opacity: 0.9; }
.pricing { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin: 50px 0; }
.plan { background: rgba(255,255,255,0.1); border-radius: 15px; padding: 30px; text-align: center; backdrop-filter: blur(10px); }
.plan h3 { font-size: 2em; margin-bottom: 10px; }
.plan .price { font-size: 3em; font-weight: bold; margin: 20px 0; }
.plan ul { list-style: none; margin: 20px 0; }
.plan li { padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.2); }
.btn { background: #ff6b6b; color: white; border: none; padding: 15px 30px; border-radius: 25px; font-size: 1.1em; cursor: pointer; transition: all 0.3s; }
.btn:hover { background: #ff5252; transform: translateY(-2px); }
.features { margin: 50px 0; }
.feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
.feature { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center; }
.social-proof { text-align: center; margin: 50px 0; }
.counter { font-size: 2em; font-weight: bold; color: #ffd700; }
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>💕 1TrueLove.org</h1>
<p>The Ultimate Relationship Advisor - Find Your Perfect Match Today!</p>
<div class="social-proof">
<div class="counter">12,847</div>
<p>People Found Love This Year</p>
</div>
</div>

<div class="pricing">
<div class="plan">
<h3>Free</h3>
<div class="price">$0</div>
<ul>
<li>3 Assessments/Month</li>
<li>Basic Advice</li>
<li>Limited Features</li>
</ul>
<button class="btn" onclick="signUp('free')">Get Started Free</button>
</div>

<div class="plan" style="border: 3px solid #ffd700;">
<h3>Pro Plan</h3>
<div class="price">$14.99</div>
<ul>
<li>Unlimited Assessments</li>
<li>AI Insights</li>
<li>Progress Tracking</li>
<li>Email Support</li>
</ul>
<button class="btn" onclick="subscribe('pro')">Start Pro Plan</button>
</div>

<div class="plan">
<h3>VIP Plan</h3>
<div class="price">$29.99</div>
<ul>
<li>Everything in Pro</li>
<li>Expert Consultations</li>
<li>Priority Support</li>
<li>Advanced Analytics</li>
</ul>
<button class="btn" onclick="subscribe('vip')">Go VIP</button>
</div>

<div class="plan">
<h3>Elite Plan</h3>
<div class="price">$49.99</div>
<ul>
<li>Everything in VIP</li>
<li>Personal AI Coach</li>
<li>Unlimited Consultations</li>
<li>Success Guarantee</li>
</ul>
<button class="btn" onclick="subscribe('elite')">Join Elite</button>
</div>
</div>

<div class="features">
<h2 style="text-align: center; margin-bottom: 30px;">Why Choose 1TrueLove?</h2>
<div class="feature-grid">
<div class="feature">
<h3>🤖 AI-Powered Matching</h3>
<p>Advanced algorithms find your perfect compatibility</p>
</div>
<div class="feature">
<h3>👥 Expert Coaches</h3>
<p>Licensed relationship therapists guide your journey</p>
</div>
<div class="feature">
<h3>📊 Progress Tracking</h3>
<p>See your dating confidence grow over time</p>
</div>
<div class="feature">
<h3>🎯 Success Guarantee</h3>
<p>Find love in 90 days or get your money back</p>
</div>
</div>
</div>
</div>

<script>
const stripe = Stripe('{{ stripe_key }}');

function signUp(plan) {
alert('Free signup coming soon! For now, try our Pro plan.');
}

async function subscribe(plan) {
const prices = {
'pro': 1499,
'vip': 2999,
'elite': 4999
};

try {
const response = await fetch('/create-checkout-session', {
method: 'POST',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify({
plan: plan,
price: prices[plan]
}),
});

const session = await response.json();

if (session.url) {
window.location.href = session.url;
} else {
alert('Payment system coming soon! Email us at hello@1truelove.org');
}
} catch (error) {
alert('Payment system coming soon! Email us at hello@1truelove.org');
}
}
</script>
</body>
</html>
'''

@app.route('/')
def index():
return render_template_string(HTML_TEMPLATE, stripe_key=STRIPE_PUBLISHABLE_KEY)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
try:
data = request.get_json()

checkout_session = stripe.checkout.Session.create(
payment_method_types=['card'],
line_items=[{
'price_data': {
'currency': 'usd',
'product_data': {
'name': f'1TrueLove {data["plan"].title()} Plan',
},
'unit_amount': data['price'],
'recurring': {
'interval': 'month',
},
},
'quantity': 1,
}],
mode='subscription',
success_url='https://1truelove.org/success',
cancel_url='https://1truelove.org/',
)

return jsonify({'url': checkout_session.url})
except Exception as e:
return jsonify({'error': str(e)}), 400

@app.route('/success')
def success():
return '<h1>🎉 Welcome to 1TrueLove! Your subscription is active!</h1><p><a href="/">← Back to Home</a></p>'

if __name__ == '__main__':
app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```
