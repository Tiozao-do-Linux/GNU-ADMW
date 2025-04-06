from user_agents import parse
import time
import ipaddress

class RenderTimeAndBrowserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._start_time = time.time()

        # Detect browser, version and OS
        user_agent_str = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_str)
        request._browser_info = f"{user_agent.browser.family} / {user_agent.browser.version_string} / {user_agent.os.family} /"

        # Collect IPs and separate by type
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
                continue  # Ignora IPs inválidos

        ipv4_str = ', '.join(ipv4) if ipv4 else ''
        ipv6_str = ', '.join(ipv6) if ipv6 else ''
        request._remote_ip = f"{ipv4_str}{ipv6_str}"

        return self.get_response(request)

    def process_template_response(self, request, response):
        end_time = time.time()

        response.context_data['render_time'] = end_time - getattr(request, '_start_time', end_time)
        response.context_data['browser_info'] = getattr(request, '_browser_info', 'Unknow')
        response.context_data['remote_ip'] = getattr(request, '_remote_ip', 'Unknow')

        return response

 