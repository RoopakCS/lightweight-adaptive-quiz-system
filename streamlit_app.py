"""
Streamlit Application for Lightweight Adaptive Quiz System (LAQS)
Interactive web interface for taking adaptive quizzes and viewing statistics.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import os
from pathlib import Path

# Import LAQS components
from src import (
    QuestionBank,
    AdaptiveEngine,
    NonAdaptiveEngine,
    SimulatedLearner,
    PerformanceTracker,
    StatisticalAnalyzer
)

# Configure page
st.set_page_config(
    page_title="LAQS - Adaptive Quiz System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2ecc71;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3498db;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-message {
        color: #2ecc71;
        font-weight: bold;
    }
    .error-message {
        color: #e74c3c;
        font-weight: bold;
    }
    .question-box {
        background-color: #ecf0f1;
        padding: 2rem;
        border-radius: 1rem;
        border-left: 5px solid #3498db;
        margin: 1rem 0;
    }
    .stats-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables."""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'question_bank' not in st.session_state:
        st.session_state.question_bank = QuestionBank(num_questions=100)
    if 'adaptive_engine' not in st.session_state:
        st.session_state.adaptive_engine = AdaptiveEngine()
    if 'current_quiz_active' not in st.session_state:
        st.session_state.current_quiz_active = False
    if 'current_question_idx' not in st.session_state:
        st.session_state.current_question_idx = 0
    if 'performance_history' not in st.session_state:
        st.session_state.performance_history = []
    if 'current_difficulty' not in st.session_state:
        st.session_state.current_difficulty = 'medium'
    if 'quiz_type' not in st.session_state:
        st.session_state.quiz_type = 'adaptive'
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'question_start_time' not in st.session_state:
        st.session_state.question_start_time = None
    if 'user_data_file' not in st.session_state:
        st.session_state.user_data_file = 'data/user_sessions.json'

init_session_state()

# User data management
def load_user_data():
    """Load user session data from JSON file."""
    Path('data').mkdir(exist_ok=True)
    if os.path.exists(st.session_state.user_data_file):
        with open(st.session_state.user_data_file, 'r') as f:
            return json.load(f)
    return {}

def save_user_data(data):
    """Save user session data to JSON file."""
    Path('data').mkdir(exist_ok=True)
    with open(st.session_state.user_data_file, 'w') as f:
        json.dump(data, f, indent=2)

def save_session_result():
    """Save completed session results."""
    if not st.session_state.performance_history:
        return
    
    user_data = load_user_data()
    
    if st.session_state.user_id not in user_data:
        user_data[st.session_state.user_id] = {
            'name': st.session_state.user_name,
            'sessions': []
        }
    
    # Calculate session metrics
    accuracy = sum(1 for p in st.session_state.performance_history if p['correct']) / len(st.session_state.performance_history)
    mastery = st.session_state.adaptive_engine.calculate_mastery_index(st.session_state.performance_history)
    avg_time = np.mean([p['time'] for p in st.session_state.performance_history])
    
    session_data = {
        'timestamp': datetime.now().isoformat(),
        'quiz_type': st.session_state.quiz_type,
        'num_questions': len(st.session_state.performance_history),
        'accuracy': accuracy,
        'mastery_index': mastery,
        'avg_time': avg_time,
        'difficulty_progression': [p['difficulty'] for p in st.session_state.performance_history],
        'performance_history': st.session_state.performance_history
    }
    
    user_data[st.session_state.user_id]['sessions'].append(session_data)
    save_user_data(user_data)

