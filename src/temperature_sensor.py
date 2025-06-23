#!/usr/bin/env python3

import json
import time
import random
from datetime import datetime
from awsiot import mqtt_connection_builder
from awscrt import io, mqtt
import threading

# =============================================================================
# AWS IoT Configuration - UPDATE THESE VALUES
# =============================================================================

# Replace with YOUR actual endpoint from AWS IoT Console → Settings
ENDPOINT = "a38j1yxtgtu8ch-ats.iot.eu-north-1.amazonaws.com"

# Replace with your actual certificate file paths
CERT_FILEPATH = "./certificates/device-certificate.pem.crt"
PRIVATE_KEY_FILEPATH = "./certificates/device-private.pem.key"
CA_FILEPATH = "./certificates/AmazonRootCA1.pem"

# MQTT Settings - UPDATE THIS TO MATCH YOUR THING NAME
CLIENT_ID = "living_room_temp_sensor"  # Updated to match your actual Thing name
TOPIC = "home/living-room/temperature/telemetry"

# =============================================================================
# Temperature Sensor Simulation
# =============================================================================

class VirtualTemperatureSensor:
    def __init__(self):
        self.base_temp = 22.0  # Base temperature in Celsius
        self.base_humidity = 45.0  # Base humidity percentage
        self.battery_level = 100.0
        
    def read_temperature(self):
        # Simulate realistic temperature variations
       # variation = random.uniform(-2.0, 3.0)
        variation = random.uniform(3.0, 8.0)

        return round(self.base_temp + variation, 1)
    
    def read_humidity(self):
        # Simulate humidity variations
        variation = random.uniform(-5.0, 10.0)
        return round(max(20.0, min(80.0, self.base_humidity + variation)), 1)
    
    def read_battery(self):
        # Simulate slow battery drain
        self.battery_level = max(0.0, self.battery_level - random.uniform(0.01, 0.05))
        return round(self.battery_level, 1)

# =============================================================================
# MQTT Connection and Publishing
# =============================================================================

def create_sensor_data(sensor):
    """Create a JSON payload with sensor readings"""
    return {
        "deviceId": CLIENT_ID,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "temperature": sensor.read_temperature(),
        "humidity": sensor.read_humidity(),
        "batteryLevel": sensor.read_battery(),
        "location": "living-room"
    }

def on_connection_interrupted(connection, error, **kwargs):
    print(f"❌ Connection interrupted. Error: {error}")

def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print(f"✅ Connection resumed. Return code: {return_code}, Session present: {session_present}")

def on_publish_complete(future):
    """Called when a publish operation completes"""
    try:
        future.result()  # This will raise an exception if the publish failed
        print("📡 Message published successfully!")
    except Exception as e:
        print(f"❌ Publish failed: {e}")

def main():
    print("🌡️  Virtual Temperature Sensor Starting...")
    
    # Initialize the sensor
    sensor = VirtualTemperatureSensor()
    
    # Create event loop for the connection
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    
    print("🔄 Connecting to AWS IoT Core...")
    
    # Create MQTT connection
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=CERT_FILEPATH,
        pri_key_filepath=PRIVATE_KEY_FILEPATH,
        client_bootstrap=client_bootstrap,
        ca_filepath=CA_FILEPATH,
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=30,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed
    )
    
    # Connect to AWS IoT
    try:
        connect_future = mqtt_connection.connect()
        connect_future.result()  # Wait for connection to complete
        print("✅ Connected to AWS IoT Core!")
        print(f"📡 Publishing to topic: {TOPIC}")
        print("🔄 Press Ctrl+C to stop...\n")
        
        # Main publishing loop
        message_count = 0
        while True:
            try:
                # Generate sensor data
                sensor_data = create_sensor_data(sensor)
                message_json = json.dumps(sensor_data, indent=2)
                
                # Publish the message
                publish_future = mqtt_connection.publish(
                    topic=TOPIC,
                    payload=message_json,
                    qos=mqtt.QoS.AT_LEAST_ONCE
                )
                
                # Print the data being sent
                message_count += 1
                print(f"📊 Message #{message_count}:")
                print(f"   🌡️  Temperature: {sensor_data['temperature']}°C")
                print(f"   💧 Humidity: {sensor_data['humidity']}%")
                print(f"   🔋 Battery: {sensor_data['batteryLevel']}%")
                print(f"   📅 Time: {sensor_data['timestamp']}")
                print("-" * 50)
                
                # Wait before next reading
                time.sleep(5)  # Send data every 5 seconds
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping sensor...")
                break
            except Exception as e:
                print(f"❌ Error publishing data: {e}")
                time.sleep(1)
                
    except Exception as e:
        print(f"❌ Failed to connect to AWS IoT: {e}")
        print("\n🔍 Troubleshooting tips:")
        print("   1. Check your ENDPOINT URL")
        print("   2. Verify certificate file paths")
        print("   3. Ensure your Thing policy allows publishing")
        return
    
    finally:
        # Disconnect
        print("🔌 Disconnecting...")
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        print("👋 Disconnected successfully!")

if __name__ == "__main__":
    main()
