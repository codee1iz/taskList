from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session, send_file
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

login_html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ЖК «Пантелеон» — Система безопасности</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
            padding: 40px;
            width: 400px;
            text-align: center;
        }
        
        .logo {
            width: 80px;
            height: 80px;
            background: linear-gradient(45deg, #FFD700, #FFA500);
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            color: white;
            font-weight: bold;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
            font-weight: 300;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }
        
        input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .login-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
        }
        
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }
        
        .error {
            background: #ffe6e6;
            color: #d63031;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #d63031;
        }
        
        .footer {
            margin-top: 30px;
            color: #999;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">🏠</div>
        <h1>ЖК «Пантелеон»</h1>
        <p class="subtitle">Система безопасности и видеонаблюдения</p>
        
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="username">Логин</label>
                <input type="text" id="username" name="username" required placeholder="Введите логин">
            </div>
            
            <div class="form-group">
                <label for="password">Пароль</label>
                <input type="password" id="password" name="password" required placeholder="Введите пароль">
            </div>
            
            <button type="submit" class="login-btn">Войти в систему</button>
        </form>
        
        <div class="footer">
            © 2026 ЖК «Пантелеон» • Премиум качество жизни
        </div>
    </div>
</body>
</html>
"""


dashboard_html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ЖК «Пантелеон» — Панель управления</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .logo {
            width: 50px;
            height: 50px;
            background: linear-gradient(45deg, #FFD700, #FFA500);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        
        .header-text h1 {
            font-size: 24px;
            font-weight: 300;
            margin-bottom: 5px;
        }
        
        .header-text p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .logout-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .logout-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .main-content {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }
        
        .page-title {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .page-title h2 {
            font-size: 32px;
            color: #333;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .page-title p {
            color: #666;
            font-size: 18px;
        }
        
        .cameras-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .camera-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            border: 1px solid #f0f0f0;
        }
        
        .camera-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }
        
        .camera-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .camera-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 20px;
        }
        
        .camera-info h3 {
            font-size: 20px;
            color: #333;
            margin-bottom: 5px;
        }
        
        .camera-info p {
            color: #666;
            font-size: 14px;
        }
        
        .camera-status {
            margin: 20px 0;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .start-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .start-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }
        
        .start-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        .video-container {
            margin-top: 20px;
            text-align: center;
        }
        
        .video-container video {
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            max-width: 100%;
        }
        
        .status-message {
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            font-size: 14px;
        }
        
        .status-loading {
            background: #e3f2fd;
            color: #1976d2;
            border-left: 4px solid #1976d2;
        }
        
        .status-hint {
            background: #fff3e0;
            color: #f57c00;
            border-left: 4px solid #f57c00;
        }
        
        .status-error {
            background: #ffebee;
            color: #d32f2f;
            border-left: 4px solid #d32f2f;
        }
        
        .footer {
            text-align: center;
            padding: 40px 0;
            color: #666;
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .cameras-grid {
                grid-template-columns: 1fr;
            }
            
            .header-content {
                flex-direction: column;
                gap: 20px;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo">🏠</div>
                <div class="header-text">
                    <h1>ЖК «Пантелеон»</h1>
                    <p>Система безопасности</p>
                </div>
            </div>
            <a href="/logout" class="logout-btn">Выйти</a>
        </div>
    </header>

    <main class="main-content">
        <div class="page-title">
            <h2>Панель управления камерами</h2>
            <p>Мониторинг безопасности жилого комплекса</p>
        </div>

        <div class="cameras-grid">
            <div class="camera-card">
                <div class="camera-header">
                    <div class="camera-icon">📹</div>
                    <div class="camera-info">
                        <h3>Камера 1</h3>
                        <p>Подъезд</p>
                    </div>
                </div>
                <div class="camera-status" id="video1">
                    <button class="start-btn" onclick="start(1)">Включить камеру</button>
                </div>
            </div>

            <div class="camera-card">
                <div class="camera-header">
                    <div class="camera-icon">📹</div>
                    <div class="camera-info">
                        <h3>Камера 2</h3>
                        <p>Вход на территорию</p>
                    </div>
                </div>
                <div class="camera-status" id="video2">
                    <button class="start-btn" onclick="start(2)">Включить камеру</button>
                </div>
            </div>

            <div class="camera-card">
                <div class="camera-header">
                    <div class="camera-icon">📹</div>
                    <div class="camera-info">
                        <h3>Камера 3</h3>
                        <p>Дворовая территория</p>
                    </div>
                </div>
                <div class="camera-status" id="video3">
                    <button class="start-btn" onclick="start(3)">Включить камеру</button>
                </div>
            </div>
        </div>
    </main>

    <footer class="footer">
        <p>© 2026 ЖК «Пантелеон» • Система безопасности и видеонаблюдения</p>
    </footer>

    <script>
        function start(id) {
            const status = document.getElementById('video' + id);
            const button = status.querySelector('.start-btn');
            
            if (button) {
                button.disabled = true;
                button.textContent = 'Запуск...';
            }
            
            status.innerHTML = '<div class="status-message status-loading">Запуск камеры...</div>';

            
            let requestBody = { camera_id: id };
          

            fetch('/api/v2/camera/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody)
            })
            .then(r => r.json())
            .then(data => {
                if (data.video) {
                    status.innerHTML = `
                        <div class="video-container">
                            <video width="100%" height="240" controls autoplay>
                                <source src="${data.video}" type="video/mp4">
                                Ваш браузер не поддерживает видео.
                            </video>
                        </div>`;
                } else if (data.hint) {
                    status.innerHTML = `
                        <div class="status-message status-hint">
                            <strong>Подсказка:</strong> ${data.hint}
                        </div>
                        <button class="start-btn" onclick="start(${id})">Попробовать снова</button>`;
                } else if (data.error) {
                    status.innerHTML = `
                        <div class="status-message status-error">
                            <strong>Ошибка:</strong> ${data.error}
                        </div>
                        <button class="start-btn" onclick="start(${id})">Попробовать снова</button>`;
                }
            })
            .catch(e => {
                status.innerHTML = `
                    <div class="status-message status-error">
                        <strong>Ошибка соединения.</strong>
                    </div>
                    <button class="start-btn" onclick="start(${id})">Попробовать снова</button>`;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        return render_template_string(login_html, error="Неверный логин или пароль")
    return render_template_string(login_html)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template_string(dashboard_html)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/video')
def serve_video():
    filename = request.args.get('file', '')  
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'videos')
    filepath = os.path.join(base_dir, filename) 

    if os.path.exists(filepath) and os.path.isfile(filepath):
        return send_file(filepath, mimetype='video/mp4')
    else:
        return "Файл не найден", 404


video_files = {
    1: "camera1_video.mp4",
    2: "camera2_video.mp4",
    3: "camera3_video.mp4"
}

@app.route('/api/v2/camera/start', methods=['POST'])
def api_v2_camera_start():
    data = request.get_json(force=True)
    try:
        camera_id = int(data.get('camera_id'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid camera_id"}), 400

    filename = video_files.get(camera_id)
    if filename:
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'videos')
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            return jsonify({"status": "ok", "video": f"/video?file={filename}"})
        else:
            return jsonify({"error": "Видео не найдено"}), 404

    return jsonify({"error": "Invalid camera_id"}), 400

@app.route('/api/v1/camera/start', methods=['POST'])
def api_v1_camera_start():
    data = request.get_json(force=True)
    camera_id = data.get('camera_id')

    if camera_id == 3:
        token = data.get('token')
        if token == 'gold':
            return jsonify({"status": "ok", "video": "/video?file=s1ec1re1t_video.mp4"})
        else:
            return jsonify({"error": "token = gold"}), 401
    else:
        return jsonify({"error": "Invalid camera_id"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)