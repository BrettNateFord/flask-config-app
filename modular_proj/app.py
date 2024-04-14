import os
import json
from flask import Flask, render_template, request
from data_ingestion import read_nmea_data_from_file
from data_parser import parse_nmea_message
from flask import redirect

app = Flask(__name__)

# Define the path to the parsing rules file
RULES_FILE_PATH = os.path.abspath(os.path.join('modular_proj', 'config', 'parsing_rules.json'))

def load_parsing_rules():
    if os.path.exists(RULES_FILE_PATH):
        with open(RULES_FILE_PATH, 'r') as file:
            data = file.read()
            if data.strip():  # Check if file is not empty
                return json.loads(data)
    return {}  # Return an empty dictionary if file is empty or not found

# Load parsing rules when the application starts
parsing_rules = load_parsing_rules()

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure', methods=['GET', 'POST'])
def configure():
    global parsing_rules
    parsing_rules_message = None
    if request.method == 'POST':
        sentence_type = request.form['sentence_type']
        field = request.form['field']
        index = int(request.form['index'])
        # Add or update parsing rule
        parsing_rules.setdefault(sentence_type, {})[field] = index
        # Save parsing rules to file
        with open(RULES_FILE_PATH, 'w') as file:
            json.dump(parsing_rules, file)
    else:
        parsing_rules_message = parsing_rules_message  # Message about parsing rules
    return render_template('configure.html', parsing_rules=parsing_rules, parsing_rules_message=parsing_rules_message)


@app.route('/sample_data')
def sample_data():
    # Read sample NMEA data from file
    nmea_data = read_nmea_data_from_file('sample_data.txt')
    return render_template('sample_data.html', nmea_data=nmea_data)

@app.route('/parsed_data')
def parsed_data():
    # Read sample NMEA data from file
    nmea_data = read_nmea_data_from_file('sample_data.txt')
    # Parse NMEA messages using configured parsing rules
    parsed_data = [parse_nmea_message(data, parsing_rules) for data in nmea_data]
    return render_template('parsed_data.html', parsed_data=parsed_data)

@app.route('/delete_rule', methods=['POST'])
def delete_rule():
    global parsing_rules
    sentence_type = request.form['sentence_type']
    field = request.form['field']
    # Remove the rule from the parsing_rules dictionary
    if sentence_type in parsing_rules and field in parsing_rules[sentence_type]:
        del parsing_rules[sentence_type][field]
        # Save parsing rules to file
        with open(RULES_FILE_PATH, 'w') as file:
            json.dump(parsing_rules, file)
    return redirect('/configure')  # Redirect to the configure page after deletion

# Define the file path for storing configuration data
CONFIG_FILE_PATH = os.path.abspath(os.path.join('modular_proj', 'config', 'power_bi_config.json'))

def save_configuration(data):
    """Save configuration data to a JSON file"""
    with open(CONFIG_FILE_PATH, 'w') as file:
        json.dump(data, file)

def load_configuration():
    """Load configuration data from the JSON file"""
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as file:
            return json.load(file)
    else:
        return None

@app.route('/power_bi_config', methods=['GET', 'POST'])
def power_bi_config():
    if request.method == 'POST':
        # Process form submission
        config_data = {
            'api_endpoint': request.form.get('api_endpoint', ''),
            'client_id': request.form.get('client_id', ''),
            'client_secret': request.form.get('client_secret', ''),
            'username': request.form.get('username', ''),
            'password': request.form.get('password', ''),
            'workspace_id': request.form.get('workspace_id', ''),
            'dataset_name': request.form.get('dataset_name', '')
        }
        # Save configuration data to a file
        save_configuration(config_data)
        return redirect('/power_bi_config')  # Redirect to the same page after saving configuration
    else:
        # Load configuration data from file (if available)
        config_data = load_configuration()
        return render_template('power_bi_config.html', config_data=config_data)
    
if __name__ == '__main__':
    app.run(debug=True)
