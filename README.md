IoT Temperature Sensor - AWS Home Automation
A complete IoT home automation system that simulates temperature sensors and processes data in real-time using AWS IoT Core.

🌟 Features
Virtual Temperature Sensor: Simulates realistic temperature, humidity, and battery readings
AWS IoT Core Integration: Secure MQTT communication with AWS cloud
Real-time Data Processing: IoT rules for automated data handling
Smart Alerts: Automated alerts when temperature exceeds thresholds
Data Storage: Persistent storage in DynamoDB for historical analysis
Professional Security: TLS certificates and IAM policies
🏗️ Architecture
Virtual Sensor → MQTT → AWS IoT Core → IoT Rules → DynamoDB
                                    ↓
                               CloudWatch Logs
🚀 What This Project Demonstrates
IoT Fundamentals
MQTT protocol implementation
Device-to-cloud communication
Sensor data simulation
Real-time data streaming
AWS Cloud Services
AWS IoT Core: Device management and messaging
DynamoDB: NoSQL database for sensor data
CloudWatch: Logging and monitoring
IAM: Security and access control
Professional Development
Clean code structure
Error handling and reconnection logic
Configuration management
Production-ready security
📊 Data Flow
Sensor Simulation: Virtual sensor generates temperature, humidity, and battery data
Data Publishing: Secure MQTT publishing to AWS IoT Core
Rule Processing: IoT rules process incoming messages
Alert Generation: Automatic alerts for temperature > 25°C
Data Storage: All readings stored in DynamoDB
Monitoring: CloudWatch logs for system monitoring
🛠️ Setup Instructions
Prerequisites
Python 3.7+
AWS Account
AWS CLI configured
Installation
Clone the repository
bash
git clone https://github.com/yourusername/temperature-iot-project.git
cd temperature-iot-project
Install dependencies
bash
pip install -r requirements.txt
AWS IoT Setup
Create an IoT Thing in AWS IoT Console
Download certificates
Create IoT policies
Configure endpoint
Update configuration
Update ENDPOINT in src/temperature_sensor.py
Update certificate paths
Update CLIENT_ID to match your Thing name
Run the sensor
bash
python src/temperature_sensor.py
📁 Project Structure
temperature-iot-project/
├── src/
│   └── temperature_sensor.py    # Main sensor simulation script
├── certificates/
│   ├── device-certificate.pem.crt
│   ├── device-private.pem.key
│   └── AmazonRootCA1.pem
├── docs/
│   └── setup-guide.md           # Detailed setup instructions
├── screenshots/                 # AWS console screenshots
├── README.md
└── requirements.txt
🔧 Configuration
IoT Rules Created
ProcessTemperatureData: Logs temperature alerts > 25°C
StoreAllTemperatureData: Stores all readings in DynamoDB
DynamoDB Table
Table Name: TemperatureReadings
Partition Key: deviceId (String)
Sort Key: timestamp (String)
📈 Sample Data
json
{
  "deviceId": "living_room_temp_sensor",
  "timestamp": "2025-06-23T10:30:45.123Z",
  "temperature": 23.5,
  "humidity": 48.2,
  "batteryLevel": 99.8,
  "location": "living-room"
}
🔐 Security Features
TLS 1.2 Encryption: All data transmission encrypted
X.509 Certificates: Device authentication
IAM Policies: Fine-grained access control
AWS IoT Device Registry: Secure device management
🎯 Use Cases
Smart Home: Temperature monitoring and automation
Industrial IoT: Environmental monitoring in facilities
Agriculture: Greenhouse climate control
Healthcare: Patient room monitoring
Data Centers: Equipment temperature tracking
🔮 Future Enhancements
 Multiple sensor types (motion, light, air quality)
 Mobile app dashboard
 Machine learning predictions
 Device control capabilities
 Real-time notifications (SMS/Email)
 Data visualization dashboard
📊 Monitoring
CloudWatch Integration
Real-time logs in /aws/iot/temperature-alerts
IoT Core metrics and monitoring
Custom dashboards and alarms
Data Storage
Historical data in DynamoDB
Queryable sensor readings
Ready for analytics and reporting
🤝 Contributing
Fork the repository
Create a feature branch
Make your changes
Test thoroughly
Submit a pull request
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

👥 Author
REVATHY UNNIKRISHNA PILLAI

GitHub: @revathyup

🙏 Acknowledgments
AWS IoT Core documentation
Python MQTT client library
AWS SDK for Python (Boto3)
This project demonstrates professional IoT development practices and cloud integration skills suitable for production environments.

