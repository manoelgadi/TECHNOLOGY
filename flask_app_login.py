
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, url_for, make_response, redirect, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index_before_login.html")


import re
@app.route("/siwe_restricted", methods=["GET", "POST"])
def siwe_restricted():

    """ Validate MetaMask credentials and determine login status """
    if request.method == "POST":
        print("INSIDE FLASK - POSTED MM DATA AND GOT RESPONSE")
        req = request.get_json()  # type: dict
        signature = req['signature']  # type: string
        message = req['message']  # type: string

        account_pattern = r"0x[a-fA-F0-9]{40}"
        nonce_pattern = r"Nonce: (\d+)"
        account_match = re.search(account_pattern, message)
        nonce_match = re.search(nonce_pattern, message)
        if account_match and nonce_match:
            account_number = account_match.group(0)
            nonce = int(nonce_match.group(1))
            print("Account:", account_number)
            print("Nonce:", nonce)
        else:
            return("Account and nonce not found in the message.")
        print('RECEIVED POSTED METAMASK DATA signature="{}" / message="{}"'.format(signature,message))

        credentials_verified = True # verify_credentials(message, signature)
        print('after credentials_verified')
        if credentials_verified == True:
            return redirect(url_for('siwe_restricted'))
        else:
            return redirect(url_for('credentials_not_verified'))
    else:
        # TODO prevent unauthorized access: refactor with @login_required, sessions, etc.;
        return render_template('siwe_restricted.html')


@app.route('/credentials_not_verified')
def credentials_not_verified():
    return render_template('index.html')

@app.route("/info")
def info():
    return render_template('info.html')

