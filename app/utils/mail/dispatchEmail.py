from app.utils.mail.emailService import send_email


async def dispatch(mail_type: str, recipients: list[str], context: dict | None = None):
    """Dispatch an email with an HTML body for common app events.

    Returns the send_email response dict.
    """
    context = context or {}

    match mail_type:
        case "contact":  # 📩 Contact Form
            subject = f"📩 New Contact Form Submission from {context.get('name', 'Unknown')}"
            body = f"""
<!DOCTYPE html>
<html>
  <head>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f9f9f9;
        padding: 20px;
        color: #333;
      }}
      .container {{
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      }}
  h2 {{ color: #4f46e5; }}
  p {{ line-height: 1.6; }}
  .label {{ font-weight: bold; }}
    </style>
  </head>
  <body>
    <div class="container">
      <h2>New Contact Form Submission</h2>
      <p><span class="label">Name:</span> {context.get('name')}</p>
      <p><span class="label">Email:</span> {context.get('email')}</p>
      <p><span class="label">Message:</span></p>
      <p>{context.get('message')}</p>
    </div>
  </body>
</html>
            """

        case "contribute":  # 💡 Contribution Form
            subject = f"💡 New Contribution Request from {context.get('name', 'Contributor')}"
            body = f"""
<!DOCTYPE html>
<html>
  <head>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f9f9f9;
        padding: 20px;
        color: #333;
      }}
      .container {{
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      }}
  h2 {{ color: #16a34a; }}
  p {{ line-height: 1.6; }}
  .label {{ font-weight: bold; }}
    </style>
  </head>
  <body>
    <div class="container">
      <h2>New Contribution Form Submission</h2>
      <p><span class="label">Name:</span> {context.get('name')}</p>
      <p><span class="label">Email:</span> {context.get('email')}</p>
      <p><span class="label">Contribution Type:</span> {context.get('type')}</p>
      <p><span class="label">Details:</span></p>
      <p>{context.get('details')}</p>
    </div>
  </body>
</html>
            """

        case "greeting":  # 👋 Greeting
            subject = "👋 Hello from FastAPI"
            body = f"<h2 style='color:#4f46e5'>Hi {context.get('name', 'User')}, welcome to our app!</h2>"

        case "reset_password":  # 🔑 Reset Password
            subject = "🔑 Reset Your Password"
            body = f"""
<p>Click the link below to reset your password:</p>
<p><a href="{context.get('reset_link', '#')}" 
style="color:#fff;background:#4f46e5;padding:10px 15px;border-radius:5px;text-decoration:none;">
Reset Password</a></p>
"""

        case "verification":  # ✅ Verification
            subject = "✅ Verify Your Email"
            body = f"<p>Your OTP is: <strong>{context.get('otp', '0000')}</strong></p>"

        case _:
            subject = "📢 Notification"
            body = "<p>This is a default notification email.</p>"

    return await send_email(subject, recipients, body, subtype="html")