# Authentication page
def show_login_page():
    """Display login/registration page."""
    st.markdown('<h1 class="main-header">🎓 Lightweight Adaptive Quiz System</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem;">Welcome to LAQS - An intelligent quiz system that adapts to your learning level!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 👤 User Authentication")
        
        tab1, tab2 = st.tabs(["Login", "New User"])
        
        with tab1:
            st.markdown("#### Login to Existing Account")
            user_id = st.text_input("User ID", key="login_id")
            
            if st.button("Login", type="primary", use_container_width=True):
                user_data = load_user_data()
                if user_id in user_data:
                    st.session_state.user_id = user_id
                    st.session_state.user_name = user_data[user_id]['name']
                    st.success(f"Welcome back, {st.session_state.user_name}! 🎉")
                    st.rerun()
                else:
                    st.error("User ID not found. Please register as a new user.")
        
        with tab2:
            st.markdown("#### Register New Account")
            new_name = st.text_input("Your Name", key="new_name")
            new_id = st.text_input("Choose a User ID", key="new_id")
            
            if st.button("Register", type="primary", use_container_width=True):
                if new_name and new_id:
                    user_data = load_user_data()
                    if new_id in user_data:
                        st.error("User ID already exists. Please choose a different one.")
                    else:
                        user_data[new_id] = {
                            'name': new_name,
                            'sessions': []
                        }
                        save_user_data(user_data)
                        st.session_state.user_id = new_id
                        st.session_state.user_name = new_name
                        st.success(f"Welcome, {new_name}! Your account has been created. 🎉")
                        st.rerun()
                else:
                    st.error("Please fill in all fields.")

# Main navigation
def show_navigation():
    """Display navigation sidebar."""
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.markdown(f"**User ID:** `{st.session_state.user_id}`")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🎯 Take Quiz", "📊 My Statistics", "🏆 Leaderboard", "ℹ️ About System"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        return page

# Quiz page
def show_quiz_page():
    """Display quiz taking interface."""
    st.markdown('<h1 class="main-header">🎯 Take Adaptive Quiz</h1>', unsafe_allow_html=True)
    
    if not st.session_state.current_quiz_active:
        # Quiz configuration
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Quiz Configuration")
            quiz_type = st.radio(
                "Select Quiz Type:",
                ["Adaptive", "Non-Adaptive (Medium Difficulty)"],
                help="Adaptive: Difficulty adjusts based on your performance\nNon-Adaptive: Fixed medium difficulty"
            )
            st.session_state.quiz_type = 'adaptive' if quiz_type == "Adaptive" else 'non-adaptive'
            
            num_questions = st.slider("Number of Questions:", 5, 30, 15)
        
        with col2:
            st.markdown("### Quiz Information")
            st.info("""
            **Adaptive Quiz:**
            - Questions adjust to your skill level
            - Helps you learn at optimal difficulty
            - Tracks your mastery progression
            
            **Non-Adaptive Quiz:**
            - All questions at medium difficulty
            - Baseline comparison
            - Traditional quiz format
            """)
        
        if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
            st.session_state.current_quiz_active = True
            st.session_state.current_question_idx = 0
            st.session_state.performance_history = []
            st.session_state.current_difficulty = 'medium'
            st.session_state.num_questions = num_questions
            st.session_state.start_time = datetime.now()
            st.session_state.question_start_time = datetime.now()
            st.rerun()
    
    else:
        # Active quiz
        if st.session_state.current_question_idx < st.session_state.num_questions:
            show_quiz_question()
        else:
            show_quiz_results()

def show_quiz_question():
    """Display current quiz question."""
    progress = st.session_state.current_question_idx / st.session_state.num_questions
    st.progress(progress)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**Question {st.session_state.current_question_idx + 1} of {st.session_state.num_questions}**")
    with col2:
        st.markdown(f"**Difficulty:** `{st.session_state.current_difficulty.upper()}`")
    with col3:
        st.markdown(f"**Type:** `{st.session_state.quiz_type.upper()}`")
    
    # Get question
    question = st.session_state.question_bank.get_question(difficulty=st.session_state.current_difficulty)
    
    st.markdown(f"""
    <div class="question-box">
        <h3>Question {st.session_state.current_question_idx + 1}</h3>
        <p style="font-size: 1.2rem; margin-top: 1rem;"><strong>Topic:</strong> {question['topic']}</p>
        <p style="font-size: 1.4rem; margin-top: 1rem;">{question['text']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer options
    options = ['A', 'B', 'C', 'D']
    answer = st.radio(
        "Select your answer:",
        options,
        key=f"q_{st.session_state.current_question_idx}",
        horizontal=True
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("✓ Submit Answer", type="primary", use_container_width=True):
            # Calculate time taken
            time_taken = (datetime.now() - st.session_state.question_start_time).total_seconds()
            
            # Check if correct
            correct = (answer == question['correct_answer'])
            
            # Record performance
            performance = {
                'correct': correct,
                'time': time_taken,
                'expected_time': question['expected_time'],
                'difficulty': question['difficulty'],
                'topic': question['topic'],
                'question_id': question['id']
            }
            st.session_state.performance_history.append(performance)
            
            # Determine next difficulty
            if st.session_state.quiz_type == 'adaptive':
                engine = st.session_state.adaptive_engine
                st.session_state.current_difficulty = engine.get_next_difficulty(
                    st.session_state.performance_history,
                    st.session_state.current_difficulty
                )
            
            # Move to next question
            st.session_state.current_question_idx += 1
            st.session_state.question_start_time = datetime.now()
            
            # Show feedback
            if correct:
                st.success("✓ Correct! Well done!")
            else:
                st.error(f"✗ Incorrect. The correct answer was {question['correct_answer']}.")
            
            st.rerun()
    
    with col2:
        if st.button("⏭ Skip Question", use_container_width=True):
            # Record as incorrect with max time
            performance = {
                'correct': False,
                'time': question['expected_time'] * 2,
                'expected_time': question['expected_time'],
                'difficulty': question['difficulty'],
                'topic': question['topic'],
                'question_id': question['id']
            }
            st.session_state.performance_history.append(performance)
            
            # Move to next question
            st.session_state.current_question_idx += 1
            st.session_state.question_start_time = datetime.now()
            st.rerun()

def show_quiz_results():
    """Display quiz completion results."""
    st.balloons()
    
    st.markdown('<h2 class="sub-header">🎉 Quiz Completed!</h2>', unsafe_allow_html=True)
    
    # Calculate metrics
    accuracy = sum(1 for p in st.session_state.performance_history if p['correct']) / len(st.session_state.performance_history)
    mastery = st.session_state.adaptive_engine.calculate_mastery_index(st.session_state.performance_history)
    avg_time = np.mean([p['time'] for p in st.session_state.performance_history])
    total_time = (datetime.now() - st.session_state.start_time).total_seconds()
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Accuracy", f"{accuracy:.1%}", help="Percentage of correct answers")
    with col2:
        st.metric("Mastery Index", f"{mastery:.2f}", help="Weighted score (0-3 scale)")
    with col3:
        st.metric("Avg Time/Question", f"{avg_time:.1f}s", help="Average response time")
    with col4:
        st.metric("Total Time", f"{total_time/60:.1f}min", help="Total quiz duration")
    
    # Performance breakdown
    st.markdown("### 📈 Performance Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Accuracy by difficulty
        df = pd.DataFrame(st.session_state.performance_history)
        acc_by_diff = df.groupby('difficulty')['correct'].mean()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        acc_by_diff.plot(kind='bar', ax=ax, color=['#2ecc71', '#3498db', '#e74c3c'])
        ax.set_title('Accuracy by Difficulty Level')
        ax.set_ylabel('Accuracy')
        ax.set_xlabel('Difficulty')
        ax.set_ylim([0, 1])
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        # Difficulty progression
        difficulties = [p['difficulty'] for p in st.session_state.performance_history]
        difficulty_map = {'easy': 1, 'medium': 2, 'hard': 3}
        difficulty_scores = [difficulty_map[d] for d in difficulties]
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(range(1, len(difficulty_scores) + 1), difficulty_scores, marker='o', linewidth=2, color='#3498db')
        ax.set_title('Difficulty Progression')
        ax.set_ylabel('Difficulty Level')
        ax.set_xlabel('Question Number')
        ax.set_yticks([1, 2, 3])
        ax.set_yticklabels(['Easy', 'Medium', 'Hard'])
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    # Save results
    save_session_result()
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 View Detailed Statistics", type="primary", use_container_width=True):
            st.session_state.current_quiz_active = False
            st.rerun()
    with col2:
        if st.button("🔄 Take Another Quiz", use_container_width=True):
            st.session_state.current_quiz_active = False
            st.rerun()

# Statistics page
def show_statistics_page():
    """Display user statistics and analytics."""
    st.markdown('<h1 class="main-header">📊 My Learning Statistics</h1>', unsafe_allow_html=True)
    
    user_data = load_user_data()
    
    if st.session_state.user_id not in user_data or not user_data[st.session_state.user_id]['sessions']:
        st.info("No quiz data yet. Take a quiz to see your statistics!")
        return
    
    sessions = user_data[st.session_state.user_id]['sessions']
    
    # Overall statistics
    st.markdown("### 🏆 Overall Performance")
    
    total_sessions = len(sessions)
    avg_accuracy = np.mean([s['accuracy'] for s in sessions])
    avg_mastery = np.mean([s['mastery_index'] for s in sessions])
    total_questions = sum([s['num_questions'] for s in sessions])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sessions", total_sessions)
    with col2:
        st.metric("Average Accuracy", f"{avg_accuracy:.1%}")
    with col3:
        st.metric("Average Mastery", f"{avg_mastery:.2f}")
    with col4:
        st.metric("Total Questions", total_questions)
    
    # Learning progression
    st.markdown("### 📈 Learning Progression")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Accuracy over time
        fig, ax = plt.subplots(figsize=(10, 6))
        
        adaptive_sessions = [s for s in sessions if s['quiz_type'] == 'adaptive']
        non_adaptive_sessions = [s for s in sessions if s['quiz_type'] == 'non-adaptive']
        
        if adaptive_sessions:
            adaptive_acc = [s['accuracy'] for s in adaptive_sessions]
            ax.plot(range(1, len(adaptive_acc) + 1), adaptive_acc, marker='o', 
                   linewidth=2, label='Adaptive', color='#2ecc71')
        
        if non_adaptive_sessions:
            non_adaptive_acc = [s['accuracy'] for s in non_adaptive_sessions]
            ax.plot(range(1, len(non_adaptive_acc) + 1), non_adaptive_acc, marker='s',
                   linewidth=2, label='Non-Adaptive', color='#e74c3c')
        
        ax.set_title('Accuracy Progression Over Sessions')
        ax.set_xlabel('Session Number')
        ax.set_ylabel('Accuracy')
        ax.set_ylim([0, 1])
        ax.legend()
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        # Mastery progression
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if adaptive_sessions:
            adaptive_mastery = [s['mastery_index'] for s in adaptive_sessions]
            ax.plot(range(1, len(adaptive_mastery) + 1), adaptive_mastery, marker='o',
                   linewidth=2, label='Adaptive', color='#2ecc71')
        
        if non_adaptive_sessions:
            non_adaptive_mastery = [s['mastery_index'] for s in non_adaptive_sessions]
            ax.plot(range(1, len(non_adaptive_mastery) + 1), non_adaptive_mastery, marker='s',
                   linewidth=2, label='Non-Adaptive', color='#e74c3c')
        
        ax.set_title('Mastery Index Progression')
        ax.set_xlabel('Session Number')
        ax.set_ylabel('Mastery Index')
        ax.set_ylim([0, 3])
        ax.legend()
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    # Detailed session history
    st.markdown("### 📋 Session History")
    
    # Create DataFrame
    session_df = pd.DataFrame([
        {
            'Date': datetime.fromisoformat(s['timestamp']).strftime('%Y-%m-%d %H:%M'),
            'Quiz Type': s['quiz_type'].capitalize(),
            'Questions': s['num_questions'],
            'Accuracy': f"{s['accuracy']:.1%}",
            'Mastery': f"{s['mastery_index']:.2f}",
            'Avg Time (s)': f"{s['avg_time']:.1f}"
        }
        for s in reversed(sessions)
    ])
    
    st.dataframe(session_df, use_container_width=True)
    
    # Adaptive system insights
    if adaptive_sessions:
        st.markdown("### 🧠 Adaptive System Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Difficulty distribution
            all_difficulties = []
            for s in adaptive_sessions:
                all_difficulties.extend(s['difficulty_progression'])
            
            diff_counts = pd.Series(all_difficulties).value_counts()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            diff_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%',
                           colors=['#2ecc71', '#3498db', '#e74c3c'])
            ax.set_title('Question Difficulty Distribution')
            ax.set_ylabel('')
            st.pyplot(fig)
        
        with col2:
            st.markdown("#### 🎯 Adaptation Statistics")
            
            avg_changes = np.mean([
                len(set(s['difficulty_progression'])) - 1
                for s in adaptive_sessions
            ])
            
            st.info(f"""
            **Average Difficulty Changes per Session:** {avg_changes:.1f}
            
            The adaptive system adjusted question difficulty an average of {avg_changes:.1f} times per session,
            indicating that the system is actively personalizing the quiz to your ability level.
            """)
            
            # Learning rate estimate
            if len(adaptive_sessions) >= 3:
                first_acc = adaptive_sessions[0]['accuracy']
                last_acc = adaptive_sessions[-1]['accuracy']
                improvement = (last_acc - first_acc) * 100
                
                if improvement > 0:
                    st.success(f"📈 You've improved by {improvement:.1f}% since your first adaptive quiz!")
                else:
                    st.info("Keep practicing! Your performance will improve over time.")

# Leaderboard page
def show_leaderboard_page():
    """Display leaderboard with all users."""
    st.markdown('<h1 class="main-header">🏆 Global Leaderboard</h1>', unsafe_allow_html=True)
    
    user_data = load_user_data()
    
    if not user_data:
        st.info("No users have taken quizzes yet. Be the first!")
        return
    
    # Calculate scores for all users
    leaderboard = []
    for user_id, data in user_data.items():
        if data['sessions']:
            avg_accuracy = np.mean([s['accuracy'] for s in data['sessions']])
            avg_mastery = np.mean([s['mastery_index'] for s in data['sessions']])
            total_questions = sum([s['num_questions'] for s in data['sessions']])
            
            # Calculate overall score (weighted)
            score = (avg_accuracy * 50) + (avg_mastery * 10) + (total_questions * 0.1)
            
            leaderboard.append({
                'Name': data['name'],
                'User ID': user_id,
                'Avg Accuracy': avg_accuracy,
                'Avg Mastery': avg_mastery,
                'Total Questions': total_questions,
                'Score': score,
                'Sessions': len(data['sessions'])
            })
    
    # Sort by score
    leaderboard = sorted(leaderboard, key=lambda x: x['Score'], reverse=True)
    
    # Display top 3
    st.markdown("### 🌟 Top Performers")
    
    if len(leaderboard) >= 1:
        col1, col2, col3 = st.columns(3)
        
        medals = ['🥇', '🥈', '🥉']
        cols = [col1, col2, col3]
        
        for i, col in enumerate(cols[:min(3, len(leaderboard))]):
            with col:
                user = leaderboard[i]
                highlight = "background-color: #fffacd;" if user['User ID'] == st.session_state.user_id else ""
                st.markdown(f"""
                <div class="stats-box" style="{highlight}">
                    <h2 style="text-align: center;">{medals[i]}</h2>
                    <h3 style="text-align: center;">{user['Name']}</h3>
                    <p style="text-align: center;"><strong>Score:</strong> {user['Score']:.1f}</p>
                    <p><strong>Accuracy:</strong> {user['Avg Accuracy']:.1%}</p>
                    <p><strong>Mastery:</strong> {user['Avg Mastery']:.2f}</p>
                    <p><strong>Questions:</strong> {user['Total Questions']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Full leaderboard
    st.markdown("### 📊 Complete Rankings")
    
    leaderboard_df = pd.DataFrame([
        {
            'Rank': i + 1,
            'Name': user['Name'],
            'User ID': user['User ID'],
            'Score': f"{user['Score']:.1f}",
            'Accuracy': f"{user['Avg Accuracy']:.1%}",
            'Mastery': f"{user['Avg Mastery']:.2f}",
            'Questions': user['Total Questions'],
            'Sessions': user['Sessions']
        }
        for i, user in enumerate(leaderboard)
    ])
    
    # Highlight current user
    def highlight_user(row):
        if row['User ID'] == st.session_state.user_id:
            return ['background-color: #fffacd'] * len(row)
        return [''] * len(row)
    
    styled_df = leaderboard_df.style.apply(highlight_user, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

# About page
def show_about_page():
    """Display information about the system."""
    st.markdown('<h1 class="main-header">ℹ️ About LAQS</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎓 Lightweight Adaptive Quiz System
    
    LAQS is an intelligent quiz system that adapts to your learning level in real-time using a 
    rule-based algorithm. Unlike traditional static quizzes, LAQS dynamically adjusts question 
    difficulty based on your performance.
    
    ### 🧠 How It Works
    
    The adaptive algorithm follows these rules:
    
    1. **High Performance** (Accuracy > 80% & Fast Response)
       - → System increases difficulty to challenge you more
    
    2. **Low Performance** (Accuracy < 50%)
       - → System decreases difficulty to build confidence
    
    3. **Medium Performance**
       - → System maintains current difficulty level
    
    ### 📊 Metrics Explained
    
    - **Accuracy**: Percentage of questions answered correctly
    - **Mastery Index**: Weighted score considering both correctness and difficulty (0-3 scale)
    - **Response Time**: How quickly you answer questions
    - **Difficulty Progression**: How the system adapts difficulty over time
    
    ### 🎯 Benefits of Adaptive Learning
    
    - **Personalized Experience**: Questions match your skill level
    - **Optimal Challenge**: Keeps you engaged without frustration or boredom
    - **Faster Learning**: Focuses on content at your zone of proximal development
    - **Better Retention**: Appropriate difficulty enhances memory formation
    
    ### 🔬 Research Basis
    
    This system is based on educational psychology principles and adaptive testing research.
    It demonstrates how lightweight, rule-based algorithms can effectively improve learning
    outcomes without requiring complex machine learning models or large datasets.
    
    ### 📈 Your Progress
    
    The system tracks your performance across sessions to show:
    - Learning progression over time
    - Comparison between adaptive and non-adaptive quizzes
    - Detailed performance analytics
    - Areas for improvement
    
    ### 🏆 Competitive Learning
    
    Check the leaderboard to see how you compare with other learners and stay motivated!
    
    ---
    
    ### 💡 Tips for Best Results
    
    1. **Take regular quizzes** to see meaningful progress
    2. **Try both adaptive and non-adaptive** modes to compare
    3. **Focus on understanding**, not just speed
    4. **Review your statistics** to identify patterns
    5. **Challenge yourself** with more questions per session
    
    ---
    
    ### 🛠️ Technical Details
    
    - **Algorithm**: Rule-based adaptive difficulty selection
    - **Thresholds**: 80% high accuracy, 50% low accuracy
    - **Window Size**: Last 5 questions considered for adaptation
    - **Question Bank**: 100 questions across 5 topics and 3 difficulty levels
    - **Metrics**: Accuracy, mastery index, response time, difficulty progression
    
    ---
    
    **Built with ❤️ using Python, Streamlit, and open-source libraries**
    """)

# Main app
def main():
    """Main application entry point."""
    
    if st.session_state.user_id is None:
        show_login_page()
    else:
        page = show_navigation()
        
        if page == "🎯 Take Quiz":
            show_quiz_page()
        elif page == "📊 My Statistics":
            show_statistics_page()
        elif page == "🏆 Leaderboard":
            show_leaderboard_page()
        elif page == "ℹ️ About System":
            show_about_page()

if __name__ == "__main__":
    main()
