from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, EmailStr
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from app.baseUrl import BaseUrl

# It's best to store credentials as environment variables
APP_NAME = BaseUrl.appName


router = APIRouter()

SENDER_EMAIL = os.getenv('SENDER_EMAIL', '8kellyodogwu@gmail.com')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', 'gpam smge leww pxdv')
# ADMIN_EMAIL = "support@firmfrontierbank.com"

# Request body schema
class EmailSchema(BaseModel):
    to: EmailStr
    subject: str = 'No Subject'
    message: str
    full_name: str | None = None


# Admin reply email template
def build_generic_email_html(
    title: str,
    message: str,
    full_name: str | None = None,
    button_text: str | None = None,
    button_link: str | None = None,
) -> str:
    greeting = (
        f"<p style='margin:0 0 16px 0;font-size:16px;color:#0f172a;'>"
        f"Hi {full_name},</p>"
        if full_name else ""
    )

    button_html = ""
    if button_text and button_link:
        button_html = f"""
        <p style="margin:24px 0 0 0;">
          <a href="{button_link}"
             style="
               display:inline-block;
               padding:12px 22px;
               background:#0b61ff;
               color:#ffffff;
               text-decoration:none;
               border-radius:8px;
               font-weight:600;
               font-size:14px;">
            {button_text}
          </a>
        </p>
        """

    return f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>{title}</title>
      </head>

      <body style="
        margin:0;
        padding:0;
        background:#f4f6f8;
        font-family:-apple-system,BlinkMacSystemFont,
        'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;
      ">

        <table role="presentation" width="100%"
          style="
            max-width:600px;
            margin:40px auto;
            background:#ffffff;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 6px 20px rgba(16,24,40,0.08);
          ">

          <!-- Content -->
          <tr>
            <td style="padding:28px 30px;">
              <h2 style="
                margin:0 0 18px 0;
                font-size:20px;
                color:#0f172a;
                font-weight:600;
              ">
                {title}
              </h2>

              {greeting}

              <p style="
                margin:0;
                font-size:15px;
                line-height:1.7;
                color:#475569;
              ">
                {message}
              </p>

              {button_html}

              <p style="
                margin:28px 0 0 0;
                font-size:14px;
                color:#475569;
              ">
                Regards,<br>
                <strong>{APP_NAME} Support Team</strong>
              </p>

              <hr style="
                border:none;
                border-top:1px solid #eef2f7;
                margin:28px 0;
              " />

              <p style="
                margin:0;
                font-size:12px;
                color:#94a3b8;
              ">
                If you did not request this message, please ignore it or
                contact our support team.
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="
              background:#0b254b;
              color:#dbeafe;
              padding:14px 28px;
              text-align:center;
              font-size:12px;
            ">
              {APP_NAME} • Secure Communication
            </td>
          </tr>

        </table>
      </body>
    </html>
    """


@router.post('/send-email')
def send_email(email: EmailSchema):
    # Build email message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = email.subject
    msg['From'] = formataddr(('FirmFrontierBank', SENDER_EMAIL))
    msg['To'] = email.to
    # msg['Bcc'] = ADMIN_EMAIL
    recipients = [email.to]


    # Attach plain text and HTML
    msg.attach(MIMEText(email.message, 'plain'))
    msg.attach(
    MIMEText(
        build_generic_email_html(
            title=email.subject,
            message=email.message,
            full_name=email.full_name,
        ),
        "html"
    )
)


    try:
        # with smtplib.SMTP('mail.privateemail.com', 587) as server:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:

            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        return {'success': True, 'message': 'Email sent successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Email sending failed: {str(e)}')
