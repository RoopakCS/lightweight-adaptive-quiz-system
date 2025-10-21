"""
Quiz Simulation Module
Runs quiz sessions for learners using adaptive or non-adaptive engines.
"""

import numpy as np
from src.question_bank import QuestionBank
from src.adaptive_engine import AdaptiveEngine, NonAdaptiveEngine
from src.learner_simulation import SimulatedLearner
from src.performance_tracker import PerformanceTracker


class QuizSimulator:
    """Simulates quiz sessions with adaptive or non-adaptive difficulty adjustment."""
    
    def __init__(self, question_bank, adaptive_engine=None, non_adaptive_engine=None):
        """
        Initialize quiz simulator.
        
        Args:
            question_bank: QuestionBank instance
            adaptive_engine: AdaptiveEngine instance (optional)
            non_adaptive_engine: NonAdaptiveEngine instance (optional)
        """
        self.question_bank = question_bank
        self.adaptive_engine = adaptive_engine or AdaptiveEngine()
        self.non_adaptive_engine = non_adaptive_engine or NonAdaptiveEngine()
    
    def run_quiz_session(self, learner, num_questions, quiz_type='adaptive', 
                        initial_difficulty='medium', tracker=None, session_id=None):
        """
        Run a complete quiz session for a learner.
        
        Args:
            learner: SimulatedLearner instance
            num_questions: Number of questions in the session
            quiz_type: 'adaptive' or 'non-adaptive'
            initial_difficulty: Starting difficulty level
            tracker: PerformanceTracker instance (optional)
            session_id: Unique session identifier
            
        Returns:
            Dictionary with session results
        """
        if session_id is None:
            session_id = f"{learner.learner_id}_session_{np.random.randint(10000)}"
        
        # Select engine based on quiz type
        engine = self.adaptive_engine if quiz_type == 'adaptive' else self.non_adaptive_engine
        
        # Initialize tracking
        if tracker:
            tracker.record_session_start(learner.learner_id, session_id, quiz_type, initial_difficulty)
        
        # Session state
        performance_history = []
        current_difficulty = initial_difficulty
        
        # Run through questions
        for i in range(num_questions):
            # Get question of appropriate difficulty
            question = self.question_bank.get_question(difficulty=current_difficulty)
            
            # Learner answers question
            response = learner.answer_question(question)
            
            # Add to performance history
            performance_history.append(response)
            
            # Record response
            if tracker:
                tracker.record_question_response(
                    learner.learner_id,
                    session_id,
                    question['id'],
                    response['correct'],
                    response['time'],
                    response['difficulty'],
                    response['topic']
                )
            
            # Determine next difficulty (for adaptive mode)
            if quiz_type == 'adaptive':
                current_difficulty = engine.get_next_difficulty(performance_history, current_difficulty)
        
        # Calculate final metrics
        mastery_index = engine.calculate_mastery_index(performance_history)
        
        if tracker:
            tracker.finalize_session(learner.learner_id, session_id, mastery_index)
        
        # Compile results
        results = {
            'learner_id': learner.learner_id,
            'session_id': session_id,
            'quiz_type': quiz_type,
            'num_questions': num_questions,
            'performance_history': performance_history,
            'mastery_index': mastery_index,
            'final_accuracy': self._calculate_accuracy(performance_history),
            'avg_time': self._calculate_avg_time(performance_history),
            'difficulty_progression': [p['difficulty'] for p in performance_history]
        }
        
        return results
    
    def _calculate_accuracy(self, performance_history):
        """Calculate overall accuracy."""
        if not performance_history:
            return 0.0
        correct = sum(1 for p in performance_history if p['correct'])
        return correct / len(performance_history)
    
    def _calculate_avg_time(self, performance_history):
        """Calculate average response time."""
        if not performance_history:
            return 0.0
        return np.mean([p['time'] for p in performance_history])


