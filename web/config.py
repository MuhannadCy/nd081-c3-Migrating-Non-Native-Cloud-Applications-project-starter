import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="muhanproj3.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="muhanad@muhanproj3" #TODO: Update value
    POSTGRES_PW="Mohanad!09"   #TODO: Update value
    POSTGRES_DB="techconfdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://muhanproj3.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=S1UD8SpFhf4mXiCKPE9K9S9CHs7e1obklxtS1gg2VBw=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'cyotmhnd@gmail.com'
    SENDGRID_API_KEY = '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' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False