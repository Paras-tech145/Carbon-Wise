import os
import pandas as pd
import streamlit as st

# Define emission factors (example values, replace with accurate data)
EMISSION_FACTORS = {
    "India": {
        "Public Transportation": 1.3,  # kgCO2/km
        "Electricity": 0.82,  # kgCO2/kWh
        "Diet": 1.25,  # kgCO2/meal, 2.5kgco2/kg
        "Waste": 0.1,  # kgCO2/kg
        "Plane": 90,  # kgCO2/h
        "Petrol car": 0.20,  # kgCO2/km
        "Diesel car": 0.12,  # kgCO2/km
        "CNG car": 0.063,  # kgCO2/km
        "Electric car": 0.06,  # kgCO2/km
        "Petrol bike": 0.07,  # kgCO2/km
        "Diesel bike": 0.11,  # kgCO2/km
        "Electric bike": 0.09,  # kgCO2/km
    }
}

# Set wide layout and page name
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

# Initialize or load session state
if 'results' not in st.session_state:
    st.session_state.results = []

# Function to save session state data to file
def save_session_state():
    data = pd.DataFrame({
        'Month': [f'Month {i+1}' for i in range(len(st.session_state.results))],
        'CO2 Emissions (tonnes)': st.session_state.results
    })
    data.to_csv('results.csv', index=False)

# Function to load session state data from file
def load_session_state():
    try:
        df = pd.read_csv('results.csv')
        st.session_state.results = df['CO2 Emissions (tonnes)'].tolist()
    except FileNotFoundError:
        st.session_state.results = []

# Function to clear all data
def clear_data():
    if os.path.exists('results.csv'):
        os.remove('results.csv')
    st.session_state.results = []

# Load session state data at the start
load_session_state()

# Streamlit app code
st.title("Carbon Wise - Carbon Footprint Calculator")

# Clear All Data Button
if st.button("Clear All Data", on_click=clear_data):
    st.info("All previous data has been deleted.")

# Show Progress Button
if st.button("Show Progress"):
    st.subheader("Your CO2 Emissions Progress")
    if st.session_state.results:
        df = pd.DataFrame({
            'Month': [f'Month {i+1}' for i in range(len(st.session_state.results))],
            'CO2 Emissions (tonnes)': st.session_state.results
        })
        df.set_index('Month', inplace=True)
        st.line_chart(df)
    else:
        st.info("No data available. Please calculate your CO2 emissions first.")

# User inputs
st.subheader("Your Country")
country = st.selectbox("Select", ["India"])

col1, col2 = st.columns(2)
with col1:
    st.subheader("Daily commute distance by Public transportation (in km)")
    pubdistance = st.number_input("Distance by public Transport", 0.0, key="pubdistance_input")
    st.subheader("Monthly electricity consumption (in kWh)")
    electricity = st.number_input("Electricity", 0.0, key="electricity_input")
    st.subheader("Annual travel by airplane (in hours)")
    plane = st.number_input("Flight", 0, key="plane_input")
    st.subheader("Weekly commute distance by Self Car (Fill this if it is CNG)(in km)")
    carcng = st.number_input("CNG Car", 0, key="cng_input")
    st.subheader("Weekly commute distance by Self Car (Fill this if it is Electric)(in km)")
    carelectric = st.number_input("Electric Car", 0, key="electric_input")
    st.subheader("️ Weekly commute distance by Self Bike (Fill this if it is Diesel)(in km)")
    bikediesel = st.number_input("Diesel Bike", 0, key="bdiesel_input")
with col2:
    st.subheader("️Waste generated per week (in kg)")
    waste = st.number_input("Waste", 0.0, key="waste_input")
    st.subheader("️Number of meals per day")
    meals = st.number_input("Meals", 0, key="meals_input")
    st.subheader("Weekly commute distance by Self Car (Fill this if it is Petrol)(in km)")
    carpetrol = st.number_input("Petrol Car", 0, key="petrol_input")
    st.subheader("Weekly commute distance by Self Car (Fill this if it is Diesel)(in km)")
    cardiesel = st.number_input("Diesel Car", 0, key="diesel_input")
    st.subheader("️Weekly commute distance by Self Bike (Fill this if it is Petrol)(in km)")
    bikepetrol = st.number_input("Petrol Bike", 0, key="bpetrol_input")
    st.subheader("️Weekly commute distance by Self Bike (Fill this if it is Electric)(in km)")
    bikeelectric = st.number_input("Electric Bike", 0, key="belectric_input")

