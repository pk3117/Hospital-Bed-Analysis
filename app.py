from flask import Flask, render_template, request, jsonify, redirect, flash
import json
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Simulated hospital data (so you can test everything without Hive)
def get_simulated_hospitals():
    hospitals = [
        # Delhi NCR Hospitals
        {
            "name": "AIIMS Delhi",
            "city": "Delhi",
            "total_beds": 2200,
            "occupied_beds": 1980,
            "icu_beds": 250,
            "date": "2025-10-07"
        },
        {
            "name": "Apollo Hospital Delhi",
            "city": "Delhi", 
            "total_beds": 695,
            "occupied_beds": 210,
            "icu_beds": 85,
            "date": "2025-10-07"
        },
        {
            "name": "Fortis Escorts Heart Institute",
            "city": "Delhi",
            "total_beds": 310,
            "occupied_beds": 85,
            "icu_beds": 45,
            "date": "2025-10-07"
        },
        {
            "name": "Max Super Specialty Hospital",
            "city": "Delhi",
            "total_beds": 500,
            "occupied_beds": 430,
            "icu_beds": 65,
            "date": "2025-10-07"
        },
        
        # Mumbai Hospitals
        {
            "name": "Kokilaben Dhirubhai Ambani Hospital",
            "city": "Mumbai",
            "total_beds": 750,
            "occupied_beds": 680,
            "icu_beds": 95,
            "date": "2025-10-07"
        },
        {
            "name": "Lilavati Hospital",
            "city": "Mumbai",
            "total_beds": 323,
            "occupied_beds": 290,
            "icu_beds": 42,
            "date": "2025-10-07"
        },
        {
            "name": "Tata Memorial Hospital",
            "city": "Mumbai",
            "total_beds": 600,
            "occupied_beds": 580,
            "icu_beds": 80,
            "date": "2025-10-07"
        },
        {
            "name": "Jaslok Hospital",
            "city": "Mumbai",
            "total_beds": 350,
            "occupied_beds": 315,
            "icu_beds": 50,
            "date": "2025-10-07"
        },
        
        # Chennai Hospitals
        {
            "name": "Apollo Speciality Hospital",
            "city": "Chennai",
            "total_beds": 300,
            "occupied_beds": 60,
            "icu_beds": 40,
            "date": "2025-10-07"
        },
        {
            "name": "MIOT International Hospital",
            "city": "Chennai",
            "total_beds": 350,
            "occupied_beds": 300,
            "icu_beds": 45,
            "date": "2025-10-07"
        },
        {
            "name": "Fortis Malar Hospital",
            "city": "Chennai",
            "total_beds": 180,
            "occupied_beds": 150,
            "icu_beds": 25,
            "date": "2025-10-07"
        },
        {
            "name": "Global Health City",
            "city": "Chennai", 
            "total_beds": 400,
            "occupied_beds": 350,
            "icu_beds": 55,
            "date": "2025-10-07"
        },
        
        # Bangalore Hospitals
        {
            "name": "Manipal Hospital",
            "city": "Bangalore",
            "total_beds": 600,
            "occupied_beds": 540,
            "icu_beds": 75,
            "date": "2025-10-07"
        },
        {
            "name": "Narayana Health",
            "city": "Bangalore",
            "total_beds": 500,
            "occupied_beds": 450,
            "icu_beds": 65,
            "date": "2025-10-07"
        },
        {
            "name": "Fortis Hospital Bangalore",
            "city": "Bangalore",
            "total_beds": 400,
            "occupied_beds": 360,
            "icu_beds": 50,
            "date": "2025-10-07"
        },
        {
            "name": "Apollo Hospital Bangalore",
            "city": "Bangalore",
            "total_beds": 250,
            "occupied_beds": 220,
            "icu_beds": 35,
            "date": "2025-10-07"
        },
        
        # Hyderabad Hospitals
        {
            "name": "Yashoda Hospitals",
            "city": "Hyderabad",
            "total_beds": 700,
            "occupied_beds": 130,
            "icu_beds": 90,
            "date": "2025-10-07"
        },
        {
            "name": "Continental Hospitals",
            "city": "Hyderabad",
            "total_beds": 350,
            "occupied_beds": 310,
            "icu_beds": 45,
            "date": "2025-10-07"
        },
        {
            "name": "KIMS Hospitals",
            "city": "Hyderabad",
            "total_beds": 400,
            "occupied_beds": 360,
            "icu_beds": 55,
            "date": "2025-10-07"
        },
        {
            "name": "Apollo Hospitals Hyderabad",
            "city": "Hyderabad",
            "total_beds": 300,
            "occupied_beds": 270,
            "icu_beds": 40,
            "date": "2025-10-07"
        },
        
        # Kolkata Hospitals
        {
            "name": "Apollo Gleneagles Hospital",
            "city": "Kolkata",
            "total_beds": 350,
            "occupied_beds": 315,
            "icu_beds": 48,
            "date": "2025-10-07"
        },
        {
            "name": "AMRI Hospitals",
            "city": "Kolkata",
            "total_beds": 400,
            "occupied_beds": 360,
            "icu_beds": 52,
            "date": "2025-10-07"
        },
        {
            "name": "Fortis Hospital Kolkata",
            "city": "Kolkata",
            "total_beds": 300,
            "occupied_beds": 270,
            "icu_beds": 42,
            "date": "2025-10-07"
        },
        {
            "name": "Ruby General Hospital",
            "city": "Kolkata",
            "total_beds": 200,
            "occupied_beds": 180,
            "icu_beds": 30,
            "date": "2025-10-07"
        },
        
        # Pune Hospitals
        {
            "name": "Ruby Hall Clinic",
            "city": "Pune",
            "total_beds": 550,
            "occupied_beds": 495,
            "icu_beds": 70,
            "date": "2025-10-07"
        },
        {
            "name": "Jehangir Hospital",
            "city": "Pune",
            "total_beds": 350,
            "occupied_beds": 315,
            "icu_beds": 48,
            "date": "2025-10-07"
        },
        {
            "name": "Sahyadri Hospital",
            "city": "Pune",
            "total_beds": 400,
            "occupied_beds": 360,
            "icu_beds": 55,
            "date": "2025-10-07"
        },
        {
            "name": "Noble Hospital",
            "city": "Pune",
            "total_beds": 250,
            "occupied_beds": 225,
            "icu_beds": 35,
            "date": "2025-10-07"
        },
        
        # Ahmedabad Hospitals
        {
            "name": "Apollo Hospital Ahmedabad",
            "city": "Ahmedabad",
            "total_beds": 300,
            "occupied_beds": 270,
            "icu_beds": 42,
            "date": "2025-10-07"
        },
        {
            "name": "CIMS Hospital",
            "city": "Ahmedabad",
            "total_beds": 350,
            "occupied_beds": 315,
            "icu_beds": 48,
            "date": "2025-10-07"
        },
        {
            "name": "Sterling Hospitals",
            "city": "Ahmedabad",
            "total_beds": 250,
            "occupied_beds": 225,
            "icu_beds": 35,
            "date": "2025-10-07"
        },
        
        # Chandigarh Hospitals
        {
            "name": "PGIMER Chandigarh",
            "city": "Chandigarh",
            "total_beds": 1800,
            "occupied_beds": 1020,
            "icu_beds": 220,
            "date": "2025-10-07"
        },
        {
            "name": "Fortis Hospital Mohali",
            "city": "Chandigarh",
            "total_beds": 300,
            "occupied_beds": 20,
            "icu_beds": 42,
            "date": "2025-10-07"
        }
    ]
    return hospitals
