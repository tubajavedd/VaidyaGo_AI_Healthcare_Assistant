# Walkthrough - Platform Admin Chatbot

I have implemented the `chatbot_admin` module, a specialized AI for platform-wide administration. It follows the same modular architecture as the patient and doctor chatbots.

## Features & Capabilities

1.  **Platform Stats**: Get real-time counts of doctors, patients, and appointments.
2.  **Doctor Management**: List doctors pending verification.
3.  **System Monitoring**: Check the health status of system services.
4.  **Persona**: Operates as "Vado SuperAdmin", a professional platform management assistant.

## Architecture

- **Engine**: Orchestrates chat flow and memory.
- **Intent Service**: Uses Mistral LLM with improved JSON/Markdown parsing to detect admin commands.
- **Tool Router**: Executes administrative actions against the platform's database.
- **Models**: Isolated chat history in `chatbot_admin` app.

## API Endpoints

- **Chat**: `POST /api/vado-admin/chat/`
- **Tools**: `GET /api/vado-admin/tools/`

## Access Control

Strictly limited to users with the `ADMIN` role.
