# # import the ML Model 
# import joblib,numpy as np
# model=joblib.load("Hair_fall_Model_lgr.lb")
# # print("Sucessfully Load the Model")
# data=[[101,45,0,1,1,1,0,1,1]]
# output = model.predict(data)
# ouput=output[0].ravel()
# print(output[0])

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import joblib

# Load the trained model (replace with your own model path)
model = joblib.load("Hair_fall_Model_lgr.lb")

# If you used a scaler during training, load it as well (replace with your scaler path)
scaler = joblib.load("scaler_model.pkl")

# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Hair Fall Prediction Dashboard", style={'text-align': 'center'}),
    
    # User input fields for the features
    html.Div([
        html.Label("Age:"),
        dcc.Input(id="age", type="number", placeholder="Enter your age", min=0, style={'margin': '5px'}),
    ], style={'margin': '10px'}),
    
    html.Div([
        html.Label("Stress Level (1-10):"),
        dcc.Input(id="stress_level", type="number", placeholder="Rate your stress level", min=1, max=10, style={'margin': '5px'}),
    ], style={'margin': '10px'}),
    
    html.Div([
        html.Label("Sleep Hours (per day):"),
        dcc.Input(id="sleep_hours", type="number", placeholder="Enter your sleep hours", min=0, style={'margin': '5px'}),
    ], style={'margin': '10px'}),
    
    html.Div([
        html.Label("Diet Quality (1-10):"),
        dcc.Input(id="diet_quality", type="number", placeholder="Rate your diet quality", min=1, max=10, style={'margin': '5px'}),
    ], style={'margin': '10px'}),
    
    html.Button("Predict", id="predict-button", n_clicks=0, style={'padding': '10px 20px', 'margin-top': '20px'}),
    
    # Area to show prediction result
    html.H2(id="prediction-output", style={'text-align': 'center', 'margin-top': '30px'})
])

# Define the callback to update the prediction output
@app.callback(
    Output("prediction-output", "children"),
    [Input("age", "value"),
     Input("stress_level", "value"),
     Input("sleep_hours", "value"),
     Input("diet_quality", "value"),
     Input("predict-button", "n_clicks")]
)
def predict_hair_fall(age, stress_level, sleep_hours, diet_quality, n_clicks):
    # Check if the "Predict" button is clicked
    if n_clicks == 0:
        return ""
    
    # Check if all inputs are provided
    if not age or not stress_level or not sleep_hours or not diet_quality:
        return "Please fill all fields."

    # Convert inputs to a numpy array (matching model input format)
    input_data = np.array([[age, stress_level, sleep_hours, diet_quality]])

    # Scale the input data (if scaling was done during training)
    input_data_scaled = scaler.transform(input_data)
    
    # Predict using the logistic regression model
    prediction = model.predict(input_data_scaled)
    
    # Return the prediction result
    if prediction == 1:
        return "Yes, you may experience hair fall."
    else:
        return "No, you may not experience hair fall."

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
