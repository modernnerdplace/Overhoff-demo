from flask import Flask, request, send_file

##if Teams webhook alerting wanted - uncomment below :
#import pymsteams
#myTeamsMessage = pymsteams.connectorcard("<Microsoft Webhook URL>") #replace with Teams Webhook URL

global filename = "warning.png" #Debug
allowed_referers = [
        'login.microsoftonline.com',
        'login.microsoft.net',
        'login.microsoft.com',
        'autologon.microsoftazuread-sso.com',
        'tasks.office.com',
        'login.windows.net']
app = Flask(__name__)

@app.route('/companyBranding.png')
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
        app.run(debug=True)

if __name__ == "__main__":
    main()
