from flask import Flask, request, send_file
import os
import requests

##if Teams webhook alerting wanted - uncomment below :
#import pymsteams
#myTeamsMessage = pymsteams.connectorcard("<Microsoft Webhook URL>") #replace with Teams Webhook URL

pixel_filename = "companyBranding.png"
allowed_referers = [
        'https://login.microsoftonline.com/',
        'https://login.microsoft.net/',
        'https://login.microsoft.com/',
        'https://autologon.microsoftazuread-sso.com/',
        'https://tasks.office.com/',
        'https://login.windows.net/']
app = Flask(__name__)
filename = "warning.png"

def get_public_ip():
    try:
        response = requests.get('http://ipv4.icanhazip.com', timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error obtaining public IP: {e}")
        return None

@app.route(f'/{pixel_filename}')
def pixel():
    requester_ip = request.remote_addr
    referer_header = request.headers.get('Referer')
    if str(referer_header) not in allowed_referers:
        print(f"[!] Non-Microsoft referer header detected: {referer_header}")
        print("[*] Debug Information:")
        print(f"[*] Requester IP (user logging in): {requester_ip}")
        print(f"[*] Referer header (AitM): {referer_header}")
        #Teams Webhook
        #myTeamsMessage.text(f"[*] Requester IP (user logging in): {requester_ip} & Referer header (AitM): {referer_header}")
        #myTeamsMessage.send()
    return send_file(filename, mimetype='image/png')

def main():
    if not (os.path.exists('cert.pem') and os.path.exists('key.pem')):
        print("[-] SSL certificates not found. Please generate them using OpenSSL.\n  \\\\--> openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365")
    else:
        public_ip = get_public_ip()
        if public_ip:
            print()
            print("[*] Embed this pixel in your CSS file with the following code:\n")
            print("ext-sign-in-box {")
            print(f" background-image: url('https://{public_ip}/{pixel_filename}');")
            print(f"    background-size: 0 0;")
            print("}")
            print()

            app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=443, debug=False, use_reloader=False)

if __name__ == "__main__":
    main()
