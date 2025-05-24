import pytest
from WorkerThreads.TextExtractWorker import TextExtractWorker

def test_text_extract_worker_initialization():
    """Test that TextExtractWorker can be initialized."""
    worker = TextExtractWorker()
    assert worker is not None

def test_text_extract_worker_attributes():
    """Test basic attributes of TextExtractWorker."""
    worker = TextExtractWorker()
    assert hasattr(worker, 'queue')
    assert hasattr(worker, 'thread')