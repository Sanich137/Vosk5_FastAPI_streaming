import os

# server settings
host = os.getenv('HOST', '0.0.0.0')
port = int(os.getenv('PORT', 49153))


buffer_size = 20
model_name = "Vosk5"  ## Vosk5SmallStreaming  Vosk5 gigaam

base_sample_rate=16000  # Стрим из астериска отдаёт только 8к
MAX_OVERLAP_DURATION = 15.0  # Максимальная продолжительность буфера аудио (зависит от модели)
RECOGNITION_ATTEMPTS = 1