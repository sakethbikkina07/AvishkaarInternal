from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Hospital database for Srikakulam region
HOSPITALS_DATABASE = [
    {
        "id": 1,
        "name": "Government General Hospital Srikakulam",
        "type": "government",
        "location": "Srikakulam",
        "address": "Fort Road, Srikakulam - 532001",
        "phone": "08942-226666",
        "latitude": 18.2949,
        "longitude": 83.8938,
        "specialties": ["cardiac", "neurological", "respiratory", "trauma", "gastrointestinal", "orthopedic", "pediatric", "general"],
        "facilities": {
            "emergency": True,
            "icu": True,
            "opd": True,
            "icuBeds": 15,
            "icuAvailable": 8,
            "ventilators": 10,
            "ventilatorsAvailable": 6
        },
        "doctors": {
            "cardiac": 3,
            "neurological": 2,
            "respiratory": 2,
            "trauma": 4,
            "general": 8
        },
        "distance": 0
    },
    {
        "id": 2,
        "name": "Seven Hills Hospital",
        "type": "private",
        "location": "Srikakulam",
        "address": "NH-16, Srikakulam - 532001",
        "phone": "08942-228888",
        "latitude": 18.3020,
        "longitude": 83.8965,
        "specialties": ["cardiac", "neurological", "orthopedic", "general"],
        "facilities": {
            "emergency": True,
            "icu": True,
            "opd": True,
            "icuBeds": 10,
            "icuAvailable": 5,
            "ventilators": 8,
            "ventilatorsAvailable": 4
        },
        "doctors": {
            "cardiac": 2,
            "neurological": 2,
            "orthopedic": 3,
            "general": 5
        },
        "distance": 2
    },
    {
        "id": 3,
        "name": "Sai Sudha Hospital",
        "type": "private",
        "location": "Srikakulam",
        "address": "Peddapadu Road, Srikakulam - 532001",
        "phone": "08942-223333",
        "latitude": 18.2980,
        "longitude": 83.8900,
        "specialties": ["gastrointestinal", "orthopedic", "pediatric", "general"],
        "facilities": {
            "emergency": True,
            "icu": True,
            "opd": True,
            "icuBeds": 8,
            "icuAvailable": 3,
            "ventilators": 5,
            "ventilatorsAvailable": 2
        },
        "doctors": {
            "gastrointestinal": 2,
            "orthopedic": 2,
            "pediatric": 3,
            "general": 4
        },
        "distance": 1.5
    },
    {
        "id": 4,
        "name": "Area Hospital Amadalavalasa",
        "type": "government",
        "location": "Amadalavalasa",
        "address": "Main Road, Amadalavalasa - 532185",
        "phone": "08945-222222",
        "latitude": 18.4130,
        "longitude": 83.9050,
        "specialties": ["respiratory", "trauma", "gastrointestinal", "pediatric", "general"],
        "facilities": {
            "emergency": True,
            "icu": True,
            "opd": True,
            "icuBeds": 6,
            "icuAvailable": 4,
            "ventilators": 4,
            "ventilatorsAvailable": 3
        },
        "doctors": {
            "respiratory": 2,
            "trauma": 2,
            "pediatric": 2,
            "general": 5
        },
        "distance": 18
    },
    {
        "id": 5,
        "name": "Vijaya Hospital Palasa",
        "type": "private",
        "location": "Palasa",
        "address": "Station Road, Palasa - 532221",
        "phone": "08944-233333",
        "latitude": 18.7730,
        "longitude": 84.4130,
        "specialties": ["cardiac", "orthopedic", "general"],
        "facilities": {
            "emergency": True,
            "icu": True,
            "opd": True,
            "icuBeds": 5,
            "icuAvailable": 2,
            "ventilators": 4,
            "ventilatorsAvailable": 1
        },
        "doctors": {
            "cardiac": 1,
            "orthopedic": 2,
            "general": 3
        },
        "distance": 25
    },
    {
        "id": 6,
        "name": "Community Health Center Etcherla",
        "type": "government",
        "location": "Etcherla",
        "address": "Main Road, Etcherla - 532402",
        "phone": "08946-244444",
        "latitude": 18.4380,
        "longitude": 83.7790,
        "specialties": ["trauma", "pediatric", "general"],
        "facilities": {
            "emergency": True,
            "icu": False,
            "opd": True,
            "icuBeds": 0,
            "icuAvailable": 0,
            "ventilators": 0,
            "ventilatorsAvailable": 0
        },
        "doctors": {
            "trauma": 1,
            "pediatric": 2,
            "general": 3
        },
        "distance": 12
    },
    {
        "id": 7,
        "name": "Raghava Hospital",
        "type": "private",
        "location": "Narasannapeta",
        "address": "RTC Complex Road, Narasannapeta - 532421",
        "phone": "08943-255555",
        "latitude": 18.4160,
        "longitude": 84.0460,
        "specialties": ["neurological", "orthopedic", "general"],
        "facilities": {
            "emergency": True,
            "icu": True,
            "opd": True,
            "icuBeds": 4,
            "icuAvailable": 2,
            "ventilators": 3,
            "ventilatorsAvailable": 1
        },
        "doctors": {
            "neurological": 1,
            "orthopedic": 2,
            "general": 3
        },
        "distance": 35
    },
    {
        "id": 8,
        "name": "Sri Venkateswara Hospital",
        "type": "private",
        "location": "Ichapuram",
        "address": "Beach Road, Ichapuram - 532312",
        "phone": "08941-266666",
        "latitude": 19.1130,
        "longitude": 84.6840,
        "specialties": ["cardiac", "respiratory", "general"],
        "facilities": {
            "emergency": True,
            "icu": True,
            "opd": True,
            "icuBeds": 6,
            "icuAvailable": 3,
            "ventilators": 5,
            "ventilatorsAvailable": 2
        },
        "doctors": {
            "cardiac": 2,
            "respiratory": 1,
            "general": 4
        },
        "distance": 28
    },
    {
        "id": 9,
        "name": "Government Hospital Palakonda",
        "type": "government",
        "location": "Palakonda",
        "address": "Hospital Road, Palakonda - 532440",
        "phone": "08945-277777",
        "latitude": 18.6040,
        "longitude": 83.7580,
        "specialties": ["trauma", "gastrointestinal", "pediatric", "general"],
        "facilities": {
            "emergency": True,
            "icu": False,
            "opd": True,
            "icuBeds": 0,
            "icuAvailable": 0,
            "ventilators": 0,
            "ventilatorsAvailable": 0
        },
        "doctors": {
            "trauma": 2,
            "gastrointestinal": 1,
            "pediatric": 2,
            "general": 4
        },
        "distance": 42
    },
    {
        "id": 10,
        "name": "Lakshmi Nursing Home",
        "type": "private",
        "location": "Tekkali",
        "address": "Main Road, Tekkali - 532201",
        "phone": "08948-288888",
        "latitude": 18.6050,
        "longitude": 84.2360,
        "specialties": ["pediatric", "general"],
        "facilities": {
            "emergency": True,
            "icu": False,
            "opd": True,
            "icuBeds": 0,
            "icuAvailable": 0,
            "ventilators": 0,
            "ventilatorsAvailable": 0
        },
        "doctors": {
            "pediatric": 2,
            "general": 2
        },
        "distance": 38
    },
    {
        "id": 11,
        "name": "Apollo Clinic Srikakulam",
        "type": "private",
        "location": "Srikakulam",
        "address": "Railway Station Road, Srikakulam - 532001",
        "phone": "08942-235555",
        "latitude": 18.2970,
        "longitude": 83.8970,
        "specialties": ["cardiac", "respiratory", "gastrointestinal", "general"],
        "facilities": {
            "emergency": True,
            "icu": True,
            "opd": True,
            "icuBeds": 6,
            "icuAvailable": 4,
            "ventilators": 5,
            "ventilatorsAvailable": 3
        },
        "doctors": {
            "cardiac": 2,
            "respiratory": 1,
            "gastrointestinal": 1,
            "general": 3
        },
        "distance": 1
    },
    {
        "id": 12,
        "name": "Rajiv Gandhi Hospital",
        "type": "government",
        "location": "Sompeta",
        "address": "Main Road, Sompeta - 532284",
        "phone": "08946-299999",
        "latitude": 18.9460,
        "longitude": 84.5860,
        "specialties": ["trauma", "respiratory", "pediatric", "general"],
        "facilities": {
            "emergency": True,
            "icu": True,
            "opd": True,
            "icuBeds": 5,
            "icuAvailable": 3,
            "ventilators": 4,
            "ventilatorsAvailable": 2
        },
        "doctors": {
            "trauma": 2,
            "respiratory": 1,
            "pediatric": 2,
            "general": 4
        },
        "distance": 45
    }
]

