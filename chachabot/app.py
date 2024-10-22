from flask import Flask, request, jsonify, render_template, redirect, url_for
import re
import openai
from pymongo import MongoClient

openai.api_key = 'YOUR API KEY'

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot_users']  #database name
users = db['credentials']  #collection name

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.find_one({'username': username})
        if user and user['password'] == password:
            return redirect(url_for('home'))
        else:
            return "Invalid username or password", 400
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if len(password) < 8:
            return "Password must be at least 8 characters", 400
        elif not re.search("[0-9]", password):
            return "Password must contain at least one number", 400
        elif not re.search("[!@#$%^&*()_+=-{};:'<>,.?/`~]", password):
            return "Password must contain at least one special character", 400
        else:
            users.insert_one({'username': username, 'password': password})
            return redirect(url_for('login'))
    else:
        return render_template('signup.html')
    
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        data = request.get_json()
        input_text = data.get('input_text')

        keywords = [
    "RiverConservation", "WatershedManagement", "BiodiversityPreservation",
    "PollutionControl", "RiparianZones", "NamamiGangeProgram", "CleanGangaMission",
    "GangaActionPlan", "SewageTreatmentPlants", "RiverCleaningProjects",
    "RiverineEcology", "EcosystemServices", "FloraandFaunaofRivers",
    "WetlandConservation", "HabitatRestoration", "EcologicalBalance",
    "EnvironmentalImpact", "HumanActivitiesandImpact", "IndustrialPollution",
    "AgriculturalRunoff", "ClimateChangeEffects", "DeforestationandRiverHealth",
    "WaterQualityParameters", "MonitoringandTesting", "WaterPollutionSources",
    "SafeDrinkingWater", "WastewaterManagement", "CommunityAwareness",
    "RiverCleanupEvents", "VolunteerOpportunities", "StakeholderEngagement",
    "PublicParticipation", "EnvironmentalLaws", "RiverProtectionPolicies",
    "GovernmentInitiatives", "LegalFrameworksforRiverConservation",
    "ConservationOrganizations", "NGOsWorkingonRiverConservation",
    "EnvironmentalGroups", "ConservationFoundations",'what','what', 'river', 'rivers', 'campaign', 'hello', 'hey', 'clean', 'save', 'conservation', 'water', 'pollution', 'namami', 'gange', 'krishna', 'kaveri']

        if not any(keyword in input_text.lower() for keyword in keywords):
            return jsonify({'response': 'I can only respond to queries about rivers in India and related campaigns.'})


        # Input validation
        if not isinstance(input_text, str) or input_text == '':
            return jsonify({'error': 'Invalid input'}), 400

        try:
            # Call to GPT-3 API with timeout
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant which helps in creating awareness about river conservation, provide information about namami gange program and riverine ecology of India. Do not answer other questions"},
                    {"role": "user", "content": input_text}
                ]
            )
        except openai.OpenAIError as e:
            # Error handling
            return jsonify({'error': 'Error processing request: ' + str(e)}), 500

        return jsonify({'response': response['choices'][0]['message']['content']})
    else:
        # Handle GET request
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
