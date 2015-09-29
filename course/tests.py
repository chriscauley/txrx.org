from django.test import TestCase

class ListenersTest(TestCase):
    """This tests all possible purchases from paypal and to make sure prices line up.
    This uses artificial IPN data, not the actual IPN."""
    def test_annonymous_purchase(self,params):
        """
        Pay for a class with a non-existent user. Verify price, enrollment, email, and new account.
        Then test the same user and make sure a second account was not created.
        """
        pass
    def test_discounts(self,params):
        """
        Pay for a class with a membership that has a discount.
        Make sure that the price was correct, the user is enrolled, and no new accounts were created.
        """
        pass
    def test_quantity(self,params):
        """
        Pay for a class with more than one quantity. Make sure enrollment and session.total students is correct
        Pay for a class that the user is alread enrolled in. ibid.
        """
        pass

class UtilsTest(TestCase):
    """ Test the following parameters of the get_or_create_student functions.
    paypal_email - should return correct student
    u_id - should return user.id = u_id or user.email = u_id
    subscr_id - tested in membership.tests
    send_mail - not tested
    """
    def test_paypal_email(self,params):
        pass
    def test_u_id_parameter(self,params):
        pass
