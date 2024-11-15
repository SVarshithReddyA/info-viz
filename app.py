import os, datetime
import random
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time
import json
from datetime import datetime
import csv

app = Flask(__name__)
app.secret_key = os.urandom(24)

app = Flask(__name__)
app.secret_key = os.urandom(24)

QUESTIONS = [
    {
        "id": "highest_absences_march",
        "text": "Which school had the highest number of absences in March?",
        "options": [f"School {i}" for i in range(1, 11)]
    },
    {
        "id": "lowest_absences_school_7",
        "text": "During which month did School 7 have the lowest number of absences?",
        "options": ['September', 'October', 'November', 'December', 'January', 
                   'February', 'March', 'April', 'May', 'June', 'July', 'August']
    },
    {
        "id": "highest_absences_december",
        "text": "In which school were absences the highest in December?",
        "options": [f"School {i}" for i in range(1, 11)]
    },
    {
        "id": "increase_april_may",
        "text": "Which school showed a noticeable increase in absences between April and May?",
        "options": [f"School {i}" for i in range(1, 11)]
    },
    {
        "id": "highest_total_absences_month",
        "text": "Which month had the highest total absences across all schools?",
        "options": ['September', 'October', 'November', 'December', 'January', 
                   'February', 'March', 'April', 'May', 'June', 'July', 'August']
    },
    {
        "id": "peak_month_school_3",
        "text": "For School 3, in which month were absences at their peak?",
        "options": ['September', 'October', 'November', 'December', 'January', 
                   'February', 'March', 'April', 'May', 'June', 'July', 'August']
    },
    {
        "id": "more_absences_jan_oct_school_5",
        "text": "Did School 5 have more absences in January or in October?",
        "options": ['January', 'October']
    },
    {
        "id": "fewest_absences_july",
        "text": "Which school had the fewest absences in July?",
        "options": [f"School {i}" for i in range(1, 11)]
    },
    {
        "id": "school_10_diff",
        "text": "During which month did School 10 see the greatest decline in absences compared to the previous month?",
        "options": ['September', 'October', 'November', 'December', 'January', 
                   'February', 'March', 'April', 'May', 'June', 'July', 'August']
    },
    {
        "id": "consistent_high_absences",
        "text": "Which school had consistently high absences from September to November?",
        "options": [f"School {i}" for i in range(1, 11)]
    }
]

def generate_heatmap_and_answers():
    num_schools = 10
    num_months = 12
    data = {
        'School ID': np.random.choice(range(1, num_schools + 1), size=num_schools * num_months),
        'Month': np.tile(['September', 'October', 'November', 'December', 'January', 'February', 
                          'March', 'April', 'May', 'June', 'July', 'August'], num_schools),
        'Number of Students Absent': np.random.randint(1, 76, size=num_schools * num_months)
    }
    df = pd.DataFrame(data)
    aggregated_data = df.groupby(['School ID', 'Month'], as_index=False).sum()

    school_order = list(range(1, num_schools + 1))
    month_order = ['September', 'October', 'November', 'December', 'January', 
                   'February', 'March', 'April', 'May', 'June', 'July', 'August']

    heatmap_data = aggregated_data.pivot(index='Month', columns='School ID', values='Number of Students Absent').fillna(0)
    heatmap_data = heatmap_data.reindex(month_order)
    heatmap_data = heatmap_data[school_order]

    answers = {
        "highest_absences_march": int(heatmap_data.loc['March'].idxmax()),
        "lowest_absences_school_7": str(heatmap_data[7].idxmin()),
        "highest_absences_december": int(heatmap_data.loc['December'].idxmax()),
        "increase_april_may": int((heatmap_data.loc['May'] - heatmap_data.loc['April']).idxmax()),
        "highest_total_absences_month": str(heatmap_data.sum(axis=1).idxmax()),
        "peak_month_school_3": str(heatmap_data[3].idxmax()),
        "more_absences_jan_oct_school_5": 'January' if heatmap_data.loc['January', 5] > heatmap_data.loc['October', 5] else 'October',
        "fewest_absences_july": int(heatmap_data.loc['July'].idxmin()),
        "school_10_diff": str(heatmap_data[10].diff().idxmin()),
        "consistent_high_absences": int(heatmap_data.loc['September':'November'].mean().idxmax())
    }

    return heatmap_data, answers