# Normalize inputs
if pubdistance > 0:
    pubdistance = pubdistance * 30  # Convert daily distance to monthly
if electricity > 0:
    electricity = electricity * 1  # Convert monthly electricity to monthly
if meals > 0:
    meals = meals * 30  # Convert daily meals to monthly
if waste > 0:
    waste = waste * 4  # Convert weekly waste to monthly
if plane > 0:
    plane = plane / 12  # already monthly
if carpetrol > 0:
    carpetrol = carpetrol * 4  # Convert weekly distance to monthly
if cardiesel > 0:
    cardiesel = cardiesel * 4  # Convert weekly distance to monthly
if carcng > 0:
    carcng = carcng * 4  # Convert weekly distance to monthly
if carelectric > 0:
    carelectric = carelectric * 4  # Convert weekly distance to monthly
if bikepetrol > 0:
    bikepetrol = bikepetrol * 4  # Convert weekly distance to monthly
if bikediesel > 0:
    bikediesel = bikediesel * 4  # Convert weekly distance to monthly
if bikeelectric > 0:
    bikeelectric = bikeelectric * 4  # Convert weekly distance to monthly

# Calculate carbon emissions
pubtransportation_emissions = EMISSION_FACTORS[country]["Public Transportation"] * pubdistance
electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity
diet_emissions = EMISSION_FACTORS[country]["Diet"] * meals
waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste
plane_emissions = EMISSION_FACTORS[country]["Plane"] * plane
petrol_emissions = EMISSION_FACTORS[country]["Petrol car"] * carpetrol
diesel_emissions = EMISSION_FACTORS[country]["Diesel car"] * cardiesel
cng_emissions = EMISSION_FACTORS[country]["CNG car"] * carcng
electric_emissions = EMISSION_FACTORS[country]["Electric car"] * carelectric
petrolbike_emissions = EMISSION_FACTORS[country]["Petrol bike"] * bikepetrol
dieselbike_emissions = EMISSION_FACTORS[country]["Diesel bike"] * bikediesel
electricbike_emissions = EMISSION_FACTORS[country]["Electric bike"] * bikeelectric

# Convert emissions to tonnes and round off to 2 decimal points
pubtransportation_emissions = round(pubtransportation_emissions / 1000, 2)
electricity_emissions = round(electricity_emissions / 1000, 2)
diet_emissions = round(diet_emissions / 1000, 2)
waste_emissions = round(waste_emissions / 1000, 2)
plane_emissions = round(plane_emissions / 1000, 2)
petrol_emissions = round(petrol_emissions / 1000, 2)
diesel_emissions = round(diesel_emissions / 1000, 2)
cng_emissions = round(cng_emissions / 1000, 2)
electric_emissions = round(electric_emissions / 1000, 2)
petrolbike_emissions = round(petrolbike_emissions / 1000, 2)
dieselbike_emissions = round(dieselbike_emissions / 1000, 2)
electricbike_emissions = round(electricbike_emissions / 1000, 2)

# Calculate total emissions
total_emissions = round(
    pubtransportation_emissions + electricity_emissions + diet_emissions + waste_emissions + plane_emissions + petrol_emissions + diesel_emissions + cng_emissions + electric_emissions + petrolbike_emissions + dieselbike_emissions + electricbike_emissions, 2
)

# Calculate total emissions by car
car_emissions = round(
    petrol_emissions + diesel_emissions + cng_emissions + electric_emissions, 2
)

# Calculate total emissions by bike
bike_emissions = round(
    petrolbike_emissions + dieselbike_emissions + electricbike_emissions, 2
)

if 'show_results' not in st.session_state:
    st.session_state.show_results = False

if 'show_tips' not in st.session_state:
    st.session_state.show_tips = False

def calculate_emissions():
    st.session_state.show_results = True
    st.session_state.results.append(total_emissions)
    save_session_state()  # Save to persistent storage

def show_tips():
    st.session_state.show_tips = True

# Calculate emissions button
if st.button("Calculate CO2 Emissions", on_click=calculate_emissions):
    st.session_state.show_results = True

