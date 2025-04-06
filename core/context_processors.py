import time
from user_agents import parse

def footer_info(request):
    # fake render time
    begin_time = time.time()
    end_time = time.time()
    render_time = end_time - begin_time

    # render_time = request.render_time
    #TODO : render_time not working

    # Detect browser, version and OS
    user_agent_str = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_str)
    browser_info = f"{user_agent.browser.family} / {user_agent.browser.version_string} / {user_agent.os.family} /"

    # Remote IP
    ip_address = request.META.get('REMOTE_ADDR', '')

    return {
        'render_time': render_time,
        'info_browser': browser_info,
        'info_remote_ip': ip_address
    }
