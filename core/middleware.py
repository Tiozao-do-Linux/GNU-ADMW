import time
# from django.template.response import TemplateResponse
# from django.utils.deprecation import MiddlewareMixin


class RenderTimeMiddleware(object):
    """
    Middleware to measure the time it takes to render a template response.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Antes da view")
        begin_time = time.time()

        # Process the request
        response = self.get_response(request)

        print("Depois da view")
        end_time = time.time()
        render_time = end_time - begin_time
        # print(f'Render Time: {render_time}')

        if hasattr(response, 'context_data'):
            response.context_data['render_time'] = render_time
            print(f'response.context_data["render_time"]: {response.context_data["render_time"]}')
 
        return response
 