# Display results
if st.session_state.show_results:
    st.header("Results")
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Carbon Emissions by Category")
        st.info(f"Public Transportation: {pubtransportation_emissions} tonnes CO2 per month")
        st.info(f"Electricity: {electricity_emissions} tonnes CO2 per month")
        st.info(f"️Diet: {diet_emissions} tonnes CO2 per month")
        st.info(f"Waste: {waste_emissions} tonnes CO2 per month")
        st.info(f"Flight: {plane_emissions} tonnes CO2 per month")
        st.info(f"Personal Car: {car_emissions} tonnes CO2 per month")
        st.info(f"Personal Bike: {bike_emissions} tonnes CO2 per month")

    with col4:
        st.subheader("Total Carbon Footprint")
        st.success(f" Your total carbon footprint is: {total_emissions} tonnes CO2 per month")
        st.warning("In 2021, CO2 emissions per capita for India was 1.9 tons of CO2 per capita. Between 1972 and 2021, CO2 emissions per capita of India grew substantially from 0.39 to 1.9 tons of CO2 per capita rising at an increasing annual rate that reached a maximum of 9.41% in 2021.")

        # Show Get Tips button after calculating emissions
        st.button("Get Tips", on_click=show_tips)

if st.session_state.show_tips:
    st.header("Tips")
    col5, col6 = st.columns(2)
    with col5:
        if electricity_emissions > 1.0:
            st.subheader("Tips for reducing Electricity Emissions")
            st.info(f"Use LED bulbs instead of incandescent or CFL bulbs (saves up to 75% energy).")
            st.info(f"Unplug devices when not in use or use smart power strips to prevent phantom energy usage.")
            st.info(f"Opt for a green energy plan from your electricity provider if available, which uses wind, solar, or hydropower.")
            st.info(f"Use fans and natural ventilation whenever possible instead of air conditioning.")
            st.info(f"Power down computers and devices when not in use or put them in energy-saving mode.")
            st.info(f"Reduce screen brightness on monitors and TVs, as brighter settings consume more power.")
            st.info(f"Use natural sunlight during the day instead of electric lighting, by keeping windows open.")
        if waste_emissions > 0.5:
            st.subheader("Tips for reducing Waste Emissions")
            st.info(f"Minimize food waste by planning meals and using leftovers.")
            st.info(f"Participate in local recycling programs and ensure you follow proper sorting guidelines.")
            st.info(f"Use reusable bags, bottles, and containers instead of disposable ones.")
            st.info(f"Educate others about the importance of waste segregation to enhance community efforts.")
            st.info(f"Repurpose items instead of discarding them (e.g., upcycling old clothes or furniture).")
            st.info(f"Donate usable items (e.g., clothes, electronics, furniture) to reduce overall waste generation.")
    with col6:
        if car_emissions > 1.0:
            st.subheader("Tips for reducing Emissions from Cars")
            st.info(f"Sharing your car with others significantly reduces emissions per person. Consider carpooling for daily commutes or trips.")
            st.info(f"Hybrid cars use both fuel and electricity, cutting emissions. Electric vehicles (EVs), especially when powered by renewable energy, can reduce emissions to near zero.")
            st.info(f"Practice eco-driving: avoid sudden acceleration, maintain a steady speed, and minimize idling. This can improve fuel efficiency by up to 30%, cutting down on emissions.")
            st.info(f"Combine errands into a single trip, use public transport where possible, or walk/bike short distances. Fewer trips mean less fuel consumption.")
            st.info(f"Regularly service your car (e.g., tune-ups, oil changes, and tire pressure checks) to ensure it runs efficiently, reducing fuel consumption and emissions.")
        if bike_emissions > 1.0:
            st.subheader("Tips for reducing Emissions from Bikes")
            st.info(f"Opt for buses, trains, or cycling for shorter journeys, and use your motorbike for longer distances or areas with poor public transport.")
            st.info(f"Consider switching to an electric motorbike (e-bike) to significantly lower emissions, especially if you charge it using renewable energy.")
            st.info(f"Plan your routes to avoid heavy traffic and minimize stop-start driving. Taking more direct routes will save fuel and lower emissions.")
            st.info(f"Avoid high-speed driving and aggressive acceleration. Keeping your speed moderate and steady can increase fuel efficiency and lower emissions.")
            st.info(f"Keep your motorbike well-maintained by regularly checking the engine, tires, and exhaust system. A well-maintained bike runs more efficiently, reducing emissions.")
