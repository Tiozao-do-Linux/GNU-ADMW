import time
import ipaddress
from user_agents import parse

class RenderTimeMiddleware:
    def process_request(self, request):
        start_time = time.time()
        print(f'Start time: {start_time}')
        self._start_time = start_time
        return

    def process_response(self, request, response):
        end_time = time.time()
        print(f'Ended time: {end_time}')
        render_time = end_time - self._start_time
        print(f'Render time: {render_time} seconds')
        response.render_time = render_time
        # Optionally, add render_time to the response context
        # response.context_data['render_time'] = render_time
        return response

class SimpleMiddleware:
    """
    Middleware to:
     - measure the time it takes to render a response,
     - detect browser, version and OS
     - collect remote IPs
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.website = {
            'name': 'My Website',
            'url': 'https://example.com'
            }
        print(f'SimpleMiddleware - __init__::')

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.
        # ⏱️ Time before the view
        start_time = time.time()
        request._start_time = start_time

        # 🕵️ Detect browser, version and OS
        user_agent_str = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_str)
        request._browser_info = f"{user_agent.browser.family} / {user_agent.browser.version_string} / {user_agent.os.family} /"

        # 🌐 Collect IPs and separate by type
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        ip_list = []
        if x_forwarded_for:
            ip_list = [ip.strip() for ip in x_forwarded_for.split(',')]
        else:
            remote_ip = request.META.get('REMOTE_ADDR', '')
            if remote_ip:
                ip_list = [remote_ip]

        ipv4 = []
        ipv6 = []
        for ip in ip_list:
            try:
                ip_obj = ipaddress.ip_address(ip)
                if ip_obj.version == 4:
                    ipv4.append(ip)
                elif ip_obj.version == 6:
                    ipv6.append(ip)
            except ValueError:
                continue  # Ignore invalid IP addresses

        ipv4_str = ', '.join(ipv4) if ipv4 else ''
        ipv6_str = ', '.join(ipv6) if ipv6 else ''
        request._remote_ip = f"{ipv4_str}{ipv6_str}"

        print(f'SimpleMiddleware - __call__::Before:: ')

        # Call the view
        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        end_time = time.time()
        load_time = end_time - start_time
        print(f'SimpleMiddleware - __call__::After:: Page Loaded in {load_time:.4f} seconds')
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Logic executed before a call to view. Gives access to the view itself & arguments
        start_time = time.time()
        response = view_func(request, *view_args, **view_kwargs)
        end_time = time.time()
        view_time = end_time - start_time
        print(f'SimpleMiddleware - process_view:: View function: {view_func.__name__} - View time: {view_time:.4f} seconds')
        return response

    def process_exception(self, request, exception):
        # Logic executed if an exception/error occurs in the view
        print(f'SimpleMiddleware - process_exception:: Exception: {exception}')
        pass

    def process_template_response(self, request, response):
        # Logic executed after the view is called, # ONLY IF view response is TemplateResponse, see listing 2-24 
        end_time = time.time()
        # Inject data into the response
        response.context_data['website'] = self.website
        response.context_data['render_time'] = end_time - getattr(request, '_start_time', end_time)
        response.context_data['browser_info'] = getattr(request, '_browser_info', 'Unknow')
        response.context_data['remote_ip'] = getattr(request, '_remote_ip', 'Unknow')
        print(f'SimpleMiddleware - process_template_response:: Render time: {response.context_data["render_time"]:.4f} seconds')
        return response

    def process_response(self, request, response):
        # Code to be executed for each response
        end_time = time.time()
        render_time = end_time - self._start_time
        response.render_time = render_time
        # Optionally, add render_time to the response context
        # response.context_data['render_time'] = render_time
        print(f'SimpleMiddleware - process_response:: Render time: {render_time} seconds')
        return response
