# 🎙️ TTS Botrix Stream con Coqui AI

Sistema de Text-to-Speech (TTS) con voces IA realistas usando Coqui TTS v0.22.0 para streaming con Botrix.

## 🚀 Voces Disponibles

- `voz1` - Voz Española Femenina (Natural, modelo CSS10)
- `voz2` - Voz Inglesa Femenina (Tacotron2)
- `voz3` - Voz Inglesa Natural (Glow-TTS)

## ✨ Características

- 🎯 Voces IA ultra-realistas con Coqui TTS
- 🚀 Sistema de caché para respuestas rápidas
- 🌐 API REST simple para Botrix
- 🔄 Soporte para múltiples modelos
- 🎚️ Calidad de audio profesional

## 📦 Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/TU-USUARIO/tts-botrix-stream.git
cd tts-botrix-stream

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python main.py
```

**Nota:** La primera vez descargará los modelos de Coqui (~100-500MB por modelo).

## 🌐 Despliegue en Railway

### Opción 1: Desde GitHub (Recomendada)

1. Ve a https://railway.app y crea una cuenta
2. Click en "New Project" → "Deploy from GitHub repo"
3. Selecciona tu repositorio `tts-botrix-stream`
4. Railway detectará automáticamente el Procfile
5. Espera 5-10 minutos (descarga de modelos)
6. Obtén tu URL pública

### Opción 2: Render.com

1. Ve a https://render.com
2. "New" → "Web Service"
3. Conecta tu repositorio
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn main:app`

**⚠️ Importante:** Los modelos de Coqui ocupan espacio. Asegúrate de tener suficiente almacenamiento en tu plan gratuito.

## 🎮 Configuración en Botrix

### Comando básico:

```
!addcom !tts $(urlfetch https://TU-URL.railway.app/tts?voice=$(1)&text=$(2-))
```

### Comandos específicos por voz:

```
!addcom !tts1 $(urlfetch https://TU-URL.railway.app/tts?voice=voz1&text=$(1-))
!addcom !tts2 $(urlfetch https://TU-URL.railway.app/tts?voice=voz2&text=$(1-))
!addcom !tts3 $(urlfetch https://TU-URL.railway.app/tts?voice=voz3&text=$(1-))
```

### Uso en stream:

```
!tts voz1 Hola a todos en el stream
!tts1 Este mensaje usa la voz española
!tts2 This message uses the English voice
```

## 🛠️ API Endpoints

### Generar TTS
```
GET /tts?voice=voz1&text=Hola mundo
```

### Listar voces
```
GET /voices
```

### Ver modelos disponibles
```
GET /models
```

### Estado del servicio
```
GET /test
```

## 📝 Ejemplos de Uso

### En navegador:
```
https://TU-URL.railway.app/tts?voice=voz1&text=Hola desde Coqui TTS
```

### Con curl:
```bash
curl "https://TU-URL.railway.app/tts?voice=voz1&text=Prueba de audio" --output audio.wav
```

### Con Python:
```python
import requests

response = requests.get(
    'https://TU-URL.railway.app/tts',
    params={'voice': 'voz1', 'text': 'Hola mundo'}
)

with open('audio.wav', 'wb') as f:
    f.write(response.content)
```

## 🔧 Agregar Más Voces

Edita el diccionario `VOICES` en `main.py`:

```python
VOICES = {
    'voz4': {
        'model': 'tts_models/es/mai/tacotron2-DDC',
        'name': 'Otra Voz Española',
        'language': 'es'
    }
}
```

Para ver todos los modelos disponibles:
```bash
python -c "from TTS.api import TTS; print('\n'.join(TTS.list_models()))"
```

## 🎤 Clonar tu Propia Voz (Avanzado)

Para usar tu propia voz:

1. Graba 10-30 minutos de audio limpio
2. Usa el modelo `tts_models/multilingual/multi-dataset/your_tts`
3. Proporciona el archivo de referencia de tu voz

Documentación: https://github.com/coqui-ai/TTS

## ⚙️ Requisitos del Sistema

- Python 3.9-3.11
- 2GB RAM mínimo (4GB recomendado)
- 1GB espacio libre (para modelos)
- CPU: Cualquiera (GPU opcional para mayor velocidad)

## 🐛 Solución de Problemas

### Error: "No module named TTS"
```bash
pip install TTS==0.22.0
```

### Error: "CUDA not available"
Es normal si no tienes GPU. Coqui funcionará con CPU (más lento pero funcional).

### El audio no se genera
Revisa los logs del servidor y verifica que el modelo se haya descargado correctamente.

### Railway se queda sin memoria
Usa solo 1-2 modelos en la versión gratuita. Los modelos ocupan mucha RAM.

## 📚 Recursos

- [Coqui TTS GitHub](https://github.com/coqui-ai/TTS)
- [Documentación Botrix](https://botrix.live/docs/)
- [Lista de modelos Coqui](https://github.com/coqui-ai/TTS#released-models)

## 📄 Licencia

MIT License

## 🤝 Contribuciones

¡Pull requests son bienvenidos! Para cambios mayores, abre un issue primero.

---

**Hecho con ❤️ para la comunidad de streaming**
