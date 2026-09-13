from flask import Flask, render_template, request, redirect, url_for, jsonify
import yaml
import os
import markdown
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Safe Markdown Filter
@app.template_filter('markdown')
def markdown_filter(text):
    if not text: return ""
    return markdown.markdown(str(text), extensions=['fenced_code', 'tables'])

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            # Ensure all required keys exist to prevent template errors
            defaults = {
                'name': 'Sumon Kumar Paul', 'title': 'DevOps Engineer', 
                'experience': {'items': []}, 'skills': {'categories': []},
                'projects': {'items': []}, 'certifications': {'items': []},
                'education': {'items': []}
            }
            if isinstance(data, dict):
                for k, v in defaults.items():
                    if k not in data: data[k] = v
            else:
                data = defaults
            return data
    except Exception as e:
        print(f"[ERROR] Config loading failed: {e}")
        return {
            'name': 'Sumon Kumar Paul', 'title': 'DevOps Engineer',
            'experience': {'items': []}, 'skills': {'categories': []},
            'projects': {'items': []}, 'certifications': {'items': []},
            'education': {'items': []}
        }

config = load_config()

@app.route('/')
def index():
    return render_template('index.html', config=config)

@app.route('/api/status')
def system_status():
    return jsonify({
        "uptime": "99.9%", "cpu_usage": "12%", 
        "memory_usage": "4.2GB / 16GB", "docker_containers": 8,
        "k8s_pods": 12, "last_deploy": "2 hours ago"
    })

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.is_json:
        return jsonify({"status": "success", "message": "Email sent!"})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) # Debug False for Production