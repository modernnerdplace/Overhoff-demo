from flask import Flask, request, send_file#

##if Teams webhook alerting wanted - uncomment below :
#import pymsteams
#myTeamsMessage = pymsteams.connectorcard("<Microsoft Webhook URL>") #replace with Teams Webhook URL

pixel_filename = "companyBranding.png"
allowed_referers = [
        'login.microsoftonline.com',
        'login.microsoft.net',
        'login.microsoft.com',
        'autologon.microsoftazuread-sso.com',
        'tasks.office.com',
        'login.windows.net']
app = Flask(__name__)
filename = "warning.png"

@app.route(f'/{pixel_filename}')
def pixel():
    requester_ip = request.remote_addr
    if len(request.headers.get('Referer')) > 0:
            referer_header = request.headers.get('Referer').replace("https://","").replace("/","")
    else:
            filename = "safe.png" 
    print(referer_header) #debug
    print(referer_header in allowed_referers) #debug       
    print(type(referer_header))
    if referer_header not in allowed_referers:
        print(f"[!] Non-Microsoft referer header detected: {referer_header}")
        print(f"[*] Requester IP (user logging in): {requester_ip}")
        print(f"[*] Referer header (AitM): {referer_header}")
        
        #Teams Webhook
        #myTeamsMessage.text(f"[*] Requester IP (user logging in): {requester_ip} & Referer header (AitM): {referer_header}")
        #myTeamsMessage.send()
    else: 
        filename = "safe.png" #debug
    return send_file(filename, mimetype='image/png',as_attachment=False)

def main():
        app.run(debug=True)

if __name__ == "__main__":
    main()
