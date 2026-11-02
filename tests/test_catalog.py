import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from maintidoc_dataset.catalog import topic_for_filename


def test_isolation_metadata():
    topic = topic_for_filename("04_hv_isolation_faults.pdf")
    assert topic.system == "HIGH_VOLTAGE"
    assert "22280F" in topic.dtc_codes


def test_airbag_metadata():
    topic = topic_for_filename("35_airbag_warning_faults.pdf")
    assert topic.system == "SAFETY"
    assert "930904" in topic.dtc_codes
