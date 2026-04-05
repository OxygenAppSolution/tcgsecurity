from flask import Flask, render_template, flash, redirect, url_for,request
from forms import ContactForm
import os
from flask_mail import Mail, Message

os.environ.get
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

app = Flask(__name__)

# Security: Pulling values from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# --- EMAIL CONFIGURATION ---
# --- EMAIL CONFIGURATION ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False  # Add this explicitly
# Use .strip() to ensure no hidden spaces from the .env file cause the 535 error
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME').strip()
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD').strip()
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME').strip()

# This will print the SMTP conversation to your terminal
# Temporary Sanity Check
raw_pass = os.environ.get('MAIL_PASSWORD')
print(f"DEBUG: Password starts with: {raw_pass[:2]}... and ends with ...{raw_pass[-2:]}")
print(f"DEBUG: Password length is: {len(raw_pass.strip())} (Should be 16)")

mail = Mail(app)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        service = request.form.get('service')
        message_body = request.form.get('message')

        # Create the email
        msg = Message(subject=f"New Contact Lead: {name}",
                      recipients=[app.config['MAIL_USERNAME']])
        
        msg.body = f"""
        The City Guard Website:
        
        Name: {name}
        Email: {email}
        service: {service}
        
        Message:
        {message_body}
        """

        try:
            mail.send(msg)
            flash("Your message has been sent successfully! We will contact you shortly.", "success")
        except Exception as e:
            flash("There was an error sending your message. Please try again later.", "danger")
            print(f"Error: {e}")

        return render_template('contact.html')

    return render_template('contact.html')


# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

from flask import Flask, render_template, abort

# ... your other code ...

# This dictionary holds the full details for each service
SERVICES_DATA = {
    'armed': {
        'title': 'Armed Security Services',
        'subtitle': 'Elite Texas-Licensed Commissioned Officers',
        'image': 'service1.png',
        'full_description': 'The City Guard provides elite, Texas-licensed Commissioned Officers for locations requiring a decisive security presence. Our armed division is comprised of individuals who have met the highest standards of tactical proficiency and ethical conduct.',
        'features': [
            'Elite Veteran Presence: We actively recruit Ex-Military Veterans.',
            'Multilingual Capability: Officers available in multiple languages.',
            'Superior Training: Tactical and de-escalation training.',
            'Rigorous Vetting: Exhaustive background checks.',
            'Tactical Deterrence: Professional armed presence.'
        ]
    },
    'unarmed': {
        'title': 'Unarmed Security Services',
        'subtitle': 'Professional Concierge & Vigilance',
        'image': 'service2.png',
        'full_description': 'Our Unarmed division focuses on high-visibility deterrence and professional customer service. Ideal for corporate environments, retail, and low-risk residential areas.',
        'features': [
            'Professional Concierge: Friendly yet firm gatekeeping.',
            'Regular Foot Patrols: Constant presence on the move.',
            'Incident Reporting: Detailed digital logs.',
            'Access Control: Managing visitor logs strictly.'
        ]
    }
}

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/service/<service_key>')
def service_detail(service_key):
    service = SERVICES_DATA.get(service_key)
    if not service:
        abort(404)
    return render_template('service_detail.html', service=service)



# --- ERROR HANDLERS ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

import os
from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

import os

if __name__ == '__main__':
    # Use the port assigned by DigitalOcean, or default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)