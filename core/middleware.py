import time

class TimeRenderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        inicio = time.time()
        response = self.get_response(request)
        fim = time.time()
        tempo = fim - inicio
        response.context_data = getattr(response, 'context_data', {}) or {}
        response.context_data['tempo_render'] = f"Página gerada em {tempo:.4f} Segundos"
        return response
