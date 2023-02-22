from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        reason = renderer_context['response'].reason_phrase
        count = len(data)
        response = {
            "status": "success",
            "message": reason,
            "count": len(data),
            "data": data,
        }

        if not str(status_code).startswith('2'):
            response["status"] = "error"
            response["message"] = reason
            del response['data']
            response["error"] = data

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)