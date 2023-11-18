from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)
SESSION_CONFIGS = [
#dict(name='Hola', num_demo_participants=None, app_sequence=['Hola']),
#dict(name='campo_dinamico', num_demo_participants=1, app_sequence=['campo_dinamico']),
#dict(name='crazy_eights', num_demo_participants=1, app_sequence=['crazy_eights']),
#dict(name='image_choices', num_demo_participants=1, app_sequence=['image_choices']),
dict(name='queuing', num_demo_participants=None, app_sequence=['queuing'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

ROOMS = [
    dict(
        name='session_room',
        display_name='Session Room',
        participant_label_file='_rooms/participant_label.txt',
        # use_secure_urls=True
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
