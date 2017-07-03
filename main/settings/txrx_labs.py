# A few TXRX specific constants which I am unsure where else to store

SAFETY_ID = 102 # course for safety orientation
SAFETY_CRITERION_ID = 7
ORIENTATION_ID = 105 # Event for member orientation
ORIENTATION_CRITERION_ID = 15

MEMBERSHIP_STATUS_FUNCTIONS = [
  'txrx.onboarding.active_membership',
  'txrx.onboarding.oriented',
  #'txrx.onboarding.documents',
  'txrx.onboarding.safety_training',
]
