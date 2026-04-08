import pandas as pd
import random

# 1. Start with the Kaggle Style columns
data = {
    'CustomerID': ['KAVYA-001', 'MOHIT-002', 'FRIEND-003'],
    'Name': ['Kavya S', 'Mohit Kumar', 'Sneha Reddy'],
    'Age': [21, 24, 22],
    'Gender': ['Female', 'Male', 'Female'],
    'Phone': ['+91 9876543210', '+91 8888877777', '+91 9999900000'],
    'Email': ['kavya@email.com', 'mohit@email.com', 'sneha@email.com'],
    'MonthlyCharges': [95.0, 45.0, 110.0], # 95 and 110 will trigger "High Risk"
    'Tenure': [5, 24, 2],
    'PaymentMethod': ['Electronic check', 'Credit card', 'Bank transfer']
}

df = pd.DataFrame(data)

# 2. Save it as your "Satisfaction" file
df.to_csv('real_world_test.csv', index=False)
print("✅ Real-world test data created! Upload 'real_world_test.csv' in your app.")