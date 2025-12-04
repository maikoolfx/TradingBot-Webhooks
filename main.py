import os
import requests
from google import genai 
from google.genai.errors import APIError

# Las claves se leen automáticamente de los secretos de GitHub
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL") 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

# --- FUNCIÓN DE INTERACCIÓN CON GEMINI ---
def generate_gemini_phrase():
    """Conecta con el modelo Gemini y pide la frase motivacional de trading."""
    if not GEMINI_API_KEY:
        return "Error de IA: La clave de Gemini API no está configurada."

    try:
        # Inicializar el cliente de Gemini
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # El prompt para la IA:
        prompt = "Genera una frase motivacional de trading concisa, profunda y aplicable al día de hoy. Sin dar explicaciones, títulos, ni usar hashtags. Solo la frase."

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                max_output_tokens=50 
            )
        )
        return response.text.strip()

    except APIError as e:
        print(f"Error de la API de Gemini: {e}")
        return "La API de Gemini reportó un error. Revisa la clave y la facturación."
    except Exception as e:
        print(f"Error general al generar la frase: {e}")
        return "La IA tuvo un problema técnico, pero tu disciplina debe continuar."

# --- FUNCIÓN DE ENVÍO CON WEBHOOK ---
def send_daily_message_via_webhook():
    """Genera la frase con la IA y la envía al Webhook de Discord."""
    
    if not WEBHOOK_URL:
        print("ERROR: La URL del Webhook no está configurada.")
        return

    phrase = generate_gemini_phrase()

    # Estructura del mensaje (Discord acepta HTML-like embeds)
    data = {
        "embeds": [{
            "title": "✨ Consejo de Trading por Gemini ✨",
            "description": f"**>>>** {phrase}",
            "color": 3447003, # Código de color azul
            "footer": {"text": "Generado por el modelo Gemini 2.5 Flash"}
        }]
    }

    try:
        # Enviamos la solicitud HTTP POST
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status() 
        print("Mensaje de IA enviado con éxito vía Webhook.")
    except Exception as e:
        print(f"Error al enviar el mensaje por Webhook: {e}")

# Ejecutar la función principal.
if __name__ == "__main__":
    send_daily_message_via_webhook()
