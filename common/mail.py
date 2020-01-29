# coding=utf-8
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from common import config
from common import logger


class Mail:
    """
    powered by Jhx at 2020/1/27
    用来获取配置并发送邮件
    """

    def __init__(self):
        self.mail_info = {}
        self.mail_info['from'] = config.config['mail']  # 发件人
        self.mail_info['username'] = config.config['mail']  # 发件邮箱账号
        self.mail_info['hostname'] = 'smtp.' + config.config['mail'][config.config['mail'].rfind('@') + 1:config.config[
            'mail'].__len__()]  # smtp服务器域名
        self.mail_info['password'] = config.config['pwd']  # 发件人的密码（163邮箱直接填邮箱密码，QQ邮箱填授权码）
        self.mail_info['to'] = str(config.config['mailto']).split(',')  # 收件人
        self.mail_info['cc'] = str(config.config['mailcopy']).split(',')  # 抄送人
        self.mail_info['mail_subject'] = config.config['mailtitle']  # 邮件标题
        self.mail_info['mail_encoding'] = config.config['mail_encoding']
        # 附件内容
        self.mail_info['filepaths'] = []
        self.mail_info['filenames'] = []

    def send(self, text):
        # 这里使用SMTP_SSL就是默认使用465端口，如果发送失败，可以使用587
        smtp = SMTP_SSL(self.mail_info['hostname'])
        smtp.set_debuglevel(0)  # 日志等级，0最低，1比较详细，2最详细
        smtp.ehlo(self.mail_info['hostname'])
        smtp.login(self.mail_info['username'], self.mail_info['password'])
        # 普通HTML邮件
        # msg=MIMEText(text,'html',self.mail_info['mail_encoding'])

        # 支持附件的邮件
        msg = MIMEMultipart()
        msg.attach(MIMEText(text, 'html', self.mail_info['mail_encoding']))
        msg['Subject'] = Header(self.mail_info['mail_subject'], self.mail_info['mail_encoding'])
        msg['from'] = self.mail_info['from']

        logger.debug(self.mail_info)
        logger.debug(text)
        msg['to'] = ','.join(self.mail_info['to'])
        msg['cc'] = ','.join(self.mail_info['cc'])
        receive = self.mail_info['to']
        receive += self.mail_info['cc']

        # 添加附件
        for i in range(len(self.mail_info['filepaths'])):
            att1 = MIMEText(open(self.mail_info['filepaths'][i], 'rb').read(), 'base64', 'utf-8')
            att1['Content_Type'] = 'application/octet-stream'
            att1['Content_Disposition'] = 'attachment;filename="' + self.mail_info['filenames'][i] + '"'
            msg.attach(att1)

        try:
            smtp.sendmail(self.mail_info['from'], receive, msg.as_string())
            smtp.quit()
            logger.info('邮件发送成功')
        except Exception as e:
            logger.error('邮件发送失败：')
            logger.exception(e)


# if __name__ == '__main__':
#     config.get_config('../lib/conf.properties')
#     logger.debug(config.config)
#     mail = Mail()
#     mail.send(config.config['mailtxt'])
