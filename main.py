from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from TTS.api import TTS
import os
import hashlib
import time

app = Flask(__name__)
CORS(app)

# Crear carpetas necesarias
os.makedirs('audio_cache', exist_ok=True)
os.makedirs('models', exist_ok=True)

# Inicializar TTS (se descargará el modelo la primera vez)
print("Inicializando Coqui TTS...")
tts = None

# Configuración de voces con modelos de Coqui
VOICES = {
    'voz1': {
        'model': 'tts_models/es/css10/vits',
        'name': 'Voz Española Femenina',
        'language': 'es'
    },
    'voz2': {
        'model': 'tts_models/en/ljspeech/tacotron2-DDC',
        'name': 'Voz Inglesa Femenina',
        'language': 'en'
    },
    'voz3': {
        'model': 'tts_models/en/ljspeech/glow-tts',
        'name': 'Voz Inglesa Natural',
        'language': 'en'
    }
}

# Modelo por defecto (español)
DEFAULT_MODEL = 'tts_models/es/css10/vits'

def init_tts():
    """Inicializar el motor TTS"""
    global tts
    try:
        if tts is None:
            print(f"Cargando modelo: {DEFAULT_MODEL}")
            tts = TTS(model_name=DEFAULT_MODEL, progress_bar=False)
            print("✓ Modelo cargado exitosamente")
    except Exception as e:
        print(f"Error inicializando TTS: {e}")
        raise e

@app.route('/')
def home():
    """Página principal con información del servicio"""
    voices_list = "\n".join([f"- {key}: {val['name']}" for key, val in VOICES.items()])
    return f"""
    <h1>🎙️ TTS API con Coqui AI para Botrix</h1>
    <h2>Voces disponibles:</h2>
    <pre>{voices_list}</pre>
    <h3>Uso:</h3>
    <p><code>/tts?voice=voz1&text=Hola mundo</code></p>
    <h3>Para Botrix:</h3>
    <p><code>$(urlfetch {request.url_root}tts?voice=$(1)&text=$(2-))</code></p>
    <h3>Estado:</h3>
    <p>Motor TTS: {'✓ Listo' if tts else '✗ No inicializado'}</p>
    """

@app.route('/tts', methods=['GET'])
def generate_tts():
    """Endpoint principal para generar TTS"""
    try:
        # Inicializar TTS si no está listo
        if tts is None:
            init_tts()
        
        # Obtener parámetros
        voice = request.args.get('voice', 'voz1')
        text = request.args.get('text', '')
        
        # Validaciones
        if not text:
            return jsonify({'error': 'Falta el parámetro "text"'}), 400
        
        if voice not in VOICES:
            return jsonify({'error': f'Voz no válida. Usa: {", ".join(VOICES.keys())}'}), 400
        
        # Limitar longitud del texto
        if len(text) > 200:
            text = text[:200]
        
        # Crear hash único para el archivo (cache)
        file_hash = hashlib.md5(f"{voice}_{text}".encode()).hexdigest()
        audio_file = f'audio_cache/{file_hash}.wav'
        
        # Si no existe en cache, generar
        if not os.path.exists(audio_file):
            voice_config = VOICES[voice]
            
            # Si el modelo es diferente al actual, cargar nuevo modelo
            if voice_config['model'] != DEFAULT_MODEL:
                global tts
                print(f"Cambiando a modelo: {voice_config['model']}")
                tts = TTS(model_name=voice_config['model'], progress_bar=False)
            
            # Generar audio
            print(f"Generando audio para: {text[:50]}...")
            tts.tts_to_file(text=text, file_path=audio_file)
            print(f"✓ Audio generado: {audio_file}")
        
        # Devolver el archivo de audio
        return send_file(audio_file, mimetype='audio/wav')
    
    except Exception as e:
        print(f"Error en /tts: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/voices', methods=['GET'])
def list_voices():
    """Listar todas las voces disponibles"""
    return jsonify(VOICES)

@app.route('/models', methods=['GET'])
def list_models():
    """Listar todos los modelos disponibles de Coqui"""
    try:
        available_models = TTS.list_models()
        return jsonify({
            'total': len(available_models),
            'models': available_models
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    """Endpoint de prueba"""
    return jsonify({
        'status': 'online',
        'tts_ready': tts is not None,
        'voices': list(VOICES.keys()),
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
                    print(f"Limpiado: {filename}")
    except Exception as e:
        print(f"Error limpiando cache: {e}")

if __name__ == '__main__':
    print("Iniciando servidor TTS con Coqui...")
    init_tts()
    clean_old_cache()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)