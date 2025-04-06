from user_agents import parse
import time

class RenderTimeAndBrowserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._start_time = time.time()

        # Detect browser, version and OS
        user_agent_str = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_str)
        request._browser_info = f"{user_agent.browser.family} / {user_agent.browser.version_string} / {user_agent.os.family} /"

        # Remote IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            request._remote_ip = x_forwarded_for.split(',')[0].strip()
        else:
            request._remote_ip = request.META.get('REMOTE_ADDR', 'Unknow')

        return self.get_response(request)

    def process_template_response(self, request, response):
        end_time = time.time()

        response.context_data['render_time'] = end_time - getattr(request, '_start_time', end_time)
        response.context_data['browser_info'] = getattr(request, '_browser_info', 'Unknow')
        response.context_data['remote_ip'] = getattr(request, '_remote_ip', 'Unknow')

        return response

 