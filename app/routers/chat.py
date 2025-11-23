from fastapi import FastAPI, WebSocket, APIRouter
import os
# from fastapi.middleware.cors import CORSMiddleware
from google import genai
router = APIRouter()

# Configuración CORS para React Native
# router.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # O poner el dominio de tu app
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Inicializar el cliente de Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()

            # Generar respuesta usando Gemini
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=data
            )

            # Enviar respuesta al cliente
            await websocket.send_text(response.text)

        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")
            break