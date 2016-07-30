import sendgrid
from sendgrid.helpers.mail import (
    Mail,
    Email,
    Content,
)


class FlaskSendGrid(object):
    app = None
    api_key = None
    default_from = None

    def __init__(self, app=None, **opts):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.api_key = app.config['SENDGRID_API_KEY']
        self.default_from = app.config['SENDGRID_DEFAULT_FROM']

    def send_email(self, **opts):
        if not opts.get('from_email', None) and not self.default_from:
            raise ValueError('No from email or default_from was configured')

        sg = sendgrid.SendGridAPIClient(apikey=self.api_key)

        to_email = Email(opts.get('to_email'))
        from_email = Email(opts.get('from_email', None) or self.default_from)
        subject = opts['subject']

        if opts.get('html', None):
            content = Content('html', opts['html'])
        elif opts.get('text', None):
            content = Content('text/plain', opts['text'])

        mail = Mail(from_email, subject, to_email, content)
        data = mail.get()
        response = sg.client.mail.send.post(request_body=data)

        return response.status_code
