"""
Lightweight Adaptive Quiz System (LAQS)
"""

__version__ = "1.0.0"
__author__ = "LAQS Research Team"

from .question_bank import QuestionBank
from .adaptive_engine import AdaptiveEngine, NonAdaptiveEngine
from .learner_simulation import SimulatedLearner, LearnerPopulation
from .quiz_simulation import QuizSimulator, ExperimentRunner
from .performance_tracker import PerformanceTracker
from .visualization import VisualizationEngine
from .analysis import StatisticalAnalyzer

__all__ = [
    'QuestionBank',
    'AdaptiveEngine',
    'NonAdaptiveEngine',
    'SimulatedLearner',
    'LearnerPopulation',
    'QuizSimulator',
    'ExperimentRunner',
    'PerformanceTracker',
    'VisualizationEngine',
    'StatisticalAnalyzer'
]
