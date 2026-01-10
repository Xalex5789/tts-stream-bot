# 🚀 GUÍA PASO A PASO - DEPLOY EN RAILWAY

## ✅ CHECKLIST DE ARCHIVOS

Antes de hacer deploy, verifica que tu repositorio tenga:

```
tts-stream-bot/
├── main.py              ✅ Ya lo tienes
├── requirements.txt     ✅ Ya lo tienes
├── runtime.txt          ✅ Ya lo tienes
├── Procfile            ⚠️  NUEVO - DESCÁRGALO
├── railway.json        ⚠️  NUEVO - DESCÁRGALO
├── .gitignore          ⚠️  RENOMBRA gitignore.txt a .gitignore
└── README.md           ⚠️  NUEVO - DESCÁRGALO
```

## 📥 PASO 1: AGREGAR LOS ARCHIVOS FALTANTES

### Opción A: Desde tu computadora

1. Descarga los 3 archivos nuevos que te di
2. Cópialos a la carpeta de tu proyecto local
3. Renombra `gitignore.txt` a `.gitignore`

### Opción B: Desde GitHub web

1. Ve a tu repo: https://github.com/Xalex5789/tts-stream-bot
2. Click en "Add file" → "Create new file"
3. Para cada archivo:
   - Nombre: `Procfile` (sin extensión)
   - Contenido: `web: gunicorn main:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - Click "Commit new file"
4. Repite para `railway.json` y el nuevo `README.md`

## 🔧 PASO 2: VERIFICAR requirements.txt

Tu `requirements.txt` debe tener exactamente esto:

```
flask==3.0.0
flask-cors==4.0.0
gtts==2.5.0
requests==2.31.0
gunicorn==21.2.0
```

✅ Ya lo tienes correcto.

## 🌐 PASO 3: DEPLOY EN RAILWAY

1. **Ir a Railway**
   - Ve a https://railway.app
   - Inicia sesión con GitHub

2. **Nuevo Proyecto**
   - Click "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Busca y selecciona `Xalex5789/tts-stream-bot`

3. **Esperar el Deploy**
   - Railway detectará automáticamente Python
   - Verás los logs en tiempo real
   - Espera 2-3 minutos
   - Debe decir: "Build successful" o similar

4. **Obtener tu URL**
   - Click en tu proyecto
   - Ve a "Settings"
   - Busca "Domains"
   - Click "Generate Domain"
   - Copia tu URL (ejemplo: `https://tts-stream-bot-production.up.railway.app`)

## 🧪 PASO 4: PROBAR QUE FUNCIONA

Reemplaza `TU-URL` con la URL que obtuviste:

### Test 1: Página principal
Abre en tu navegador:
```
https://TU-URL.railway.app/
```

Debes ver una página con la lista de voces.

### Test 2: Generar audio
Abre en tu navegador:
```
https://TU-URL.railway.app/tts?voice=voz1&text=Hola mundo
```

Debe descargar un archivo MP3. ¡Ábrelo y escúchalo!

### Test 3: Otra voz
```
https://TU-URL.railway.app/tts?voice=voz2&text=Bienvenidos al stream
```

## 🎮 PASO 5: CONFIGURAR BOTRIX

### 5.1 Ir a Botrix
1. Ve a https://botrix.live
2. Inicia sesión
3. Ve a tu Dashboard

### 5.2 Crear el Comando
1. Busca "Commands" o "Comandos"
2. Click "Add Command" o "Agregar Comando"
3. Llena así:

**Comando:**
```
!tts
```

**Respuesta:**
```
$(urlfetch https://TU-URL.railway.app/tts?voice=$(1)&text=$(2-))
```

**Ejemplo real:** Si tu URL es `https://tts-stream-bot-production.up.railway.app`:
```
$(urlfetch https://tts-stream-bot-production.up.railway.app/tts?voice=$(1)&text=$(2-))
```

### 5.3 Permisos
- Disponible para: Todos
- Cooldown: 5 segundos (opcional)

## 🎤 PASO 6: PROBAR EN TU STREAM

En el chat de tu stream escribe:

```
!tts voz1 Hola a todos en el stream
```

Botrix debería:
1. Capturar el mensaje
2. Llamar a tu API en Railway
3. Generar el audio
4. Reproducirlo en tu stream

## 🎯 COMANDOS EXTRAS (OPCIONAL)

Si quieres comandos más simples, crea estos en Botrix:

```
!tts1 → $(urlfetch https://TU-URL/tts?voice=voz1&text=$(1-))
!tts2 → $(urlfetch https://TU-URL/tts?voice=voz2&text=$(1-))
!tts3 → $(urlfetch https://TU-URL/tts?voice=voz3&text=$(1-))
!ttsen → $(urlfetch https://TU-URL/tts?voice=voz4&text=$(1-))
```

Así tus viewers solo escriben:
```
!tts1 Este es un mensaje
```

## ⚠️ PROBLEMAS COMUNES

### ❌ Error: "Application failed to respond"
**Causa:** Falta el archivo `Procfile`
**Solución:** Agrega el Procfile y vuelve a hacer deploy

### ❌ Railway dice "Build failed"
**Causa:** Error en requirements.txt o runtime.txt
**Solución:** Verifica que digan exactamente:
- `runtime.txt`: `python-3.10.13`
- `requirements.txt`: Las 5 líneas exactas que te mostré

### ❌ El audio no se genera
**Causa:** URL incorrecta o falta el parámetro `text`
**Solución:** 
1. Verifica la URL completa
2. Asegúrate de incluir `?voice=voz1&text=algo`
3. Prueba primero en el navegador

### ❌ Botrix no responde
**Causa:** Comando mal configurado
**Solución:**
1. Verifica que uses `$(urlfetch ...)`
2. No uses comillas en la URL
3. Asegúrate de que `$(1)` y `$(2-)` estén correctos

## 📞 ¿NECESITAS AYUDA?

Si algo no funciona, dime:
1. ¿En qué paso estás?
2. ¿Qué error ves exactamente?
3. ¿Ya tienes tu URL de Railway?
4. Muéstrame un screenshot de los logs de Railway

---

¡Buena suerte! 🚀
