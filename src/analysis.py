"""
Analysis Module
Statistical analysis and reporting for quiz system evaluation.
"""

import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path


class StatisticalAnalyzer:
    """Performs statistical analysis on quiz system performance data."""
    
    def __init__(self, tracker):
        """
        Initialize analyzer with performance tracker.
        
        Args:
            tracker: PerformanceTracker instance
        """
        self.tracker = tracker
        self.sessions_df = tracker.get_all_sessions_df()
        self.questions_df = tracker.get_all_questions_df()
    
    def compute_descriptive_stats(self):
        """Compute descriptive statistics for both quiz types."""
        if self.sessions_df.empty:
            return {}
        
        stats_dict = {}
        
        for quiz_type in ['adaptive', 'non-adaptive']:
            data = self.sessions_df[self.sessions_df['quiz_type'] == quiz_type]
            
            if data.empty:
                continue
            
            stats_dict[quiz_type] = {
                'accuracy': {
                    'mean': data['accuracy'].mean(),
                    'std': data['accuracy'].std(),
                    'min': data['accuracy'].min(),
                    'max': data['accuracy'].max(),
                    'median': data['accuracy'].median()
                },
                'mastery_index': {
                    'mean': data['mastery_index'].mean(),
                    'std': data['mastery_index'].std(),
                    'min': data['mastery_index'].min(),
                    'max': data['mastery_index'].max(),
                    'median': data['mastery_index'].median()
                },
                'avg_time_per_question': {
                    'mean': data['avg_time_per_question'].mean(),
                    'std': data['avg_time_per_question'].std(),
                    'min': data['avg_time_per_question'].min(),
                    'max': data['avg_time_per_question'].max(),
                    'median': data['avg_time_per_question'].median()
                },
                'total_sessions': len(data)
            }
        
        return stats_dict
    
    def perform_t_tests(self):
        """
        Perform t-tests to compare adaptive vs non-adaptive performance.
        
        Returns:
            Dictionary with t-test results
        """
        if self.sessions_df.empty:
            return {}
        
        adaptive_data = self.sessions_df[self.sessions_df['quiz_type'] == 'adaptive']
        non_adaptive_data = self.sessions_df[self.sessions_df['quiz_type'] == 'non-adaptive']
        
        if adaptive_data.empty or non_adaptive_data.empty:
            return {}
        
        results = {}
        
        # T-test for accuracy
        t_stat_acc, p_value_acc = stats.ttest_ind(
            adaptive_data['accuracy'],
            non_adaptive_data['accuracy']
        )
        results['accuracy'] = {
            't_statistic': t_stat_acc,
            'p_value': p_value_acc,
            'significant': p_value_acc < 0.05
        }
        
        # T-test for mastery index
        t_stat_mast, p_value_mast = stats.ttest_ind(
            adaptive_data['mastery_index'],
            non_adaptive_data['mastery_index']
        )
        results['mastery_index'] = {
            't_statistic': t_stat_mast,
            'p_value': p_value_mast,
            'significant': p_value_mast < 0.05
        }
        
        # T-test for time per question
        t_stat_time, p_value_time = stats.ttest_ind(
            adaptive_data['avg_time_per_question'],
            non_adaptive_data['avg_time_per_question']
        )
        results['avg_time_per_question'] = {
            't_statistic': t_stat_time,
            'p_value': p_value_time,
            'significant': p_value_time < 0.05
        }
        
        return results
    
    def calculate_effect_sizes(self):
        """
        Calculate Cohen's d effect sizes for key metrics.
        
        Returns:
            Dictionary with effect size values
        """
        if self.sessions_df.empty:
            return {}
        
        adaptive_data = self.sessions_df[self.sessions_df['quiz_type'] == 'adaptive']
        non_adaptive_data = self.sessions_df[self.sessions_df['quiz_type'] == 'non-adaptive']
        
        if adaptive_data.empty or non_adaptive_data.empty:
            return {}
        
        def cohens_d(group1, group2):
            """Calculate Cohen's d effect size."""
            n1, n2 = len(group1), len(group2)
            var1, var2 = group1.var(), group2.var()
            pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
            return (group1.mean() - group2.mean()) / pooled_std if pooled_std > 0 else 0
        
        effect_sizes = {}
        
        # Effect size for accuracy
        effect_sizes['accuracy'] = cohens_d(
            adaptive_data['accuracy'],
            non_adaptive_data['accuracy']
        )
        
        # Effect size for mastery index
        effect_sizes['mastery_index'] = cohens_d(
            adaptive_data['mastery_index'],
            non_adaptive_data['mastery_index']
        )
        
        # Effect size for time
        effect_sizes['avg_time_per_question'] = cohens_d(
            adaptive_data['avg_time_per_question'],
            non_adaptive_data['avg_time_per_question']
        )
        
        return effect_sizes
    
    def analyze_learning_gains(self):
        """
        Analyze learning gains (pre-test to post-test improvement).
        
        Returns:
            Dictionary with learning gain statistics
        """
        if self.sessions_df.empty:
            return {}
        
        gains = {}
        
        for quiz_type in ['adaptive', 'non-adaptive']:
            type_data = self.sessions_df[self.sessions_df['quiz_type'] == quiz_type]
            
            learner_gains = []
            
            for learner_id in type_data['learner_id'].unique():
                learner_sessions = type_data[type_data['learner_id'] == learner_id].sort_values('start_time')
                
                if len(learner_sessions) >= 2:
                    first_acc = learner_sessions.iloc[0]['accuracy']
                    last_acc = learner_sessions.iloc[-1]['accuracy']
                    gain = last_acc - first_acc
                    learner_gains.append(gain)
            
            if learner_gains:
                gains[quiz_type] = {
                    'mean_gain': np.mean(learner_gains),
                    'std_gain': np.std(learner_gains),
                    'median_gain': np.median(learner_gains),
                    'positive_gains': sum(1 for g in learner_gains if g > 0),
                    'total_learners': len(learner_gains)
                }
        
        return gains
    
    def generate_report(self, output_file='results/statistical_report.txt'):
        """
        Generate comprehensive statistical report.
        
        Args:
            output_file: Path to save the report
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(exist_ok=True, parents=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("LIGHTWEIGHT ADAPTIVE QUIZ SYSTEM - STATISTICAL ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            # Descriptive Statistics
            f.write("1. DESCRIPTIVE STATISTICS\n")
            f.write("-" * 80 + "\n\n")
            
            desc_stats = self.compute_descriptive_stats()
            
            for quiz_type, stats_dict in desc_stats.items():
                f.write(f"{quiz_type.upper()} QUIZ:\n")
                f.write(f"  Total Sessions: {stats_dict['total_sessions']}\n\n")
                
                f.write(f"  Accuracy:\n")
                f.write(f"    Mean: {stats_dict['accuracy']['mean']:.4f}\n")
                f.write(f"    Std Dev: {stats_dict['accuracy']['std']:.4f}\n")
                f.write(f"    Median: {stats_dict['accuracy']['median']:.4f}\n")
                f.write(f"    Range: [{stats_dict['accuracy']['min']:.4f}, {stats_dict['accuracy']['max']:.4f}]\n\n")
                
                f.write(f"  Mastery Index:\n")
                f.write(f"    Mean: {stats_dict['mastery_index']['mean']:.4f}\n")
                f.write(f"    Std Dev: {stats_dict['mastery_index']['std']:.4f}\n")
                f.write(f"    Median: {stats_dict['mastery_index']['median']:.4f}\n")
                f.write(f"    Range: [{stats_dict['mastery_index']['min']:.4f}, {stats_dict['mastery_index']['max']:.4f}]\n\n")
                
                f.write(f"  Avg Time per Question (seconds):\n")
                f.write(f"    Mean: {stats_dict['avg_time_per_question']['mean']:.2f}\n")
                f.write(f"    Std Dev: {stats_dict['avg_time_per_question']['std']:.2f}\n")
                f.write(f"    Median: {stats_dict['avg_time_per_question']['median']:.2f}\n\n")
            
            # T-test Results
            f.write("\n2. STATISTICAL SIGNIFICANCE TESTS (Independent t-tests)\n")
            f.write("-" * 80 + "\n\n")
            
            t_test_results = self.perform_t_tests()
            
            for metric, result in t_test_results.items():
                f.write(f"{metric.replace('_', ' ').title()}:\n")
                f.write(f"  t-statistic: {result['t_statistic']:.4f}\n")
                f.write(f"  p-value: {result['p_value']:.6f}\n")
                f.write(f"  Significant (p < 0.05): {'YES' if result['significant'] else 'NO'}\n\n")
            
            # Effect Sizes
            f.write("\n3. EFFECT SIZES (Cohen's d)\n")
            f.write("-" * 80 + "\n\n")
            f.write("Interpretation: |d| < 0.2 (small), 0.2-0.8 (medium), > 0.8 (large)\n\n")
            
            effect_sizes = self.calculate_effect_sizes()
            
            for metric, d_value in effect_sizes.items():
                magnitude = "small" if abs(d_value) < 0.2 else ("medium" if abs(d_value) < 0.8 else "large")
                f.write(f"{metric.replace('_', ' ').title()}:\n")
                f.write(f"  Cohen's d: {d_value:.4f} ({magnitude} effect)\n\n")
            
            # Learning Gains
            f.write("\n4. LEARNING GAINS ANALYSIS\n")
            f.write("-" * 80 + "\n\n")
            
            learning_gains = self.analyze_learning_gains()
            
            for quiz_type, gains in learning_gains.items():
                f.write(f"{quiz_type.upper()} QUIZ:\n")
                f.write(f"  Mean Learning Gain: {gains['mean_gain']:.4f}\n")
                f.write(f"  Std Dev: {gains['std_gain']:.4f}\n")
                f.write(f"  Median Gain: {gains['median_gain']:.4f}\n")
                f.write(f"  Learners with Positive Gains: {gains['positive_gains']}/{gains['total_learners']} ")
                f.write(f"({gains['positive_gains']/gains['total_learners']*100:.1f}%)\n\n")
            
            # Comparison Summary
            f.write("\n5. COMPARISON SUMMARY\n")
            f.write("-" * 80 + "\n\n")
            
            comparison = self.tracker.get_comparison_stats()
            
            if comparison:
                f.write(f"Accuracy Improvement: {comparison.get('accuracy_improvement', 0):.2f}%\n")
                f.write(f"Mastery Improvement: {comparison.get('mastery_improvement', 0):.2f}%\n\n")
                
                f.write("Adaptive system demonstrates:\n")
                if comparison.get('accuracy_improvement', 0) > 0:
                    f.write(f"  ✓ Higher accuracy by {comparison['accuracy_improvement']:.2f}%\n")
                if comparison.get('mastery_improvement', 0) > 0:
                    f.write(f"  ✓ Higher mastery by {comparison['mastery_improvement']:.2f}%\n")
                if comparison['adaptive']['mean_difficulty_changes'] > 0:
                    f.write(f"  ✓ Dynamic difficulty adjustment (avg {comparison['adaptive']['mean_difficulty_changes']:.1f} changes per session)\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
        
        print(f"Statistical report saved to: {output_path}")
        return output_path
    
    def print_summary(self):
        """Print a concise summary to console."""
        print("\n" + "=" * 70)
        print("STATISTICAL ANALYSIS SUMMARY")
        print("=" * 70)
        
        comparison = self.tracker.get_comparison_stats()
        
        if comparison:
            print("\nPERFORMANCE COMPARISON:")
            print(f"  Adaptive Accuracy:     {comparison['adaptive']['mean_accuracy']:.2%}")
            print(f"  Non-Adaptive Accuracy: {comparison['non_adaptive']['mean_accuracy']:.2%}")
            print(f"  → Improvement:         {comparison.get('accuracy_improvement', 0):+.2f}%")
            
            print(f"\n  Adaptive Mastery:      {comparison['adaptive']['mean_mastery']:.3f}")
            print(f"  Non-Adaptive Mastery:  {comparison['non_adaptive']['mean_mastery']:.3f}")
            print(f"  → Improvement:         {comparison.get('mastery_improvement', 0):+.2f}%")
        
        t_tests = self.perform_t_tests()
        if t_tests:
            print("\nSTATISTICAL SIGNIFICANCE:")
            for metric, result in t_tests.items():
                sig_mark = "✓" if result['significant'] else "✗"
                print(f"  {sig_mark} {metric}: p = {result['p_value']:.4f}")
        
        effect_sizes = self.calculate_effect_sizes()
        if effect_sizes:
            print("\nEFFECT SIZES (Cohen's d):")
            for metric, d_value in effect_sizes.items():
                print(f"  {metric}: d = {d_value:.3f}")
        
        print("=" * 70 + "\n")


if __name__ == "__main__":
    print("Analysis module loaded. Use with PerformanceTracker instance.")
