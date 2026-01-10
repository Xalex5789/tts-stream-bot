from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from gtts import gTTS
import os
import hashlib
import time

app = Flask(__name__)
CORS(app)

# Crear carpeta para audios si no existe
os.makedirs('audio_cache', exist_ok=True)

# Configuración de voces (Google TTS con diferentes acentos)
VOICES = {
    'voz1': {'lang': 'es', 'tld': 'com.mx', 'name': 'Voz Mexicana'},
    'voz2': {'lang': 'es', 'tld': 'es', 'name': 'Voz Española'},
    'voz3': {'lang': 'es', 'tld': 'com.ar', 'name': 'Voz Argentina'},
    'voz4': {'lang': 'en', 'tld': 'com', 'name': 'Voz Inglesa'},
    'voz5': {'lang': 'en', 'tld': 'co.uk', 'name': 'Voz Británica'},
}

@app.route('/')
def home():
    """Página principal con información del servicio"""
    voices_list = "\n".join([f"- {key}: {val['name']}" for key, val in VOICES.items()])
    return f"""
    <h1>🎙️ TTS API para Botrix</h1>
    <p>Sistema de Text-to-Speech con múltiples voces para streaming</p>
    
    <h2>Voces disponibles:</h2>
    <pre>{voices_list}</pre>
    
    <h3>📖 Uso:</h3>
    <p><code>/tts?voice=voz1&text=Hola mundo</code></p>
    
    <h3>🎮 Para Botrix:</h3>
    <p><code>$(urlfetch {request.url_root}tts?voice=$(1)&text=$(2-))</code></p>
    
    <h3>🎬 Para OBS:</h3>
    <p><code>{request.url_root}tts-overlay-widget.html</code></p>
    
    <h3>✅ Ejemplos:</h3>
    <ul>
        <li><a href="/tts?voice=voz1&text=Hola a todos">Probar voz1</a></li>
        <li><a href="/tts?voice=voz2&text=Bienvenidos al stream">Probar voz2</a></li>
        <li><a href="/tts-overlay-widget.html">Ver Overlay para OBS</a></li>
        <li><a href="/test">Ver estado del servidor</a></li>
    </ul>
    """

@app.route('/tts-overlay-widget.html')
def overlay_widget():
    """Servir el overlay HTML para OBS"""
    try:
        return send_from_directory('.', 'tts-overlay-widget.html')
    except FileNotFoundError:
        return """
        <h1>❌ Archivo no encontrado</h1>
        <p>El archivo tts-overlay-widget.html no está en el servidor.</p>
        <p>Asegúrate de que esté en la raíz del proyecto en GitHub.</p>
        <p><a href="/">Volver al inicio</a></p>
        """, 404

@app.route('/tts-overlay.html')
def overlay_basic():
    """Servir el overlay básico HTML para OBS"""
    try:
        return send_from_directory('.', 'tts-overlay.html')
    except FileNotFoundError:
        return """
        <h1>❌ Archivo no encontrado</h1>
        <p>El archivo tts-overlay.html no está en el servidor.</p>
        <p><a href="/">Volver al inicio</a></p>
        """, 404

@app.route('/tts', methods=['GET'])
def generate_tts():
    """Endpoint principal para generar TTS"""
    try:
        # Obtener parámetros
        voice = request.args.get('voice', 'voz1')
        text = request.args.get('text', '')
        
        # Validaciones
        if not text:
            return jsonify({'error': 'Falta el parámetro "text"'}), 400
        
        if voice not in VOICES:
            return jsonify({'error': f'Voz no válida. Usa: {", ".join(VOICES.keys())}'}), 400
        
        # Limitar longitud del texto (para evitar abusos)
        if len(text) > 200:
            text = text[:200]
        
        # Crear hash único para el archivo (cache)
        file_hash = hashlib.md5(f"{voice}_{text}".encode()).hexdigest()
        audio_file = f'audio_cache/{file_hash}.mp3'
        
        # Si no existe en cache, generar
        if not os.path.exists(audio_file):
            voice_config = VOICES[voice]
            tts = gTTS(text=text, lang=voice_config['lang'], tld=voice_config['tld'])
            tts.save(audio_file)
        
        # Devolver el archivo de audio
        return send_file(audio_file, mimetype='audio/mpeg')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/voices', methods=['GET'])
def list_voices():
    """Listar todas las voces disponibles"""
    return jsonify(VOICES)

@app.route('/tts-url', methods=['GET'])
def generate_tts_url():
    """Endpoint que devuelve URL del audio (para Botrix)"""
    try:
        voice = request.args.get('voice', 'voz1')
        text = request.args.get('text', '')
        
        if not text:
            return "❌ Falta el texto", 400
        
        if voice not in VOICES:
            return f"❌ Voz no válida. Usa: {', '.join(VOICES.keys())}", 400
        
        # Limitar longitud
        if len(text) > 200:
            text = text[:200]
        
        # Generar URL del audio
        audio_url = f"{request.url_root}tts?voice={voice}&text={text}"
        
        # Devolver solo texto simple para Botrix
        return f"✅ TTS: {text[:50]}... | {audio_url}"
    
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

@app.route('/test', methods=['GET'])
def test():
    """Endpoint de prueba"""
    return jsonify({
        'status': 'online',
        'voices': list(VOICES.keys()),
        'total_voices': len(VOICES),
        'timestamp': time.time()
    })

# Limpiar cache viejo (audios de más de 1 hora)
def clean_old_cache():
    try:
        current_time = time.time()
        for filename in os.listdir('audio_cache'):
            filepath = os.path.join('audio_cache', filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > 3600:  # 1 hora
                    os.remove(filepath)
    except Exception as e:
        print(f"Error limpiando cache: {e}")

if __name__ == '__main__':
    clean_old_cache()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
