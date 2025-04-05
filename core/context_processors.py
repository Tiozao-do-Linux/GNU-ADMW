import datetime
from user_agents import parse as parse_user_agent

def footer_info(request):
    now = datetime.datetime.now()
    
    # Detect browser, version and OS
    user_agent_str = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse_user_agent(user_agent_str)
    browser_info = f"{user_agent.browser.family} / {user_agent.browser.version_string} / {user_agent.os.family} /"

    # Remote IP
    ip_address = request.META.get('REMOTE_ADDR', 'Unknown')

    return {
        'info_now': now,
        'info_browser': browser_info,
        'infor_remote_ip': ip_address
    }