class ExperimentRunner:
    """Runs experiments comparing adaptive vs non-adaptive quiz systems."""
    
    def __init__(self, question_bank=None, num_questions_per_session=20):
        """
        Initialize experiment runner.
        
        Args:
            question_bank: QuestionBank instance (creates default if None)
            num_questions_per_session: Number of questions per quiz session
        """
        self.question_bank = question_bank or QuestionBank(num_questions=100)
        self.num_questions_per_session = num_questions_per_session
        self.tracker = PerformanceTracker()
        self.simulator = QuizSimulator(self.question_bank)
    
    def run_single_learner_experiment(self, learner, num_sessions=5):
        """
        Run experiment for a single learner with both quiz types.
        
        Args:
            learner: SimulatedLearner instance
            num_sessions: Number of sessions to run for each quiz type
            
        Returns:
            Dictionary with results for both quiz types
        """
        results = {
            'adaptive': [],
            'non_adaptive': []
        }
        
        # Run adaptive sessions
        learner.reset()
        for i in range(num_sessions):
            session_id = f"{learner.learner_id}_adaptive_{i+1}"
            result = self.simulator.run_quiz_session(
                learner,
                self.num_questions_per_session,
                quiz_type='adaptive',
                tracker=self.tracker,
                session_id=session_id
            )
            results['adaptive'].append(result)
        
        # Run non-adaptive sessions
        learner.reset()
        for i in range(num_sessions):
            session_id = f"{learner.learner_id}_non_adaptive_{i+1}"
            result = self.simulator.run_quiz_session(
                learner,
                self.num_questions_per_session,
                quiz_type='non-adaptive',
                tracker=self.tracker,
                session_id=session_id
            )
            results['non_adaptive'].append(result)
        
        return results
    
    def run_population_experiment(self, learner_population, num_sessions=5):
        """
        Run experiment for entire learner population.
        
        Args:
            learner_population: LearnerPopulation instance
            num_sessions: Number of sessions per learner per quiz type
            
        Returns:
            Dictionary with aggregate results
        """
        all_results = []
        
        learners = learner_population.get_all_learners()
        total_learners = len(learners)
        
        print(f"Running experiment for {total_learners} learners...")
        
        for idx, learner in enumerate(learners):
            print(f"  Processing learner {idx + 1}/{total_learners}: {learner.learner_id}")
            
            learner_results = self.run_single_learner_experiment(learner, num_sessions)
            all_results.append({
                'learner_id': learner.learner_id,
                'learner_profile': learner.get_profile(),
                'results': learner_results
            })
        
        print("Experiment completed!")
        return all_results
    
    def get_summary_statistics(self):
        """Get summary statistics from all tracked sessions."""
        return self.tracker.get_comparison_stats()
    
    def export_results(self, output_dir='data'):
        """Export all results to CSV files."""
        self.tracker.export_to_csv(output_dir)
    
    def get_tracker(self):
        """Get the performance tracker instance."""
        return self.tracker
    
    def reset(self):
        """Reset the experiment (clear all tracked data)."""
        self.tracker.clear()


def run_quick_demo():
    """Run a quick demonstration of the system."""
    from src.learner_simulation import SimulatedLearner
    
    print("=== LAQS Quick Demo ===\n")
    
    # Create components
    qb = QuestionBank(num_questions=50)
    learner = SimulatedLearner("demo_learner", base_ability=0.6, learning_rate=0.05)
    tracker = PerformanceTracker()
    simulator = QuizSimulator(qb)
    
    # Run adaptive session
    print("Running ADAPTIVE quiz session...")
    adaptive_result = simulator.run_quiz_session(
        learner, 
        num_questions=10, 
        quiz_type='adaptive',
        tracker=tracker,
        session_id='demo_adaptive'
    )
    
    print(f"  Accuracy: {adaptive_result['final_accuracy']:.2%}")
    print(f"  Mastery Index: {adaptive_result['mastery_index']:.2f}")
    print(f"  Difficulty Progression: {' → '.join(adaptive_result['difficulty_progression'][:5])}...")
    
    # Reset and run non-adaptive session
    learner.reset()
    print("\nRunning NON-ADAPTIVE quiz session...")
    non_adaptive_result = simulator.run_quiz_session(
        learner,
        num_questions=10,
        quiz_type='non-adaptive',
        tracker=tracker,
        session_id='demo_non_adaptive'
    )
    
    print(f"  Accuracy: {non_adaptive_result['final_accuracy']:.2%}")
    print(f"  Mastery Index: {non_adaptive_result['mastery_index']:.2f}")
    print(f"  Difficulty Progression: {' → '.join(non_adaptive_result['difficulty_progression'][:5])}...")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    run_quick_demo()
