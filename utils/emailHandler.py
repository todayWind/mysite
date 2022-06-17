import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from conf import settings
from utils.logHandler import LogHandler


class EmailHandler:
    REPORT_PATH = settings.REPORT_PATH
    Log = LogHandler().log_fun()

    def __init__(self):
        self.message = MIMEMultipart()
        self.message['From'] = Header("我是发件人,wind", 'utf-8')  # 发件人
        self.message['To'] = Header("我是收件人,南京1班", 'utf-8')  # 收件人
        self.message['Subject'] = Header('自动化测试报告', 'utf-8')  # 邮件标题
        # 邮件正文内容
        send_content = 'hi man，你收到邮件了吗？'
        content_obj = MIMEText(send_content, 'plain', 'utf-8')  # 第一个参数为邮件内容
        self.message.attach(content_obj)

    def send_email(self, status: bool = False):
        # 构造附件1，发送自动化测试报告
        f = open(self.REPORT_PATH, 'rb').read()
        att1 = MIMEText(f, 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件附件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="report.html"'
        self.message.attach(att1)

        if status:
            try:
                smtpObj = smtplib.SMTP()
                smtpObj.connect(settings.MAIL_HOST, 25)  # 25 为 SMTP 端口号
                smtpObj.login(settings.MAIL_USER, settings.MAIL_PASS)
                smtpObj.sendmail(settings.SENDER, settings.RECEIVERS, self.message.as_string())
                logging.info("邮件发送成功")
                return '邮件发送成功'

            except smtplib.SMTPException:
                logging.error("Error: 无法发送邮件")
                return 'Error: 无法发送邮件'
        return


if __name__ == '__main__':
    em = EmailHandler()
    em.send_email()