# Store hospitals in memory (for demo purposes)
hospital_data = get_simulated_hospitals()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add_hospital')
def add_hospital_page():
    return render_template('add_hospital.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

# Helper function
def get_occupancy_status(rate):
    """Helper function to determine occupancy status"""
    if rate >= 80: return {"text": "High", "color": "danger"}
    if rate >= 60: return {"text": "Medium", "color": "warning"}
    return {"text": "Low", "color": "success"}

# API Routes
@app.route('/api/all_hospitals')
def all_hospitals():
    """Get all hospital data for dashboard display"""
    try:
        hospitals = []
        for hospital in hospital_data:
            total_beds = hospital["total_beds"]
            occupied_beds = hospital["occupied_beds"]
            available_beds = total_beds - occupied_beds
            occupancy_rate = round((occupied_beds * 100.0) / total_beds, 2) if total_beds > 0 else 0
            
            hospitals.append({
                "name": hospital["name"],
                "total_beds": total_beds,
                "occupied_beds": occupied_beds,
                "icu_beds": hospital["icu_beds"],
                "city": hospital["city"],
                "date": hospital["date"],
                "available_beds": available_beds,
                "occupancy_rate": occupancy_rate,
                "status": get_occupancy_status(occupancy_rate)
            })
        
        print(f"Returning {len(hospitals)} hospitals")
        return jsonify(hospitals)
    except Exception as e:
        print(f"Error in all_hospitals: {e}")
        return jsonify({"error": str(e)})

@app.route('/api/statistics')
def statistics():
    """Get overall statistics"""
    try:
        total_hospitals = len(hospital_data)
        total_beds = sum(h["total_beds"] for h in hospital_data)
        occupied_beds = sum(h["occupied_beds"] for h in hospital_data)
        available_beds = total_beds - occupied_beds
        icu_beds = sum(h["icu_beds"] for h in hospital_data)
        cities_covered = len(set(h["city"] for h in hospital_data))
        overall_occupancy_rate = round((occupied_beds * 100.0) / total_beds, 2) if total_beds > 0 else 0
        
        stats = {
            "total_hospitals": total_hospitals,
            "total_beds": total_beds,
            "occupied_beds": occupied_beds,
            "icu_beds": icu_beds,
            "cities_covered": cities_covered,
            "available_beds": available_beds,
            "overall_occupancy_rate": overall_occupancy_rate
        }
        
        print("Statistics:", stats)
        return jsonify(stats)
    except Exception as e:
        print(f"Error in statistics: {e}")
        return jsonify({"error": str(e)})

@app.route('/api/timeseries_data')
def timeseries_data():
    """Get time series data for charts"""
    try:
        # Generate last 7 days of data with some variation
        dates = []
        total_beds_data = []
        occupied_beds_data = []
        icu_beds_data = []
        available_beds_data = []
        
        base_total = sum(h["total_beds"] for h in hospital_data)
        
        for i in range(6, -1, -1):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            dates.append(date)
            
            # Add some realistic variation
            variation = random.uniform(-0.05, 0.05)
            occupied = int(base_total * (0.65 + variation))
            
            total_beds_data.append(base_total)
            occupied_beds_data.append(occupied)
            available_beds_data.append(base_total - occupied)
            icu_beds_data.append(sum(h["icu_beds"] for h in hospital_data))
        
        return jsonify({
            "dates": dates,
            "total_beds": total_beds_data,
            "occupied_beds": occupied_beds_data,
            "icu_beds": icu_beds_data,
            "available_beds": available_beds_data
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/city_data')
def city_data():
    """Get city-wise data for charts"""
    try:
        # Group by city
        city_stats = {}
        for hospital in hospital_data:
            city = hospital["city"]
            if city not in city_stats:
                city_stats[city] = {
                    "total_beds": 0,
                    "occupied_beds": 0,
                    "icu_beds": 0,
                    "hospital_count": 0
                }
            
            city_stats[city]["total_beds"] += hospital["total_beds"]
            city_stats[city]["occupied_beds"] += hospital["occupied_beds"]
            city_stats[city]["icu_beds"] += hospital["icu_beds"]
            city_stats[city]["hospital_count"] += 1
        
        cities = []
        total_beds = []
        occupied_beds = []
        icu_beds = []
        hospital_counts = []
        occupancy_rates = []
        
        for city, stats in city_stats.items():
            cities.append(city)
            total_beds.append(stats["total_beds"])
            occupied_beds.append(stats["occupied_beds"])
            icu_beds.append(stats["icu_beds"])
            hospital_counts.append(stats["hospital_count"])
            occupancy_rate = round((stats["occupied_beds"] * 100.0) / stats["total_beds"], 2) if stats["total_beds"] > 0 else 0
            occupancy_rates.append(occupancy_rate)
        
        return jsonify({
            "cities": cities,
            "total_beds": total_beds,
            "occupied_beds": occupied_beds,
            "icu_beds": icu_beds,
            "hospital_counts": hospital_counts,
            "occupancy_rates": occupancy_rates
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/hospital_analysis')
def hospital_analysis():
    """Get hospital analysis data for scatter charts and tables"""
    try:
        hospitals = []
        cities = []
        total_beds = []
        occupied_beds = []
        icu_beds = []
        occupancy_rates = []
        
        for hospital in hospital_data:
            hospitals.append(hospital["name"])
            cities.append(hospital["city"])
            total_beds.append(hospital["total_beds"])
            occupied_beds.append(hospital["occupied_beds"])
            icu_beds.append(hospital["icu_beds"])
            occupancy_rate = round((hospital["occupied_beds"] * 100.0) / hospital["total_beds"], 2) if hospital["total_beds"] > 0 else 0
            occupancy_rates.append(occupancy_rate)
        
        return jsonify({
            "hospitals": hospitals,
            "cities": cities,
            "total_beds": total_beds,
            "occupied_beds": occupied_beds,
            "icu_beds": icu_beds,
            "occupancy_rates": occupancy_rates
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/timeseries_analysis')
def timeseries_analysis():
    """Alias for timeseries_data - to match your frontend expectations"""
    return timeseries_data()

@app.route('/api/city_analysis') 
def city_analysis():
    """Alias for city_data - to match your frontend expectations"""
    return city_data()

@app.route("/add_hospital", methods=["POST"])
def add_hospital():
    """Add new hospital to the simulated data"""
    if request.method == "POST":
        try:
            hospital_name = request.form["hospital_name"]
            total_beds = int(request.form["total_beds"])
            occupied_beds = int(request.form["occupied_beds"])
            icu_beds = int(request.form["icu_beds"])
            city = request.form.get("city", "Unknown")
            
            # Validate data
            if occupied_beds > total_beds:
                flash("Error: Occupied beds cannot exceed total beds")
                return render_template("add_hospital.html")
            
            # Get current date
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Add to our simulated data
            new_hospital = {
                "name": hospital_name,
                "city": city,
                "total_beds": total_beds,
                "occupied_beds": occupied_beds,
                "icu_beds": icu_beds,
                "date": current_date
            }
            
            hospital_data.append(new_hospital)
            
            flash(f"Hospital '{hospital_name}' added successfully!")
            return redirect("/dashboard")
            
        except Exception as e:
            flash(f"Error: {str(e)}")
            return render_template("add_hospital.html")

@app.route('/api/test_connection')
def test_connection():
    """Test connection - always success for simulated data"""
    return jsonify({
        "status": "success",
        "count": len(hospital_data),
        "error": ""
    })

@app.route('/api/clear_data')
def clear_data():
    """Clear all data and reset to sample (for testing)"""
    global hospital_data
    hospital_data = get_simulated_hospitals()
    return jsonify({"status": "success", "message": "Data reset to sample"})

if __name__ == '__main__':
    print("🚀 Starting Hospital Bed Analysis System (SIMULATED DATA)...")
    print("📊 Access the dashboard at: http://localhost:5000/dashboard")
    print("🏥 Add hospitals at: http://localhost:5000/add_hospital")
    print("🔄 Reset data: http://localhost:5000/api/clear_data")
    print("💡 Using simulated data - no Hive required!")
    app.run(debug=True, host='0.0.0.0', port=5001)