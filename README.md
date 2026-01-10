# 🎙️ TTS API para Botrix - Con gTTS

Sistema de Text-to-Speech simple y efectivo usando Google TTS (gTTS) para streaming.

## 🚀 Características

- ✅ **5 voces diferentes** (español e inglés)
- ⚡ **Sistema de caché** para respuestas rápidas
- 🌐 **API REST** compatible con Botrix
- 🆓 **100% Gratis** - usa Google TTS
- 🔄 **Auto-limpieza** de archivos antiguos

## 🎤 Voces Disponibles

- `voz1` - Voz Mexicana (es-MX)
- `voz2` - Voz Española (es-ES)
- `voz3` - Voz Argentina (es-AR)
- `voz4` - Voz Inglesa USA (en-US)
- `voz5` - Voz Inglesa UK (en-GB)

## 📦 Deploy en Railway

### Paso 1: Preparar el repositorio

1. Asegúrate de tener estos archivos:
   - ✅ `main.py`
   - ✅ `requirements.txt`
   - ✅ `runtime.txt`
   - ✅ `Procfile` ⬅️ **IMPORTANTE**
   - ✅ `.gitignore`

### Paso 2: Subir a GitHub

```bash
git add .
git commit -m "Agregar Procfile para Railway"
git push
```

### Paso 3: Deploy en Railway

1. Ve a https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Selecciona tu repositorio
4. Espera 2-3 minutos
5. ¡Listo! Copia tu URL

## 🎮 Configurar en Botrix

### Comando Universal
```
!addcom !tts $(urlfetch https://TU-URL.railway.app/tts?voice=$(1)&text=$(2-))
```

### Comandos por Voz
```
!addcom !tts1 $(urlfetch https://TU-URL.railway.app/tts?voice=voz1&text=$(1-))
!addcom !tts2 $(urlfetch https://TU-URL.railway.app/tts?voice=voz2&text=$(1-))
!addcom !tts3 $(urlfetch https://TU-URL.railway.app/tts?voice=voz3&text=$(1-))
```

### Uso en Stream
```
!tts voz1 Hola a todos
!tts1 Mensaje en voz mexicana
!tts2 Mensaje en voz española
```

## 🧪 Probar tu API

### Ver página principal
```
https://TU-URL.railway.app/
```

### Generar audio
```
https://TU-URL.railway.app/tts?voice=voz1&text=Hola mundo
```

### Ver estado
```
https://TU-URL.railway.app/test
```

## 📡 Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Página de información |
| `/tts?voice=X&text=Y` | GET | Generar TTS |
| `/voices` | GET | Lista de voces |
| `/test` | GET | Estado del servidor |

## 🛠️ Instalación Local

```bash
# Clonar
git clone https://github.com/TU-USUARIO/tts-stream-bot.git
cd tts-stream-bot

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python main.py
```

Abre http://localhost:5000

## ⚙️ Requisitos

- Python 3.10+
- 512MB RAM mínimo
- Conexión a internet (para gTTS)

## 🐛 Solución de Problemas

### Railway no inicia
- ✅ Verifica que tengas el archivo `Procfile`
- ✅ Revisa los logs en Railway
- ✅ Asegúrate de usar Python 3.10+

### El audio no se descarga
- ✅ Verifica la URL completa
- ✅ Prueba con `?voice=voz1&text=hola`
- ✅ Revisa que el texto no esté vacío

### Botrix no reproduce
- ✅ Verifica la sintaxis del comando
- ✅ Prueba la URL en el navegador primero
- ✅ Asegúrate de usar `$(urlfetch ...)`

## 📄 Licencia

MIT License - Úsalo libremente

## 🤝 Contribuir

Pull requests bienvenidos. Para cambios grandes, abre un issue primero.

---

**Hecho con ❤️ para streamers**
