import random
from celery import Celery
from backgroundtest.celery import app

@app.task
def linking_background_notice(notice_id):
    try:
        notice = BackgroundNotice.objects.get(pk=notice_id)
        notice.notify_count += 1
        notice.save()
    except BackgroundNotice.DoesNotExist:
        logger.error(f"Background Notice with ID {notice_id} does not exist.")
        return
    except Exception as e:
        logger.error(
            f"An error occurred while retrieving notice with ID {notice_id}: {str(e)}"
        )
        return

    # Sending Mails To Users on Basis on Notice Type
    if notice.notice_type == "USER_VERFICATION_REMINDER":
        unverified_users = User.objects.filter(is_email_verified=False)

        for user in unverified_users:
            logger.debug("Inside USER_VERFICATION_REMINDER block")

            send_verification_remainder_email(
                recipient_email=user.email, customer_id=user.user_customer.id
            )
    else:
        pass  # for other notice type

