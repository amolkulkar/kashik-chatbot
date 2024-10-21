from flask import Flask, request, jsonify, render_template
import pandas as pd

# Configuration
FILE_PATH = 'data.csv'

# Load dataset
def load_dataset(file_path):
    """Load dataset from CSV file"""
    dataset_df = pd.read_csv(file_path)
    return dataset_df

# Process dataset
def process_dataset(dataset_df):
    """Process dataset to extract input/output pairs"""
    input_columns = [col for col in dataset_df.columns if col.startswith('Input')]
    output_columns = [col for col in dataset_df.columns if col.startswith('Output')]
    dataset = []
    for index, row in dataset_df.iterrows():
        for input_col, output_col in zip(input_columns, output_columns):
            if pd.notna(row[input_col]) and pd.notna(row[output_col]):
                dataset.append({'input': str(row[input_col]), 'output': str(row[output_col])})
    return dataset

# Get response
def get_response(user_input):
    """Get response for user input"""
    dataset = process_dataset(load_dataset(FILE_PATH))
    for pair in dataset:
        if pair['input'].lower() == user_input.lower():
            return pair['output']
    return "I'm sorry, I don't understand that."

# Create Flask app
app = Flask(__name__, template_folder='templates')

# Define routes
@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/chatbot', methods=['POST'])
def interact():
    try:
        user_input = request.form.get('Statement')
        response = get_response(user_input)
        print(user_input)
        print(response)
        return jsonify({'result': response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
