# Quick Start Guide - Lightweight Adaptive Quiz System

## Installation & Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Quick Demo
```bash
python main.py
```

This will:
- Simulate 5 learners
- Run 3 quiz sessions per learner (adaptive + non-adaptive)
- Generate visualizations and statistical report
- Complete in ~30 seconds

## Understanding the Output

### Console Output
You'll see:
1. **System Initialization**: Question bank and learner population created
2. **Simulation Progress**: Live updates as learners complete sessions
3. **Statistical Summary**: Key findings comparing adaptive vs non-adaptive
4. **File Locations**: Where results are saved

### Generated Files

#### Data Files (`data/` folder)
- `question_bank.csv` - All 100 questions with difficulty levels
- `session_results.csv` - Summary of each quiz session
- `question_responses.csv` - Individual question-by-question responses

#### Result Files (`results/` folder)
- `learning_progression.png` - Shows accuracy/mastery improving over sessions
- `comparison_boxplot.png` - Statistical comparison of both quiz types
- `difficulty_distribution.png` - What difficulty levels were encountered
- `learner_comparison.png` - Individual learner trajectories
- `statistical_summary.png` - Key metrics bar charts
- `statistical_report.txt` - Comprehensive text report with all statistics

## Running Different Scenarios

### Full Simulation (15 learners, 5 sessions)
```bash
python main.py --full
```
*Takes ~2-3 minutes*

### Custom Configuration
```bash
# 20 learners, 7 sessions each, 25 questions per session
python main.py --learners 20 --sessions 7 --questions 25
```

### Large-Scale Experiment
```bash
python main.py --learners 50 --sessions 10 --questions 30
```
*Great for research papers - takes ~10 minutes*

## Interpreting Results

### What to Look For

#### 1. Accuracy Improvement
- **Expected**: Adaptive system shows 5-15% higher accuracy
- **Why**: Questions match learner ability level

#### 2. Mastery Index
- **Expected**: 10-20% improvement in adaptive
- **What it means**: Learners solve harder problems successfully

#### 3. Difficulty Progression
- **Adaptive**: Should show 3-5 changes per session
- **Non-Adaptive**: Always stays at "medium"

#### 4. Statistical Significance
- Check p-values in the report
- **p < 0.05** means results are statistically significant
- Effect size (Cohen's d) shows practical significance

### Sample Findings

From a typical simulation:

```
ADAPTIVE QUIZ:
  Mean Accuracy: 72.5%
  Mean Mastery: 1.85
  
NON-ADAPTIVE QUIZ:
  Mean Accuracy: 65.3%
  Mean Mastery: 1.52
  
IMPROVEMENT:
  Accuracy: +11.0%
  Mastery: +21.7%
  
SIGNIFICANCE:
  p-value: 0.0023 (highly significant)
  Effect size: 0.65 (medium-large effect)
```

## Using in Your Research

### For Academic Papers

1. **Run full simulation**:
   ```bash
   python main.py --full
   ```

2. **Collect these outputs**:
   - Statistical report (results/statistical_report.txt)
   - All visualizations (results/*.png)
   - Raw data (data/*.csv)

3. **Key sections to reference**:
   - Methodology: System design and adaptive algorithm
   - Results: Statistical comparison and effect sizes
   - Discussion: Benefits and limitations

### Customizing for Your Study

Edit these files to customize:

1. **Question Bank** (`src/question_bank.py`):
   - Add your own questions
   - Change topics/subjects
   - Adjust difficulty criteria

2. **Adaptive Rules** (`src/adaptive_engine.py`):
   - Modify accuracy thresholds
   - Adjust time sensitivity
   - Change window size

3. **Learner Profiles** (`src/learner_simulation.py`):
   - Create specific learner types
   - Adjust learning rates
   - Model different populations

## Common Use Cases

### 1. Quick Demo for Presentation
```bash
python main.py
```
Shows system works, generates visuals in 30 seconds

### 2. Research Paper Data Collection
```bash
python main.py --full
```
Generates publication-ready results

### 3. Parameter Tuning Study
```bash
# Modify adaptive_engine.py thresholds
# Then run multiple times:
python main.py --full
```
Compare different configurations

### 4. Large Population Study
```bash
python main.py --learners 100 --sessions 10
```
Robust statistical power

## Troubleshooting

### Issue: Import errors
**Solution**: Make sure you're in the project root directory
```bash
cd lightweight-adaptive-quiz-system
python main.py
```

### Issue: No visualizations appear
**Solution**: Plots are saved to `results/` folder even if display fails

### Issue: Simulation takes too long
**Solution**: Reduce parameters
```bash
python main.py --learners 5 --sessions 2
```

### Issue: Want to re-run with fresh data
**Solution**: Delete old data files
```bash
# Windows PowerShell
Remove-Item data\*.csv, results\*.png, results\*.txt -ErrorAction SilentlyContinue

# Then run again
python main.py
```

## Next Steps

1. **Run the demo** to see it in action
2. **Examine the results** in `results/` folder
3. **Read the statistical report** for detailed findings
4. **Customize the system** for your specific needs
5. **Share your findings**!

## Questions?

- Check the main README.md for detailed documentation
- Examine the code - it's well-commented
- Open an issue on GitHub

---

**Ready to start? Run:**
```bash
python main.py
```
