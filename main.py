import os
import requests
from openai import OpenAI # ¡NUEVA LIBRERÍA!

# La URL del Webhook y la Clave de la IA
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL") 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # ¡NUEVO NOMBRE DE CLAVE!

# --- FUNCIÓN DE INTERACCIÓN CON OPENAI ---
def generate_openai_phrase():
    """Conecta con el modelo de OpenAI y pide la frase motivacional de trading."""
    if not OPENAI_API_KEY:
        return "Error de IA: La clave de OpenAI no está configurada."

    try:
        # Inicializar el cliente de OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # El prompt para la IA:
        prompt = "Genera una frase motivacional de trading concisa, profunda y aplicable al día de hoy. Sin dar explicaciones, títulos, ni usar hashtags. Solo la frase."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Modelo rápido y estable
            messages=[
                {"role": "system", "content": "Eres un gurú de trading que da motivación concisa."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        # Extraer el texto de la respuesta
        return response.choices[0].message.content.strip()

    except Exception as e:
        # Manejo de errores que vimos antes (imprime en el log de GitHub)
        error_message = f"Error al generar la frase con OpenAI: {e}" 
        print(error_message) 
        return f"Error técnico con OpenAI: {e}" 

# --- FUNCIÓN DE ENVÍO CON WEBHOOK (SIN CAMBIOS) ---
def send_daily_message_via_webhook():
    """Genera la frase con la IA y la envía al Webhook de Discord."""
    
    if not WEBHOOK_URL:
        print("ERROR: La URL del Webhook no está configurada.")
        return

    # Usamos la nueva función de generación de OpenAI
    phrase = generate_openai_phrase()

    data = {
        "embeds": [{
            "title": "💡 Consejo de Trading por GPT-3.5 💡", # Cambiamos el título
            "description": f"**>>>** {phrase}",
            "color": 15844367, # Código de color verde/amarillo para OpenAI
            "footer": {"text": "Generado por el modelo GPT-3.5 Turbo"}
        }]
    }

    try:
        requests.post(WEBHOOK_URL, json=data).raise_for_status() 
        print("Mensaje de IA enviado con éxito vía Webhook.")
    except Exception as e:
        print(f"Error al enviar el mensaje por Webhook: {e}")

if __name__ == "__main__":
    send_daily_message_via_webhook()
