# Third Party Stuff
from rest_framework.renderers import JSONRenderer


class AppsApiRenderer(JSONRenderer):
    media_type = "application/vnd.apps+json"
