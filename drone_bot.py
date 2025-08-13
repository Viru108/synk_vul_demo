import streamlit as st
import requests
import plotly.graph_objects as go
import numpy as np

# --- Drone Recommendation Logic ---
def suggest_frame(mission_type, payload_weight_grams):
    if mission_type == "Delivery" and payload_weight_grams > 1000:
        return "Large Multirotor Frame (e.g., 700mm+)"
    elif payload_weight_grams > 500:
        return "Medium Multirotor Frame (e.g., 500-650mm)"
    else:
        return "Small Multirotor Frame (e.g., 300-450mm)"

def suggest_motors(frame_size_mm, payload_weight_grams):
    if frame_size_mm > 600 and payload_weight_grams > 1000:
        return "High-power motors (e.g., 3508 or larger)"
    elif frame_size_mm > 450 and payload_weight_grams > 500:
        return "Mid-range motors (e.g., 2212 to 3110)"
    else:
        return "Small to medium motors (e.g., 1806 to 2208)"

def suggest_propellers(frame_size_mm):
    if frame_size_mm > 600:
        return "Large propellers (e.g., 15-18 inches)"
    elif frame_size_mm > 450:
        return "Medium propellers (e.g., 10-14 inches)"
    else:
        return "Small propellers (e.g., 5-9 inches)"

def suggest_battery(desired_flight_time_minutes, payload_weight_grams):
    capacity = (desired_flight_time_minutes * (payload_weight_grams + 500)) * 2
    return f"{int(capacity)} mAh 11.1V LiPo"

# --- Drone 3D Visual Generator ---
def draw_drone_3d(frame_size_mm, propeller_diameter_inches):
    arm_length = min(40.0, float(frame_size_mm) / 20.0)
    prop_radius = float(propeller_diameter_inches) / 2.0

    fig = go.Figure()

    # Draw arms and propellers
    for angle_deg in [0, 90, 180, 270]:
        angle_rad = np.radians(angle_deg)
        x_end = arm_length * np.cos(angle_rad)
        y_end = arm_length * np.sin(angle_rad)

        # Draw arm
        fig.add_trace(go.Scatter3d(
            x=[0, x_end],
            y=[0, y_end],
            z=[0, 0],
            mode='lines',
            line=dict(color='gray', width=10),
            name='Arm'
        ))

        # Draw propeller
        theta = np.linspace(0, 2 * np.pi, 100)
        px = x_end + prop_radius * np.cos(theta)
        py = y_end + prop_radius * np.sin(theta)
        pz = np.zeros_like(px)

        fig.add_trace(go.Scatter3d(
            x=px,
            y=py,
            z=pz,
            mode='lines',
            line=dict(color='black', width=3),
            name='Propeller'
        ))

    # Draw central body
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=15, color='red'),
        name='Body'
    ))

    # Forward direction
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, arm_length * 1.2], z=[0, 0],
        mode='lines',
        line=dict(color='blue', width=4, dash='dot'),
        name='Front'
    ))

    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data'
        )
    )

    st.plotly_chart(fig)

# --- Streamlit UI ---
st.title("Drone Design Assistant")

st.write("Answer a few questions and get recommendations for building your drone:")

mission_type = st.selectbox("Mission Type:", ["Recreational", "Photography/Videography", "Delivery", "Inspection", "Other"])
payload_weight_grams = st.number_input("Payload Weight (grams):", min_value=0, value=0)
desired_flight_time_minutes = st.number_input("Desired Flight Time (minutes):", min_value=0, value=0)
frame_size_mm = st.number_input("Frame Size (in mm):", min_value=0, value=0)
propeller_diameter_inches = st.number_input("Propeller Diameter (inches):", min_value=0.0, value=0.0, step=0.1)

if st.button("Get Drone Design Recommendation"):
    st.subheader("Recommendations")

    frame = suggest_frame(mission_type, payload_weight_grams)
    motors = suggest_motors(frame_size_mm, payload_weight_grams)
    propellers = suggest_propellers(frame_size_mm)
    battery = suggest_battery(desired_flight_time_minutes, payload_weight_grams)

    st.write(f"**Frame:** {frame}")
    st.write(f"**Motors:** {motors}")
    st.write(f"**Propellers:** {propellers}")
    st.write(f"**Battery:** {battery}")

    st.subheader("Drone 3D Visualization")
    draw_drone_3d(frame_size_mm, propeller_diameter_inches)

    st.markdown("<br><br>**Note:** This is a simplified visual and estimation. Actual drone builds should consider detailed thrust-to-weight ratios, component compatibility, and real-world testing.", unsafe_allow_html=True)