from selenium import webdriver

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def fb_login():

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.fullscreen_window()
    driver.get('https://en-gb.facebook.com/login/')

    user_name = driver.find_element_by_id("email")
    user_name.send_keys('facebook_user_id')

    passwd = driver.find_element_by_id("pass")
    passwd.send_keys("facebook_user_password")

    sub = driver.find_element_by_id("loginbutton")
    sub.submit()

    f = driver.get_screenshot_as_png()

    driver.close()

    send_email_attach(f)


def send_email_attach(f):

    # Define your SMTP email server details
    smtp_server = 'smtp.gmail.com'
    smtp_user = 'user@gmail.com'
    smtp_pass = 'gmail_password'

    # email addesses to
    to_address = ['kalaiarasanbalaraman@gmail.com', 'phoenixkalai33@gmail.com']
    from_address = 'user@gmail.com'

    # actual component of email
    msg = MIMEMultipart('alternative')
    msg['To'] = ",".join(to_address)
    msg['From'] = from_address
    msg['Subject'] = 'This is my subject for this mail'

    # body of the actual message in html format
    html = """
        
        <h1> Please check the status of the report </h1>
        
        """

    # MIME type text
    msg.attach(MIMEText(html, 'html'))

    # atachments

    # Add file as application/octet-stream
    # Email client can usually download this automatically as attach
    part = MIMEBase("application", "octet-stream")

    part.set_payload((f))

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        "attachment; filename= image.jpg",
    )

    # Attach part into message
    msg.attach(part)

    # Send the message thru SMTP server
    s = smtplib.SMTP(smtp_server, 587)

    s.starttls()

    # provide smtp user and password
    s.login(smtp_user, smtp_pass)

    # finally sending HTML mail
    s.sendmail(from_address, to_address, msg.as_string())
    print("mail sent")
    s.quit()


if __name__ == '__main__':
    fb_login()
