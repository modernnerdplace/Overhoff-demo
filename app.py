from flask import Flask, request, send_file
import os
import requests

##if Teams webhook alerting wanted - uncomment below :
#import pymsteams
#myTeamsMessage = pymsteams.connectorcard("<Microsoft Webhook URL>") #replace with Teams Webhook URL

allowed_referers = [
        'login.microsoftonline.com',
        'login.microsoft.net',
        'login.microsoft.com',
        'autologon.microsoftazuread-sso.com',
        'tasks.office.com',
        'login.windows.net']
app = Flask(__name__)

def get_public_ip():
    try:
        response = requests.get('http://ipv4.icanhazip.com', timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error obtaining public IP: {e}")
        return None

@app.route('/companyBranding.png', methods=['GET'])
def pixel():
    #requester_ip = request.remote_addr  #To fix.
    referer_header = str(request.headers.get('Referer'))   
    referer_header = referer_header.replace("https://","").replace("/","")
    if (referer_header not in allowed_referers) and (referer_header is not None) and (len(referer_header) > 1):
        print(f"[!] Non-Microsoft referer header detected: {referer_header}")
        print(f"[*] Referer header (AitM): {referer_header}")
        #print(f"[*] Requester IP (user logging in): {requester_ip}")    #To Fix.
        #Teams Webhook#
        #myTeamsMessage.text(f"[*] Requester IP (user logging in): {requester_ip} & Referer header (AitM): {referer_header}")
        #myTeamsMessage.send()  
        return send_file('warning.png', mimetype='image/png',as_attachment=False)
    else:
        return send_file('safe.png', mimetype='image/png',as_attachment=False) 

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

            app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=443, debug=True, use_reloader=False)

if __name__ == "__main__":
    main()
