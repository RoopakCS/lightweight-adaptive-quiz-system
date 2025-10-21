"""
Visualization Module
Creates plots and visualizations for analyzing quiz system performance.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class VisualizationEngine:
    """Creates visualizations for quiz system analysis."""
    
    def __init__(self, output_dir='results'):
        """
        Initialize visualization engine.
        
        Args:
            output_dir: Directory to save plots
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
    
    def plot_learning_progression(self, tracker, learner_ids=None, save=True):
        """
        Plot learning progression over sessions for selected learners.
        
        Args:
            tracker: PerformanceTracker instance
            learner_ids: List of learner IDs to plot (None = plot all)
            save: Whether to save the plot
        """
        sessions_df = tracker.get_all_sessions_df()
        
        if sessions_df.empty:
            print("No session data available for plotting.")
            return
        
        # Filter learners if specified
        if learner_ids:
            sessions_df = sessions_df[sessions_df['learner_id'].isin(learner_ids)]
        
        # Create subplot
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Learning Progression Across Sessions', fontsize=16, fontweight='bold')
        
        # Plot 1: Accuracy over sessions
        ax1 = axes[0, 0]
        for quiz_type in ['adaptive', 'non-adaptive']:
            data = sessions_df[sessions_df['quiz_type'] == quiz_type]
            if not data.empty:
                # Group by learner and calculate mean across sessions
                grouped = data.groupby('learner_id')['accuracy'].apply(list)
                
                # Calculate average trajectory
                max_sessions = max(len(sessions) for sessions in grouped)
                session_accuracies = []
                
                for i in range(max_sessions):
                    session_acc = [sessions[i] for sessions in grouped if i < len(sessions)]
                    if session_acc:
                        session_accuracies.append(np.mean(session_acc))
                
                ax1.plot(range(1, len(session_accuracies) + 1), session_accuracies, 
                        marker='o', linewidth=2, label=quiz_type.capitalize())
        
        ax1.set_xlabel('Session Number')
        ax1.set_ylabel('Accuracy')
        ax1.set_title('Accuracy Improvement Over Sessions')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Mastery Index over sessions
        ax2 = axes[0, 1]
        for quiz_type in ['adaptive', 'non-adaptive']:
            data = sessions_df[sessions_df['quiz_type'] == quiz_type]
            if not data.empty:
                grouped = data.groupby('learner_id')['mastery_index'].apply(list)
                
                max_sessions = max(len(sessions) for sessions in grouped)
                session_mastery = []
                
                for i in range(max_sessions):
                    session_mast = [sessions[i] for sessions in grouped if i < len(sessions)]
                    if session_mast:
                        session_mastery.append(np.mean(session_mast))
                
                ax2.plot(range(1, len(session_mastery) + 1), session_mastery,
                        marker='s', linewidth=2, label=quiz_type.capitalize())
        
        ax2.set_xlabel('Session Number')
        ax2.set_ylabel('Mastery Index')
        ax2.set_title('Mastery Progression Over Sessions')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Average time per question
        ax3 = axes[1, 0]
        for quiz_type in ['adaptive', 'non-adaptive']:
            data = sessions_df[sessions_df['quiz_type'] == quiz_type]
            if not data.empty:
                grouped = data.groupby('learner_id')['avg_time_per_question'].apply(list)
                
                max_sessions = max(len(sessions) for sessions in grouped)
                session_times = []
                
                for i in range(max_sessions):
                    session_time = [sessions[i] for sessions in grouped if i < len(sessions)]
                    if session_time:
                        session_times.append(np.mean(session_time))
                
                ax3.plot(range(1, len(session_times) + 1), session_times,
                        marker='^', linewidth=2, label=quiz_type.capitalize())
        
        ax3.set_xlabel('Session Number')
        ax3.set_ylabel('Avg Time per Question (seconds)')
        ax3.set_title('Response Time Trend')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Difficulty changes (adaptive only)
        ax4 = axes[1, 1]
        adaptive_data = sessions_df[sessions_df['quiz_type'] == 'adaptive']
        if not adaptive_data.empty:
            grouped = adaptive_data.groupby('learner_id')['difficulty_changes'].apply(list)
            
            max_sessions = max(len(sessions) for sessions in grouped)
            session_changes = []
            
            for i in range(max_sessions):
                session_change = [sessions[i] for sessions in grouped if i < len(sessions)]
                if session_change:
                    session_changes.append(np.mean(session_change))
            
            ax4.plot(range(1, len(session_changes) + 1), session_changes,
                    marker='D', linewidth=2, color='green', label='Adaptive')
        
        ax4.set_xlabel('Session Number')
        ax4.set_ylabel('Number of Difficulty Changes')
        ax4.set_title('Adaptive Adjustments Per Session')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'learning_progression.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.show()
    
    def plot_comparison_boxplot(self, tracker, save=True):
        """
        Create box plots comparing adaptive vs non-adaptive performance.
        
        Args:
            tracker: PerformanceTracker instance
            save: Whether to save the plot
        """
        sessions_df = tracker.get_all_sessions_df()
        
        if sessions_df.empty:
            print("No session data available for plotting.")
            return
        
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        fig.suptitle('Adaptive vs Non-Adaptive Performance Comparison', 
                    fontsize=16, fontweight='bold')
        
        # Accuracy comparison
        ax1 = axes[0]
        sessions_df.boxplot(column='accuracy', by='quiz_type', ax=ax1)
        ax1.set_title('Accuracy Distribution')
        ax1.set_xlabel('Quiz Type')
        ax1.set_ylabel('Accuracy')
        ax1.get_figure().suptitle('')
        
        # Mastery index comparison
        ax2 = axes[1]
        sessions_df.boxplot(column='mastery_index', by='quiz_type', ax=ax2)
        ax2.set_title('Mastery Index Distribution')
        ax2.set_xlabel('Quiz Type')
        ax2.set_ylabel('Mastery Index')
        ax2.get_figure().suptitle('')
        
        # Time comparison
        ax3 = axes[2]
        sessions_df.boxplot(column='avg_time_per_question', by='quiz_type', ax=ax3)
        ax3.set_title('Avg Time per Question')
        ax3.set_xlabel('Quiz Type')
        ax3.set_ylabel('Time (seconds)')
        ax3.get_figure().suptitle('')
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'comparison_boxplot.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.show()
    
    def plot_difficulty_distribution(self, tracker, save=True):
        """
        Plot distribution of question difficulties encountered.
        
        Args:
            tracker: PerformanceTracker instance
            save: Whether to save the plot
        """
        questions_df = tracker.get_all_questions_df()
        sessions_df = tracker.get_all_sessions_df()
        
        if questions_df.empty:
            print("No question data available for plotting.")
            return
        
        # Merge to get quiz type for each question
        merged = questions_df.merge(
            sessions_df[['session_id', 'quiz_type']], 
            on='session_id'
        )
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle('Question Difficulty Distribution', fontsize=16, fontweight='bold')
        
        # Count plot
        ax1 = axes[0]
        difficulty_order = ['easy', 'medium', 'hard']
        sns.countplot(data=merged, x='difficulty', hue='quiz_type', 
                     order=difficulty_order, ax=ax1)
        ax1.set_title('Number of Questions by Difficulty')
        ax1.set_xlabel('Difficulty Level')
        ax1.set_ylabel('Count')
        
        # Accuracy by difficulty
        ax2 = axes[1]
        difficulty_acc = merged.groupby(['quiz_type', 'difficulty'])['correct'].mean().reset_index()
        
        for quiz_type in ['adaptive', 'non-adaptive']:
            data = difficulty_acc[difficulty_acc['quiz_type'] == quiz_type]
            data = data.set_index('difficulty').reindex(difficulty_order)
            ax2.plot(data.index, data['correct'], marker='o', 
                    linewidth=2, label=quiz_type.capitalize())
        
        ax2.set_title('Accuracy by Difficulty Level')
        ax2.set_xlabel('Difficulty Level')
        ax2.set_ylabel('Accuracy')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'difficulty_distribution.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.show()
    
    def plot_learner_comparison(self, tracker, num_learners=6, save=True):
        """
        Compare individual learner performance.
        
        Args:
            tracker: PerformanceTracker instance
            num_learners: Number of learners to display
            save: Whether to save the plot
        """
        sessions_df = tracker.get_all_sessions_df()
        
        if sessions_df.empty:
            print("No session data available for plotting.")
            return
        
        # Select subset of learners
        learner_ids = sessions_df['learner_id'].unique()[:num_learners]
        filtered_df = sessions_df[sessions_df['learner_id'].isin(learner_ids)]
        
        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        fig.suptitle('Individual Learner Performance Comparison', 
                    fontsize=16, fontweight='bold')
        
        for idx, learner_id in enumerate(learner_ids):
            if idx >= 6:
                break
            
            ax = axes[idx // 3, idx % 3]
            learner_data = filtered_df[filtered_df['learner_id'] == learner_id]
            
            for quiz_type in ['adaptive', 'non-adaptive']:
                data = learner_data[learner_data['quiz_type'] == quiz_type].sort_values('start_time')
                if not data.empty:
                    sessions = range(1, len(data) + 1)
                    ax.plot(sessions, data['accuracy'].values, 
                           marker='o', label=quiz_type.capitalize())
            
            ax.set_title(f'{learner_id}')
            ax.set_xlabel('Session')
            ax.set_ylabel('Accuracy')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
            ax.set_ylim([0, 1])
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'learner_comparison.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.show()
    
    def plot_statistical_summary(self, stats, save=True):
        """
        Create a visual summary of key statistics.
        
        Args:
            stats: Dictionary from tracker.get_comparison_stats()
            save: Whether to save the plot
        """
        if not stats:
            print("No statistics available for plotting.")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle('Statistical Summary: Adaptive vs Non-Adaptive', 
                    fontsize=16, fontweight='bold')
        
        # Bar chart of key metrics
        ax1 = axes[0]
        metrics = ['Accuracy', 'Mastery Index', 'Difficulty Changes']
        adaptive_values = [
            stats['adaptive']['mean_accuracy'],
            stats['adaptive']['mean_mastery'],
            stats['adaptive']['mean_difficulty_changes']
        ]
        non_adaptive_values = [
            stats['non_adaptive']['mean_accuracy'],
            stats['non_adaptive']['mean_mastery'],
            stats['non_adaptive']['mean_difficulty_changes']
        ]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        ax1.bar(x - width/2, adaptive_values, width, label='Adaptive', color='#2ecc71')
        ax1.bar(x + width/2, non_adaptive_values, width, label='Non-Adaptive', color='#e74c3c')
        
        ax1.set_ylabel('Value')
        ax1.set_title('Key Performance Metrics')
        ax1.set_xticks(x)
        ax1.set_xticklabels(metrics)
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Improvement percentages
        ax2 = axes[1]
        improvements = ['Accuracy\nImprovement', 'Mastery\nImprovement']
        improvement_values = [
            stats.get('accuracy_improvement', 0),
            stats.get('mastery_improvement', 0)
        ]
        
        colors = ['#2ecc71' if v > 0 else '#e74c3c' for v in improvement_values]
        bars = ax2.bar(improvements, improvement_values, color=colors, alpha=0.7)
        
        ax2.set_ylabel('Improvement (%)')
        ax2.set_title('Adaptive vs Non-Adaptive Improvement')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom' if height > 0 else 'top')
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'statistical_summary.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.show()
    
    def generate_all_plots(self, tracker):
        """
        Generate all visualization plots.
        
        Args:
            tracker: PerformanceTracker instance
        """
        print("Generating visualizations...")
        
        print("\n1. Learning Progression Plot")
        self.plot_learning_progression(tracker)
        
        print("\n2. Comparison Box Plot")
        self.plot_comparison_boxplot(tracker)
        
        print("\n3. Difficulty Distribution Plot")
        self.plot_difficulty_distribution(tracker)
        
        print("\n4. Learner Comparison Plot")
        self.plot_learner_comparison(tracker)
        
        print("\n5. Statistical Summary Plot")
        stats = tracker.get_comparison_stats()
        self.plot_statistical_summary(stats)
        
        print(f"\nAll plots saved to '{self.output_dir}' directory")


if __name__ == "__main__":
    print("Visualization module loaded. Use with PerformanceTracker instance.")