def plot_scatter(df):
    plt.figure(figsize=(14, 8))
    for school_id in df['School ID'].unique():
        school_data = df[df['School ID'] == school_id]
        plt.scatter(school_data['Month'], school_data['Number of Students Absent'], label=f'School {school_id}', alpha=0.7)

    plt.title('Scatter Plot of Student Absences Across Schools and Months')
    plt.xlabel('Month')
    plt.ylabel('Number of Students Absent')
    plt.xticks(rotation=45)
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plot_filename = 'scatterplot.png'
    plt.savefig(os.path.join('static', plot_filename))
    plt.close()
    return plot_filename
def print_session_info(question_number, answers):
    print("\n" + "="*50)
    print(f"Question Number: {question_number}")
    print("Current answers for this question:")
    for q in QUESTIONS:
        q_id = q['id']
        print(f"{q['text']}: {answers[q_id]}")
    print("="*50 + "\n")
def create_csv_files():
    """Create new CSV files with unique session ID"""
    session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    session['session_id'] = session_id
    log_dir = 'session_logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Main responses CSV file
    responses_file = os.path.join(log_dir, f'session_{session_id}_responses.csv')
    session['responses_file'] = responses_file
    
    response_headers = [
        'question_number',
        'visualization_type',
        'question_text',
        'user_answer',
        'correct_answer',
        'is_correct',
        'response_time_seconds'
    ]
    
    with open(responses_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(response_headers)
    
    # Time metrics CSV file
    times_file = os.path.join(log_dir, f'session_{session_id}_times.csv')
    session['times_file'] = times_file
    
    time_headers = [
        'total_experiment_time',
        'total_heatmap_time',
        'total_scatter_time',
        'average_heatmap_response_time',
        'average_scatter_response_time'
    ]
    
    with open(times_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(time_headers)
    
    return responses_file, times_file

def log_question_response(question_data):
    """Log individual question response to CSV"""
    responses_file = session.get('responses_file')
    if responses_file:
        with open(responses_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                question_data['question_number'],
                question_data['visualization_type'],
                question_data['question_text'],
                question_data['user_answer'],
                question_data['correct_answer'],
                question_data['is_correct'],
                question_data['response_time_seconds']
            ])

def update_time_metrics():
    """Update the time metrics CSV file"""
    times_file = session.get('times_file')
    if times_file:
        total_time = round(time.time() - session.get('start_time', time.time()), 2)
        total_heatmap_time = round(session.get('total_heatmap_time', 0), 2)
        total_scatter_time = round(session.get('total_scatter_time', 0), 2)
        
        # Calculate average response times
        heatmap_questions = session.get('heatmap_questions', 0)
        scatter_questions = session.get('scatter_questions', 0)
        
        avg_heatmap_time = round(total_heatmap_time / max(1, heatmap_questions), 2)
        avg_scatter_time = round(total_scatter_time / max(1, scatter_questions), 2)
        
        with open(times_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'total_experiment_time',
                'total_heatmap_time',
                'total_scatter_time',
                'average_heatmap_response_time',
                'average_scatter_response_time'
            ])
            writer.writerow([
                total_time,
                total_heatmap_time,
                total_scatter_time,
                avg_heatmap_time,
                avg_scatter_time
            ])

