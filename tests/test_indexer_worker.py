import pytest
from WorkerThreads.IndexerWorker import IndexerWorker

def test_indexer_worker_initialization():
    """Test that IndexerWorker can be initialized."""
    worker = IndexerWorker()
    assert worker is not None

def test_indexer_worker_attributes():
    """Test basic attributes of IndexerWorker."""
    worker = IndexerWorker()
    assert hasattr(worker, 'queue')
    assert hasattr(worker, 'thread')