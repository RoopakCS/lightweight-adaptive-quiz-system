"""
Performance Tracker Module
Tracks and manages learner performance data across quiz sessions.
"""

import pandas as pd
import numpy as np
from datetime import datetime


class PerformanceTracker:
    """Tracks learner performance metrics throughout quiz sessions."""
    
    def __init__(self):
        """Initialize performance tracker."""
        self.session_data = []
        self.question_data = []
        
    def record_session_start(self, learner_id, session_id, quiz_type, initial_difficulty='medium'):
        """
        Record the start of a quiz session.
        
        Args:
            learner_id: Unique learner identifier
            session_id: Unique session identifier
            quiz_type: 'adaptive' or 'non-adaptive'
            initial_difficulty: Starting difficulty level
        """
        session_record = {
            'learner_id': learner_id,
            'session_id': session_id,
            'quiz_type': quiz_type,
            'initial_difficulty': initial_difficulty,
            'start_time': datetime.now(),
            'questions_answered': 0,
            'correct_answers': 0,
            'total_time': 0.0,
            'difficulty_progression': [initial_difficulty]
        }
        
        self.session_data.append(session_record)
        
    def record_question_response(self, learner_id, session_id, question_id, 
                                 correct, time_taken, difficulty, topic):
        """
        Record a single question response.
        
        Args:
            learner_id: Learner identifier
            session_id: Session identifier
            question_id: Question identifier
            correct: Whether answer was correct
            time_taken: Time taken to answer (seconds)
            difficulty: Question difficulty level
            topic: Question topic
        """
        question_record = {
            'learner_id': learner_id,
            'session_id': session_id,
            'question_id': question_id,
            'correct': correct,
            'time_taken': time_taken,
            'difficulty': difficulty,
            'topic': topic,
            'timestamp': datetime.now()
        }
        
        self.question_data.append(question_record)
        
        # Update session data
        for session in self.session_data:
            if session['learner_id'] == learner_id and session['session_id'] == session_id:
                session['questions_answered'] += 1
                if correct:
                    session['correct_answers'] += 1
                session['total_time'] += time_taken
                if difficulty != session['difficulty_progression'][-1]:
                    session['difficulty_progression'].append(difficulty)
                break
    
    def finalize_session(self, learner_id, session_id, mastery_index):
        """
        Finalize a session with computed metrics.
        
        Args:
            learner_id: Learner identifier
            session_id: Session identifier
            mastery_index: Computed mastery index
        """
        for session in self.session_data:
            if session['learner_id'] == learner_id and session['session_id'] == session_id:
                session['end_time'] = datetime.now()
                session['mastery_index'] = mastery_index
                
                # Compute derived metrics
                if session['questions_answered'] > 0:
                    session['accuracy'] = session['correct_answers'] / session['questions_answered']
                    session['avg_time_per_question'] = session['total_time'] / session['questions_answered']
                else:
                    session['accuracy'] = 0.0
                    session['avg_time_per_question'] = 0.0
                
                session['difficulty_changes'] = len(session['difficulty_progression']) - 1
                break
    
    def get_session_summary(self, learner_id, session_id):
        """Get summary statistics for a specific session."""
        for session in self.session_data:
            if session['learner_id'] == learner_id and session['session_id'] == session_id:
                return session
        return None
    
    def get_learner_history(self, learner_id):
        """Get all session data for a specific learner."""
        return [s for s in self.session_data if s['learner_id'] == learner_id]
    
    def get_all_sessions_df(self):
        """Get all session data as a pandas DataFrame."""
        if not self.session_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.session_data)
        return df
    
    def get_all_questions_df(self):
        """Get all question response data as a pandas DataFrame."""
        if not self.question_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.question_data)
        return df
    
    def get_comparison_stats(self):
        """
        Compare adaptive vs non-adaptive quiz performance.
        
        Returns:
            Dictionary with comparison statistics
        """
        df = self.get_all_sessions_df()
        
        if df.empty:
            return {}
        
        adaptive_sessions = df[df['quiz_type'] == 'adaptive']
        non_adaptive_sessions = df[df['quiz_type'] == 'non-adaptive']
        
        stats = {
            'adaptive': {
                'mean_accuracy': adaptive_sessions['accuracy'].mean() if not adaptive_sessions.empty else 0,
                'mean_mastery': adaptive_sessions['mastery_index'].mean() if not adaptive_sessions.empty else 0,
                'mean_time_per_question': adaptive_sessions['avg_time_per_question'].mean() if not adaptive_sessions.empty else 0,
                'mean_difficulty_changes': adaptive_sessions['difficulty_changes'].mean() if not adaptive_sessions.empty else 0,
                'total_sessions': len(adaptive_sessions)
            },
            'non_adaptive': {
                'mean_accuracy': non_adaptive_sessions['accuracy'].mean() if not non_adaptive_sessions.empty else 0,
                'mean_mastery': non_adaptive_sessions['mastery_index'].mean() if not non_adaptive_sessions.empty else 0,
                'mean_time_per_question': non_adaptive_sessions['avg_time_per_question'].mean() if not non_adaptive_sessions.empty else 0,
                'mean_difficulty_changes': non_adaptive_sessions['difficulty_changes'].mean() if not non_adaptive_sessions.empty else 0,
                'total_sessions': len(non_adaptive_sessions)
            }
        }
        
        # Calculate improvement percentages
        if stats['non_adaptive']['mean_accuracy'] > 0:
            stats['accuracy_improvement'] = (
                (stats['adaptive']['mean_accuracy'] - stats['non_adaptive']['mean_accuracy']) / 
                stats['non_adaptive']['mean_accuracy'] * 100
            )
        else:
            stats['accuracy_improvement'] = 0
            
        if stats['non_adaptive']['mean_mastery'] > 0:
            stats['mastery_improvement'] = (
                (stats['adaptive']['mean_mastery'] - stats['non_adaptive']['mean_mastery']) / 
                stats['non_adaptive']['mean_mastery'] * 100
            )
        else:
            stats['mastery_improvement'] = 0
        
        return stats
    
    def export_to_csv(self, output_dir='data'):
        """Export tracking data to CSV files."""
        sessions_df = self.get_all_sessions_df()
        questions_df = self.get_all_questions_df()
        
        if not sessions_df.empty:
            # Convert difficulty_progression list to string for CSV
            sessions_df['difficulty_progression'] = sessions_df['difficulty_progression'].apply(
                lambda x: ','.join(x) if isinstance(x, list) else str(x)
            )
            sessions_df.to_csv(f'{output_dir}/session_results.csv', index=False)
            print(f"Session data exported to {output_dir}/session_results.csv")
        
        if not questions_df.empty:
            questions_df.to_csv(f'{output_dir}/question_responses.csv', index=False)
            print(f"Question data exported to {output_dir}/question_responses.csv")
    
    def get_learning_progression(self, learner_id):
        """
        Get learning progression for a learner across sessions.
        
        Returns:
            Dictionary with progression metrics
        """
        learner_sessions = sorted(
            [s for s in self.session_data if s['learner_id'] == learner_id],
            key=lambda x: x.get('start_time', datetime.now())
        )
        
        if not learner_sessions:
            return {}
        
        progression = {
            'session_numbers': list(range(1, len(learner_sessions) + 1)),
            'accuracies': [s.get('accuracy', 0) for s in learner_sessions],
            'mastery_indices': [s.get('mastery_index', 0) for s in learner_sessions],
            'avg_times': [s.get('avg_time_per_question', 0) for s in learner_sessions],
            'quiz_types': [s.get('quiz_type', 'unknown') for s in learner_sessions]
        }
        
        return progression
    
    def clear(self):
        """Clear all tracking data."""
        self.session_data = []
        self.question_data = []


if __name__ == "__main__":
    # Test performance tracker
    tracker = PerformanceTracker()
    
    # Simulate a session
    tracker.record_session_start('learner_001', 'session_001', 'adaptive', 'easy')
    tracker.record_question_response('learner_001', 'session_001', 1, True, 15.5, 'easy', 'Math')
    tracker.record_question_response('learner_001', 'session_001', 2, True, 18.2, 'medium', 'Math')
    tracker.finalize_session('learner_001', 'session_001', 1.5)
    
    print("Session summary:")
    print(tracker.get_session_summary('learner_001', 'session_001'))
