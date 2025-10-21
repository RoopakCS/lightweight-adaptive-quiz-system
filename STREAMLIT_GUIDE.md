# Streamlit Web Application Guide

## 🌐 LAQS Interactive Web Interface

This guide explains how to use the Streamlit web application for the Lightweight Adaptive Quiz System.

---

## 🚀 Quick Start

### Installation

1. **Install dependencies** (including Streamlit):
```bash
pip install -r requirements.txt
```

2. **Launch the application**:
```bash
streamlit run streamlit_app.py
```

3. **Open in browser**:
The app will automatically open at `http://localhost:8501`

---

## 📱 Features Overview

### 1. 👤 User Authentication
- **Login**: Access your existing account
- **Register**: Create a new user account
- **Persistent Data**: All your quiz history is saved

### 2. 🎯 Take Adaptive Quiz
- **Choose Quiz Type**:
  - Adaptive (difficulty adjusts to your performance)
  - Non-Adaptive (fixed medium difficulty)
- **Configure Questions**: Select 5-30 questions per session
- **Real-Time Adaptation**: See difficulty change as you progress
- **Instant Feedback**: Know immediately if you're correct
- **Progress Tracking**: Visual progress bar shows completion

### 3. 📊 Personal Statistics Dashboard
- **Overall Performance**: Total sessions, average accuracy, mastery index
- **Learning Progression**: Charts showing improvement over time
- **Session History**: Detailed table of all past quizzes
- **Adaptive Insights**: How the system adapted to your level
- **Performance Breakdown**: Accuracy by difficulty level
- **Difficulty Distribution**: Visual breakdown of questions encountered

### 4. 🏆 Global Leaderboard
- **Top 3 Performers**: Medal-based ranking display
- **Complete Rankings**: Full leaderboard with all users
- **Your Position**: Your row is highlighted
- **Scoring System**: Based on accuracy, mastery, and total questions

### 5. ℹ️ About System
- **How It Works**: Explanation of adaptive algorithm
- **Metrics Guide**: Understanding accuracy, mastery, etc.
- **Benefits**: Why adaptive learning is effective
- **Tips**: How to get the most from the system

---

## 🎮 How to Use

### First Time Users

1. **Register an Account**:
   - Click "New User" tab
   - Enter your name
   - Choose a unique User ID
   - Click "Register"

2. **Take Your First Quiz**:
   - Navigate to "🎯 Take Quiz"
   - Select "Adaptive" quiz type
   - Choose number of questions (start with 10-15)
   - Click "🚀 Start Quiz"

3. **Answer Questions**:
   - Read each question carefully
   - Select your answer (A, B, C, or D)
   - Click "✓ Submit Answer"
   - See instant feedback
   - Watch difficulty adapt in real-time

4. **View Results**:
   - After completing the quiz, see your performance metrics
   - View accuracy, mastery index, and time statistics
   - See charts of performance breakdown
   - Results are automatically saved

5. **Check Statistics**:
   - Navigate to "📊 My Statistics"
   - See your learning progression
   - Compare adaptive vs non-adaptive performance
   - Track improvement over time

### Returning Users

1. **Login**:
   - Enter your User ID
   - Click "Login"
   - All your previous data loads automatically

2. **Continue Learning**:
   - Take more quizzes to see progression
   - Try different quiz types
   - Challenge yourself with more questions
   - Compare with leaderboard

---

## 📊 Understanding the Dashboard

### Metrics Explained

#### Accuracy
- **What it is**: Percentage of questions answered correctly
- **Range**: 0% to 100%
- **Good score**: 70%+ indicates solid understanding
- **How to improve**: Focus on understanding concepts, not just memorizing

#### Mastery Index
- **What it is**: Weighted score considering difficulty × correctness
- **Range**: 0.0 to 3.0
- **Calculation**: Higher when you answer harder questions correctly
- **Good score**: 1.5+ shows proficiency; 2.0+ shows mastery

#### Average Time per Question
- **What it is**: Mean response time across all questions
- **Expected**: 10-20s (easy), 20-40s (medium), 40-60s (hard)
- **Fast responses**: Good if accurate; may indicate guessing if not
- **Slow responses**: Acceptable for hard questions; may need practice for easy ones

### Charts and Visualizations

#### Learning Progression
- **Shows**: Accuracy and mastery trends across sessions
- **Look for**: Upward trends indicating improvement
- **Compare**: Adaptive (green) vs Non-Adaptive (red) lines

#### Difficulty Distribution
- **Shows**: What difficulty levels you encountered
- **Adaptive**: Should show variety (easy, medium, hard)
- **Non-Adaptive**: Only shows medium (by design)
- **Interpretation**: More hard questions = system thinks you're advanced

#### Performance Breakdown
- **Shows**: Accuracy split by difficulty level
- **Ideal Pattern**: 
  - Easy: 80-95% correct
  - Medium: 60-80% correct
  - Hard: 40-70% correct

---

## 🎯 Quiz Types Comparison

### Adaptive Quiz
**How it works**:
- Starts at medium difficulty
- If you perform well (>80% accuracy, fast response) → increases to hard
- If you struggle (<50% accuracy) → decreases to easy
- Otherwise maintains current difficulty

**Best for**:
- Personalized learning experience
- Finding your optimal challenge level
- Maximizing learning efficiency
- Tracking mastery progression

**Expect**:
- Difficulty changes during quiz
- Questions matched to your ability
- Better engagement
- Higher mastery scores

### Non-Adaptive Quiz
**How it works**:
- All questions at medium difficulty
- No adaptation during quiz
- Traditional quiz format

**Best for**:
- Baseline comparison
- Consistent difficulty assessment
- Testing specific difficulty level
- Comparing with adaptive performance