def filter_hospitals(form_data):
    """Filter hospitals based on search criteria"""
    filtered = HOSPITALS_DATABASE.copy()
    
    # Filter by hospital type
    if form_data.get('hospitalType') and form_data['hospitalType'] != 'any':
        filtered = [h for h in filtered if h['type'] == form_data['hospitalType']]
    
    # Filter by location
    if form_data.get('location'):
        filtered = [h for h in filtered if h['location'] == form_data['location']]
    
    # Filter by consultation type
    consultation_type = form_data.get('consultationType')
    if consultation_type == 'icu':
        filtered = [h for h in filtered if h['facilities']['icu'] and h['facilities']['icuAvailable'] > 0]
    elif consultation_type == 'emergency':
        filtered = [h for h in filtered if h['facilities']['emergency']]
    elif consultation_type == 'opd':
        filtered = [h for h in filtered if h['facilities']['opd']]
    
    # Filter by disease type/specialty
    disease_type = form_data.get('diseaseType')
    if disease_type and disease_type != 'other':
        filtered = [h for h in filtered if disease_type in h['specialties']]
    
    # Sort by distance
    filtered.sort(key=lambda x: x['distance'])
    
    return filtered

@app.route('/')
def index():
    """Render the main page"""
    return render_template('main.html')

@app.route('/api/search-hospitals', methods=['POST'])
def search_hospitals():
    """API endpoint to search for hospitals based on criteria"""
    try:
        form_data = request.get_json()
        
        # Validate required fields
        required_fields = ['hospitalType', 'consultationType', 'diseaseType', 'patientAge', 'patientGender', 'location']
        for field in required_fields:
            if field not in form_data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Filter hospitals
        filtered_hospitals = filter_hospitals(form_data)
        
        # Log search for analytics
        search_log = {
            'timestamp': datetime.now().isoformat(),
            'criteria': form_data,
            'results_count': len(filtered_hospitals)
        }
        print(f"Search performed: {search_log}")
        
        return jsonify({
            'success': True,
            'hospitals': filtered_hospitals,
            'count': len(filtered_hospitals),
            'search_criteria': form_data
        })
    
    except Exception as e:
        print(f"Error in search_hospitals: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hospital/<int:hospital_id>', methods=['GET'])
def get_hospital_details(hospital_id):
    """Get detailed information about a specific hospital"""
    try:
        hospital = next((h for h in HOSPITALS_DATABASE if h['id'] == hospital_id), None)
        
        if hospital:
            return jsonify({
                'success': True,
                'hospital': hospital
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Hospital not found'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/hospital/<int:hospital_id>', methods=['GET'])
def hospital_page(hospital_id):
    """Render a details page for a single hospital"""
    try:
        hospital = next((h for h in HOSPITALS_DATABASE if h['id'] == hospital_id), None)
        if not hospital:
            return render_template('hospital_detail.html', hospital=None), 404

        return render_template('hospital_detail.html', hospital=hospital)
    except Exception as e:
        return render_template('hospital_detail.html', hospital=None, error=str(e)), 500


@app.route('/results', methods=['GET', 'POST'])
def results_page():
    """Render search results on a separate page (server-side)."""
    try:
        if request.method == 'POST':
            # form comes from the search page
            form = request.form
            form_data = {
                'hospitalType': form.get('hospitalType', ''),
                'consultationType': form.get('consultationType', ''),
                'diseaseType': form.get('diseaseType', ''),
                'patientAge': form.get('patientAge', ''),
                'patientGender': form.get('patientGender', ''),
                'location': form.get('location', ''),
                'additionalNotes': form.get('additionalNotes', '')
            }
        else:
            # allow GET queries as well
            args = request.args
            form_data = {
                'hospitalType': args.get('hospitalType', ''),
                'consultationType': args.get('consultationType', ''),
                'diseaseType': args.get('diseaseType', ''),
                'patientAge': args.get('patientAge', ''),
                'patientGender': args.get('patientGender', ''),
                'location': args.get('location', ''),
                'additionalNotes': args.get('additionalNotes', '')
            }

        filtered_hospitals = filter_hospitals(form_data)
        return render_template('search_results.html', hospitals=filtered_hospitals, criteria=form_data)

    except Exception as e:
        return render_template('search_results.html', hospitals=[], criteria={}, error=str(e)), 500

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get list of all available locations"""
    locations = sorted(list(set(h['location'] for h in HOSPITALS_DATABASE)))
    return jsonify({
        'success': True,
        'locations': locations
    })

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get overall statistics about hospitals"""
    total_hospitals = len(HOSPITALS_DATABASE)
    private_count = sum(1 for h in HOSPITALS_DATABASE if h['type'] == 'private')
    government_count = sum(1 for h in HOSPITALS_DATABASE if h['type'] == 'government')
    total_icu_beds = sum(h['facilities']['icuBeds'] for h in HOSPITALS_DATABASE)
    available_icu_beds = sum(h['facilities']['icuAvailable'] for h in HOSPITALS_DATABASE)
    
    return jsonify({
        'success': True,
        'statistics': {
            'total_hospitals': total_hospitals,
            'private_hospitals': private_count,
            'government_hospitals': government_count,
            'total_icu_beds': total_icu_beds,
            'available_icu_beds': available_icu_beds,
            'icu_occupancy_rate': round((1 - available_icu_beds/total_icu_beds) * 100, 2) if total_icu_beds > 0 else 0
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)