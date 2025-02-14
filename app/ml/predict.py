import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
CSV_FILE = "data_source/weather_data.csv"
MODEL_FILE = "data_source/rainfall_model.pkl"

# Ensure directory exists
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

def train_model():
    """Train the logistic regression model to predict rainfall."""
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print("No historical weather data found for training.")
        return None

    # Load dataset
    df = pd.read_csv(CSV_FILE)

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Define features and target
    X = df[["temperature", "humidity", "pressure", "wind_speed"]]
    y = (df["rainfall"] > 0).astype(int)  # Convert rainfall to binary (0 = No rain, 1 = Rain)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Training Complete! Accuracy: {accuracy:.2f}")

    # Save model and scaler
    with open(MODEL_FILE, "wb") as f:
        pickle.dump((scaler, model), f)

def load_model():
    """Load the trained model and scaler."""
    if not os.path.exists(MODEL_FILE):
        print("Model not found. Train the model first.")
        return None, None

    with open(MODEL_FILE, "rb") as f:
        scaler, model = pickle.load(f)
    return scaler, model

def predict_rainfall(temp, humidity, pressure, wind_speed):
    """Predict whether it will rain based on input features."""
    scaler, model = load_model()

    if model is None:
        print("Error: Model not trained!")
        return False

    # Preprocess input data
    features = [[temp, humidity, pressure, wind_speed]]
    features_scaled = scaler.transform(features)

    # Make prediction
    prediction = model.predict(features_scaled)
    return bool(prediction[0])  # Convert to boolean (True = Rain, False = No rain)

# Train model when script runs (Optional: Remove if you want manual training)
if __name__ == "__main__":
    train_model()
import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
CSV_FILE = "data_source/weather_data.csv"
MODEL_FILE = "data_source/rainfall_model.pkl"

# Ensure directory exists
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

def train_model():
    """Train the logistic regression model to predict rainfall."""
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print("No historical weather data found for training.")
        return None

    # Load dataset
    df = pd.read_csv(CSV_FILE)

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Define features and target
    X = df[["temperature", "humidity", "pressure", "wind_speed"]]
    y = (df["rainfall"] > 0).astype(int)  # Convert rainfall to binary (0 = No rain, 1 = Rain)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Training Complete! Accuracy: {accuracy:.2f}")

    # Save model and scaler
    with open(MODEL_FILE, "wb") as f:
        pickle.dump((scaler, model), f)

def load_model():
    """Load the trained model and scaler."""
    if not os.path.exists(MODEL_FILE):
        print("Model not found. Train the model first.")
        return None, None

    with open(MODEL_FILE, "rb") as f:
        scaler, model = pickle.load(f)
    return scaler, model

def predict_rainfall(temp, humidity, pressure, wind_speed):
    """Predict whether it will rain based on input features."""
    scaler, model = load_model()

    if model is None:
        print("Error: Model not trained!")
        return False

    # Preprocess input data
    features = [[temp, humidity, pressure, wind_speed]]
    features_scaled = scaler.transform(features)

    # Make prediction
    prediction = model.predict(features_scaled)
    return bool(prediction[0])  # Convert to boolean (True = Rain, False = No rain)

# Train model when script runs (Optional: Remove if you want manual training)
if __name__ == "__main__":
    train_model()
import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
CSV_FILE = "data_source/weather_data.csv"
MODEL_FILE = "data_source/rainfall_model.pkl"

# Ensure directory exists
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

def train_model():
    """Train the logistic regression model to predict rainfall."""
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print("No historical weather data found for training.")
        return None

    # Load dataset
    df = pd.read_csv(CSV_FILE)

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Define features and target
    X = df[["temperature", "humidity", "pressure", "wind_speed"]]
    y = (df["rainfall"] > 0).astype(int)  # Convert rainfall to binary (0 = No rain, 1 = Rain)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Training Complete! Accuracy: {accuracy:.2f}")

    # Save model and scaler
    with open(MODEL_FILE, "wb") as f:
        pickle.dump((scaler, model), f)

def load_model():
    """Load the trained model and scaler."""
    if not os.path.exists(MODEL_FILE):
        print("Model not found. Train the model first.")
        return None, None

    with open(MODEL_FILE, "rb") as f:
        scaler, model = pickle.load(f)
    return scaler, model

def predict_rainfall(temp, humidity, pressure, wind_speed):
    """Predict whether it will rain based on input features."""
    scaler, model = load_model()

    if model is None:
        print("Error: Model not trained!")
        return False

    # Preprocess input data
    features = [[temp, humidity, pressure, wind_speed]]
    features_scaled = scaler.transform(features)

    # Make prediction
    prediction = model.predict(features_scaled)
    return bool(prediction[0])  # Convert to boolean (True = Rain, False = No rain)

# Train model when script runs (Optional: Remove if you want manual training)
if __name__ == "__main__":
    train_model()
import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
CSV_FILE = "data_source/weather_data.csv"
MODEL_FILE = "data_source/rainfall_model.pkl"

# Ensure directory exists
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

def train_model():
    """Train the logistic regression model to predict rainfall."""
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print("No historical weather data found for training.")
        return None

    # Load dataset
    df = pd.read_csv(CSV_FILE)

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Define features and target
    X = df[["temperature", "humidity", "pressure", "wind_speed"]]
    y = (df["rainfall"] > 0).astype(int)  # Convert rainfall to binary (0 = No rain, 1 = Rain)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Training Complete! Accuracy: {accuracy:.2f}")

    # Save model and scaler
    with open(MODEL_FILE, "wb") as f:
        pickle.dump((scaler, model), f)

def load_model():
    """Load the trained model and scaler."""
    if not os.path.exists(MODEL_FILE):
        print("Model not found. Train the model first.")
        return None, None

    with open(MODEL_FILE, "rb") as f:
        scaler, model = pickle.load(f)
    return scaler, model

def predict_rainfall(temp, humidity, pressure, wind_speed):
    """Predict whether it will rain based on input features."""
    scaler, model = load_model()

    if model is None:
        print("Error: Model not trained!")
        return False

    # Preprocess input data
    features = [[temp, humidity, pressure, wind_speed]]
    features_scaled = scaler.transform(features)

    # Make prediction
    prediction = model.predict(features_scaled)
    return bool(prediction[0])  # Convert to boolean (True = Rain, False = No rain)

# Train model when script runs (Optional: Remove if you want manual training)
if __name__ == "__main__":
    train_model()
