import logging
import azure.functions as func

import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = "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"
ADMIN_EMAIL_ADDRESS = "cyotmhnd@gmail.com"

def main(msg: func.ServiceBusMessage):
    
    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python Service bus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    host = "muhanproj3.postgres.database.azure.com"
    dbname = "techconfdb"
    user = "muhanad@muhanproj3"
    password = "Mohanad!09"
    sslmode = "require"

    try:
        # Construct connection string
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
        conn = psycopg2.connect(conn_string)
        logging.info("Connection established")

        cursor = conn.cursor()

        # TODO: Get notification message and subject from database using the notification_id
        cursor.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id))


        res_row = cursor.fetchone()


        # TODO: Get attendees email and name
        cursor.execute("SELECT email, first_name, last_name FROM attendee;")
        result_rows = cursor.fetchall()

        # TODO: Loop through each attendee and send an email with a personalized subject
        for attendee in result_rows:
            subject = '{}: {}'.format(format(attendee[1]), format(res_row[1]))
 

            email_msg = Mail(
                    from_email=ADMIN_EMAIL_ADDRESS,
                    to_emails=format(attendee[0]),
                    subject=format(res_row[1]),
                    plain_text_content=format(res_row[0]))
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            sg.send(email_msg)
            
            # logging.info("*****SEND_EMAIL: {}********".format(email_msg))            

            # send_email(format(attendee[0]), subject, format(res_row[0]))
            # logging.info("*****SUBJECT: {}********".format(subject))

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        # notification.completed_date = datetime.utcnow()
        completed_date = datetime.utcnow()
        status = 'Notified {} attendees'.format(len(result_rows))
        cursor.execute("UPDATE notification SET completed_date = {}, status = {} WHERE id = {};", (format(completed_date), format(status), format(notification_id)))
        conn.commit()

        # print("Updated 1 row of data")

        # TODO: Close connection
        conn.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(logging.error)

    finally:
        # TODO: Close connection
        cursor.close()

