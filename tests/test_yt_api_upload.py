"""Offline upload ledger tests; all YouTube API and media objects are mocked."""
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import yt_api


class UploadLedgerSafetyTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        pack = self.root / "upload" / "pack"
        pack.mkdir(parents=True)
        (pack / "title.txt").write_text("title", encoding="utf8")
        (pack / "description.txt").write_text("description", encoding="utf8")
        (pack / "tags.txt").write_text("tag", encoding="utf8")
        self.ledger = self.root / "data" / "youtube_ids.json"
        self.ledger.parent.mkdir()
        self.original = {
            "pack": {
                "video_id": "old",
                "privacy": "private",
                "via": "api",
                "superseded": ["older"],
                "deleted": ["already-deleted"],
            }
        }
        self.ledger.write_text(json.dumps(self.original), encoding="utf8")
        package = types.ModuleType("googleapiclient")
        package.__path__ = []
        http = types.ModuleType("googleapiclient.http")
        http.MediaFileUpload = lambda *args, **kwargs: object()
        modules = patch.dict(
            sys.modules, {"googleapiclient": package, "googleapiclient.http": http}
        )
        modules.start()
        self.addCleanup(modules.stop)
        self.yt = MagicMock()
        self.yt.videos().insert().next_chunk.return_value = (
            None, {"id": "new", "status": {"privacyStatus": "private"}}
        )
        self.yt.reset_mock()
        for attr, value in (
            ("R", self.root),
            ("IDS", self.ledger),
            ("service", lambda: self.yt),
            ("mine", lambda yt: [{"id": yt_api.CHANNEL_ID}]),
        ):
            p = patch.object(yt_api, attr, value)
            p.start()
            self.addCleanup(p.stop)

    def read_ledger(self):
        return json.loads(self.ledger.read_text(encoding="utf8"))

    def test_new_version_keeps_deleted_and_superseded_history(self):
        yt_api.cmd_upload("pack", new_version=True)
        rec = self.read_ledger()["pack"]
        self.assertEqual(rec["video_id"], "new")
        self.assertEqual(rec["superseded"], ["older", "old"])
        self.assertEqual(rec["deleted"], ["already-deleted"])
        self.yt.videos().insert.assert_called_once()

    def test_atomic_save_failure_keeps_original_ledger(self):
        with patch("os.replace", side_effect=OSError("disk failure")):
            with self.assertRaises(OSError):
                yt_api.cmd_upload("pack", new_version=True)
        self.assertEqual(self.read_ledger(), self.original)
        self.assertEqual(list(self.ledger.parent.glob("youtube_ids.json.*.tmp")), [])

    def test_duplicate_upload_is_rejected_before_api_call(self):
        with self.assertRaises(SystemExit):
            yt_api.cmd_upload("pack")
        self.assertEqual(self.read_ledger(), self.original)
        self.yt.videos.assert_not_called()

    def test_dry_run_does_not_write_ledger(self):
        yt_api.cmd_upload("pack", dry=True, new_version=True)
        self.assertEqual(self.read_ledger(), self.original)
        self.yt.videos.assert_not_called()

    def test_first_upload_creates_ledger_directory(self):
        self.ledger.unlink()
        self.ledger.parent.rmdir()
        yt_api.cmd_upload("pack")
        rec = self.read_ledger()["pack"]
        self.assertEqual(rec["video_id"], "new")
        self.assertEqual(rec["superseded"], [])
        self.assertEqual(rec["deleted"], [])


if __name__ == "__main__":
    unittest.main()
