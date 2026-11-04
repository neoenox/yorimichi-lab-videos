"""Offline regression tests for finish ledger ordering; never call the real YouTube API."""
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import yt_api


class FinishLedgerSafetyTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.pack_dir = self.root / "upload" / "pack"
        self.pack_dir.mkdir(parents=True)
        (self.pack_dir / "title.txt").write_text("test title", encoding="utf8")
        (self.pack_dir / "description.txt").write_text("test description", encoding="utf8")
        (self.pack_dir / "tags.txt").write_text("tag1,tag2", encoding="utf8")
        self.ledger = self.root / "data" / "youtube_ids.json"
        self.ledger.parent.mkdir()
        self.original = {
            "pack": {
                "video_id": "old",
                "privacy": "private",
                "via": "api",
                "superseded": ["older"],
                "deleted": ["deleted0"],
            }
        }
        self.ledger.write_text(json.dumps(self.original), encoding="utf8")

        # cmd_finish imports MediaFileUpload at call time. Stub it before calling.
        package = types.ModuleType("googleapiclient")
        package.__path__ = []
        http = types.ModuleType("googleapiclient.http")
        http.MediaFileUpload = lambda *args, **kwargs: object()
        module_patch = patch.dict(
            sys.modules, {"googleapiclient": package, "googleapiclient.http": http}
        )
        module_patch.start()
        self.addCleanup(module_patch.stop)

        self.yt = MagicMock()
        self.yt.videos().list().execute.return_value = {
            "items": [{"status": {"publishAt": "2026-11-20T10:00:00Z"}}]
        }
        self.yt.videos().update().execute.return_value = {}
        self.yt.thumbnails().set().execute.return_value = {}
        self.yt.captions().insert().execute.return_value = {}
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

    def assert_original(self):
        self.assertEqual(self.read_ledger(), self.original)

    def test_metadata_update_failure_does_not_supersede_old_video(self):
        self.yt.videos().update().execute.side_effect = RuntimeError("HTTP 500")
        with self.assertRaises(RuntimeError):
            yt_api.cmd_finish("pack", "new")
        self.assert_original()

    def test_thumbnail_failure_does_not_supersede_old_video(self):
        (self.pack_dir / "thumbnail.jpg").write_bytes(b"fake")
        self.yt.thumbnails().set().execute.side_effect = RuntimeError("thumbnail failed")
        with self.assertRaises(RuntimeError):
            yt_api.cmd_finish("pack", "new")
        self.assert_original()

    def test_caption_failure_does_not_supersede_old_video(self):
        (self.pack_dir / "subtitles_ja.srt").write_text("test", encoding="utf8")
        self.yt.captions().insert().execute.side_effect = RuntimeError("caption failed")
        with self.assertRaises(RuntimeError):
            yt_api.cmd_finish("pack", "new")
        self.assert_original()

    def test_success_switches_video_only_after_all_api_steps(self):
        (self.pack_dir / "thumbnail.jpg").write_bytes(b"fake")
        (self.pack_dir / "subtitles_ja.srt").write_text("test", encoding="utf8")
        yt_api.cmd_finish("pack", "new")
        rec = self.read_ledger()["pack"]
        self.assertEqual(rec["video_id"], "new")
        self.assertEqual(rec["superseded"], ["older", "old"])
        self.assertEqual(rec["deleted"], ["deleted0"])
        self.yt.videos().update.assert_called_once()
        self.yt.thumbnails().set.assert_called_once()
        self.yt.captions().insert.assert_called_once()

    def test_same_id_retry_does_not_duplicate_superseded(self):
        yt_api.cmd_finish("pack", "old")
        self.assert_original()

    def test_atomic_replace_failure_preserves_existing_ledger(self):
        with patch("os.replace", side_effect=OSError("disk failure")):
            with self.assertRaises(OSError):
                yt_api.cmd_finish("pack", "new")
        self.assert_original()
        self.assertEqual(list(self.ledger.parent.glob("youtube_ids.json.*.tmp")), [])

    def test_first_pack_creates_missing_data_directory(self):
        self.ledger.unlink()
        self.ledger.parent.rmdir()
        yt_api.cmd_finish("pack", "new")
        self.assertEqual(self.read_ledger()["pack"]["video_id"], "new")
        self.assertEqual(self.read_ledger()["pack"]["superseded"], [])


if __name__ == "__main__":
    unittest.main()