@app.route('/')
def index():
    session['current_question'] = 0
    session['score'] = 0
    session['completed_questions'] = 0
    session['heatmap_questions'] = 0
    session['scatter_questions'] = 0
    
    # Create new CSV files for this session
    create_csv_files()
    
    # Record start time
    session['start_time'] = time.time()
    session['question_start_time'] = time.time()
    session['total_heatmap_time'] = 0
    session['total_scatter_time'] = 0
    
    # Initialize visualization type counters
    session['heatmap_questions'] = 0
    session['scatter_questions'] = 0
    
    heatmap_data, answers = generate_heatmap_and_answers()
    session['answers'] = answers

    # First visualization is always heatmap
    session['visualization_type'] = 'heatmap'
    
    heatmap_filename = 'heatmap.png'
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(heatmap_data, annot=False, cmap='Blues', cbar_kws={'label': 'Number of Students Absent'})
    plt.title("Heatmap of Student Absences Across Schools and Months")
    plt.xlabel("School ID")
    plt.ylabel("Month")
    plt.savefig(os.path.join('static', heatmap_filename))
    plt.close()

    current_question = QUESTIONS[0]
    return render_template('index.html', 
                         question=current_question,
                         plot_filename=heatmap_filename,
                         visualization_type='heatmap',
                         question_number=1,
                         total_questions=len(QUESTIONS) * 2)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_answer = request.form['answer']
    current_question_idx = session.get('current_question', 0)
    visualization_type = session.get('visualization_type')
    answers = session.get('answers', {})
    
    # Calculate response time for this question
    question_end_time = time.time()
    response_time = question_end_time - session.get('question_start_time', question_end_time)
    
    # Add response time to visualization-specific total
    if visualization_type == 'heatmap':
        session['total_heatmap_time'] = session.get('total_heatmap_time', 0) + response_time
        session['heatmap_questions'] = session.get('heatmap_questions', 0) + 1
    else:
        session['total_scatter_time'] = session.get('total_scatter_time', 0) + response_time
        session['scatter_questions'] = session.get('scatter_questions', 0) + 1
    
    current_question = QUESTIONS[current_question_idx]
    question_id = current_question['id']
    
    processed_answer = user_answer
    if 'School' in user_answer:
        processed_answer = int(user_answer.split()[1])
    
    correct_answer = str(answers[question_id])
    is_correct = str(processed_answer) == correct_answer
    
    # Log question response
    question_data = {
        'question_number': session.get('completed_questions', 0) + 1,
        'visualization_type': visualization_type,
        'question_text': current_question['text'],
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'is_correct': is_correct,
        'response_time_seconds': round(response_time, 2)
    }
    log_question_response(question_data)
    
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    
    # Increment completed questions counter
    session['completed_questions'] = session.get('completed_questions', 0) + 1
    
    # Check if all questions are completed
    if session['completed_questions'] >= len(QUESTIONS) * 2:
        # Update final time metrics
        update_time_metrics()
        return redirect(url_for('show_results'))
    
    # Toggle visualization type and update question index
    if visualization_type == 'heatmap':
        session['visualization_type'] = 'scatter'
    else:
        session['visualization_type'] = 'heatmap'
        session['current_question'] = (current_question_idx + 1) % len(QUESTIONS)
    
    # Reset question start time
    session['question_start_time'] = time.time()
    
    return redirect(url_for('transition'))
@app.route('/transition')
def transition():
    return render_template('transition.html')

@app.route('/next_question')
def next_question():
    current_question_idx = session.get('current_question', 0)
    visualization_type = session.get('visualization_type')
    
    # Set start time for new question
    session['question_start_time'] = time.time()
    
    heatmap_data, answers = generate_heatmap_and_answers()
    session['answers'] = answers
    
    if visualization_type == 'heatmap':
        plt.figure(figsize=(12, 8))
        ax = sns.heatmap(heatmap_data, annot=False, cmap='Blues', cbar_kws={'label': 'Number of Students Absent'})
        plt.title("Heatmap of Student Absences Across Schools and Months")
        plt.xlabel("School ID")
        plt.ylabel("Month")
        plot_filename = 'heatmap.png'
        plt.savefig(os.path.join('static', plot_filename))
        plt.close()
    else:
        plot_filename = plot_scatter(heatmap_data.reset_index().melt(id_vars='Month', var_name='School ID', value_name='Number of Students Absent'))
    
    current_question = QUESTIONS[current_question_idx]
    completed_questions = session.get('completed_questions', 0)
    
    return render_template('index.html',
                         question=current_question,
                         plot_filename=plot_filename,
                         visualization_type=visualization_type,
                         question_number=completed_questions + 1,
                         total_questions=len(QUESTIONS) * 2)

@app.route('/results')
def show_results():
    score = session.get('score', 0)
    total_questions = len(QUESTIONS) * 2
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