**Expect**:
- Constant medium difficulty
- May feel too easy or too hard
- Good for benchmarking
- Traditional test experience

---

## 🏆 Leaderboard System

### How Scoring Works
Your overall score is calculated as:
```
Score = (Average Accuracy × 50) + (Average Mastery × 10) + (Total Questions × 0.1)
```

**Components**:
- **Accuracy (50 points max)**: Rewards correctness
- **Mastery (30 points max)**: Rewards solving harder problems
- **Total Questions (variable)**: Rewards practice and engagement

### Tips to Rank Higher
1. **Take more quizzes**: More data = more stable performance
2. **Use adaptive mode**: Higher mastery potential
3. **Challenge yourself**: More questions per session
4. **Focus on accuracy**: Quality over speed
5. **Practice regularly**: Consistency improves performance

---

## 💡 Pro Tips

### For Best Learning Outcomes

1. **Start with Adaptive**:
   - Let the system find your level
   - Build confidence with appropriate difficulty
   - Challenge yourself as you improve

2. **Regular Practice**:
   - Take quizzes consistently (e.g., daily or weekly)
   - Track your progression over time
   - Identify patterns in your performance

3. **Review Statistics**:
   - Check after each session
   - Look for improvement trends
   - Identify weak areas (topics/difficulties)

4. **Compare Quiz Types**:
   - Take both adaptive and non-adaptive
   - See the difference in your performance
   - Understand the benefits of adaptation

5. **Challenge Progression**:
   - Start with 10-15 questions
   - Increase to 20-25 as you improve
   - Try 30 questions for deep practice

### Understanding Adaptation

**The system increases difficulty when**:
- You answer 4 out of 5 recent questions correctly
- Your response time is faster than expected
- You're demonstrating mastery

**The system decreases difficulty when**:
- You answer fewer than 3 out of 5 recent questions correctly
- You're struggling with current level
- You need to build confidence

**The system maintains difficulty when**:
- Your performance is in the middle range
- You're at an appropriate challenge level
- You're learning effectively

---

## 🔧 Troubleshooting

### Common Issues

**App won't start**:
```bash
# Reinstall Streamlit
pip install --upgrade streamlit

# Run with verbose output
streamlit run streamlit_app.py --logger.level=debug
```

**Can't login**:
- Check your User ID spelling
- Case-sensitive matching
- Register if new user

**Quiz not progressing**:
- Make sure to click "Submit Answer"
- Check browser console for errors
- Refresh the page if stuck

**Statistics not showing**:
- Complete at least one quiz first
- Data saves automatically after quiz completion
- Check `data/user_sessions.json` exists

**Plots not displaying**:
- Matplotlib backend issue
- Try: `pip install --upgrade matplotlib`
- Restart the app

### Performance Issues

**App running slow**:
- Close other browser tabs
- Clear browser cache
- Reduce number of questions per session
- Check CPU/memory usage

**Data loading slowly**:
- Limit number of users in leaderboard
- Archive old session data
- Fresh browser session

---

## 📁 Data Storage

### Where Your Data is Saved

**Location**: `data/user_sessions.json`

**Format**: JSON file containing:
```json
{
  "user_id": {
    "name": "Your Name",
    "sessions": [
      {
        "timestamp": "2025-10-21T10:30:00",
        "quiz_type": "adaptive",
        "accuracy": 0.75,
        "mastery_index": 1.85,
        ...
      }
    ]
  }
}
```

### Data Management

**Backup your data**:
```bash
# Copy the JSON file
cp data/user_sessions.json data/user_sessions_backup.json
```

**Reset your data**:
```bash
# Delete the JSON file (careful!)
rm data/user_sessions.json
```

**Export to CSV**:
The app automatically exports to CSVs after running simulations.

---

## 🎨 Customization

### Changing Quiz Settings

Edit `streamlit_app.py` to customize:

**Number of questions range**:
```python
num_questions = st.slider("Number of Questions:", 5, 30, 15)
# Change to: 10, 50, 20 for range 10-50 with default 20
```

**Adaptive thresholds**:
```python
# In init_session_state()
st.session_state.adaptive_engine = AdaptiveEngine(
    accuracy_threshold_high=0.85,  # Harder to level up
    accuracy_threshold_low=0.40     # Easier to level down
)
```

**Scoring formula**:
```python
# In show_leaderboard_page()
score = (avg_accuracy * 50) + (avg_mastery * 10) + (total_questions * 0.1)
# Adjust multipliers as desired
```

---

## 🚀 Advanced Features

### For Developers

**Add custom questions**:
1. Edit `src/question_bank.py`
2. Add questions with difficulty tags
3. Restart the app

**Add new metrics**:
1. Track in `src/performance_tracker.py`
2. Display in statistics page
3. Include in leaderboard scoring

**Custom visualizations**:
1. Add matplotlib/seaborn plots
2. Create new chart functions
3. Display in statistics section

**API Integration**:
1. Export session data via JSON
2. Import external questions
3. Sync with LMS platforms

---

## 📞 Support

### Getting Help

**Documentation**:
- README.md - Full project documentation
- QUICKSTART.md - Quick setup guide
- This file - Web app guide

**Common Solutions**:
1. Restart the app: `Ctrl+C` then `streamlit run streamlit_app.py`
2. Clear cache: `streamlit cache clear`
3. Check logs in terminal
4. Verify Python 3.8+ installed

**Report Issues**:
- Check GitHub issues
- Provide error messages
- Include steps to reproduce

---

## 🎉 Enjoy Learning!

The LAQS web application makes adaptive learning accessible, engaging, and data-driven. 

**Start your learning journey today!**

```bash
streamlit run streamlit_app.py
```

**Happy Learning! 🎓**
