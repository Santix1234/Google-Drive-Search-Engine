import pytest
from WorkerThreads.DownloadWorker import DownloadWorker

def test_download_worker_initialization():
    """Test that DownloadWorker can be initialized."""
    worker = DownloadWorker()
    assert worker is not None

def test_download_worker_attributes():
    """Test basic attributes of DownloadWorker."""
    worker = DownloadWorker()
    assert hasattr(worker, 'queue')
    assert hasattr(worker, 'thread')