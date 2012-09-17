from paypal.standard.ipn.signals import payment_was_successful, payment_was_flagged
from django.dispatch import receiver
from django.http import QueryDict
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail

@receiver(payment_was_successful, dispatch_uid='course.signals.handle_successful_payment')
def handle_successful_payment(sender, **kwargs):
    from course.models import Enrollment, Session
    print 'Got payment!'

    #see if the user exists
    email = sender.payer_email
    users = User.objects.filter(email=email)
    user_count = users.count()
    if user_count == 0:
        #create them
        user = User.objects.create_user(username=email, email=email)
        user.save()
        print "reseting password!"
        reset_password(user,email_template_name="email/welcome_classes.html")
        #TODO: also subscribe them to the TX/RX announcements mailing list
    elif user_count == 1:
        #get them
        user = users[0]
    elif user_count > 1:
        #WE GOT PROBLEMS
        user = None

    #add them to the classes they're enrolled in
    params = QueryDict(sender.query)
    class_count = int(params['num_cart_items'])

    for i in range(1, class_count+1):
        session_id = int(params['item_number%d' % (i, )])
        section_cost = int(float(params['mc_gross_%d' % (i, )]))

        session = Session.objects.get(id=session_id)

        #we're trusting during testing
        #enrollment = Enrollment(user=user, session=session)
        #enrollment.save()


        #make sure they didn't spoof things to paypal
        if section_cost == session.section.fee:
            #everything is groovy
            enrollment = Enrollment(user=user, session=session)
            enrollment.save()

        else:
            #they tried to cheat us
            #email the admins
            pass


@receiver(payment_was_flagged, dispatch_uid='course.signals.handle_flagged_payment')
def handle_flagged_payment(sender, **kwargs):
    #email people to let them intervene manually
    handle_successful_payment(sender, **kwargs)
