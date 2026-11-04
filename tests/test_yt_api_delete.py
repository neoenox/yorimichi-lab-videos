"""Offline regression tests: never call the real YouTube API."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import yt_api


class DeleteSupersededSafetyTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.ledger = Path(temp.name) / "youtube_ids.json"
        self.write_ledger(["old1"])
        self.yt = MagicMock()
        self.yt.channels().list().execute.return_value = {
            "items": [{"id": yt_api.CHANNEL_ID}]
        }
        self.yt.videos().list().execute.return_value = {
            "items": [{"status": {"privacyStatus": "private"}, "snippet": {"title": "old version"}}]
        }
        self.yt.videos().delete().execute.return_value = {}
        ids_patch = patch.object(yt_api, "IDS", self.ledger)
        service_patch = patch.object(yt_api, "service", return_value=self.yt)
        ids_patch.start()
        service_patch.start()
        self.addCleanup(ids_patch.stop)
        self.addCleanup(service_patch.stop)
        # Configuring MagicMock return values invokes videos()/delete() once.
        # Clear setup calls so assert_not_called checks only the tested function.
        self.yt.reset_mock()

    def write_ledger(self, superseded):
        self.ledger.write_text(
            json.dumps({"pack": {"video_id": "current", "superseded": superseded, "deleted": []}}),
            encoding="utf8",
        )

    def read_ledger(self):
        return json.loads(self.ledger.read_text(encoding="utf8"))["pack"]

    def test_confirmed_deletion_updates_ledger(self):
        yt_api.cmd_delete_superseded()
        self.assertEqual(self.read_ledger()["superseded"], [])
        self.assertEqual(self.read_ledger()["deleted"], ["old1"])
        self.assertFalse(self.ledger.with_name(self.ledger.name + ".tmp").exists())

    def test_delete_failure_keeps_video_pending(self):
        self.yt.videos().delete().execute.side_effect = PermissionError("forbidden")
        with self.assertRaises(SystemExit):
            yt_api.cmd_delete_superseded()
        self.assertEqual(self.read_ledger()["superseded"], ["old1"])
        self.assertEqual(self.read_ledger()["deleted"], [])

    def test_empty_list_response_is_not_proof_of_deletion(self):
        self.yt.videos().list().execute.return_value = {"items": []}
        with self.assertRaises(SystemExit):
            yt_api.cmd_delete_superseded()
        self.assertEqual(self.read_ledger()["superseded"], ["old1"])
        self.yt.videos().delete.assert_not_called()

    def test_non_private_video_is_not_deleted(self):
        self.yt.videos().list().execute.return_value = {
            "items": [{"status": {"privacyStatus": "public"}, "snippet": {"title": "public"}}]
        }
        with self.assertRaises(SystemExit):
            yt_api.cmd_delete_superseded()
        self.assertEqual(self.read_ledger()["superseded"], ["old1"])
        self.yt.videos().delete.assert_not_called()

    def test_wrong_channel_aborts_before_lookup(self):
        self.yt.channels().list().execute.return_value = {"items": [{"id": "other-channel"}]}
        with self.assertRaises(SystemExit):
            yt_api.cmd_delete_superseded()
        self.assertEqual(self.read_ledger()["superseded"], ["old1"])
        self.yt.videos().list.assert_not_called()

    def test_partial_success_persists_only_confirmed_deletion(self):
        self.write_ledger(["old1", "old2"])
        self.yt.videos().delete().execute.side_effect = [{}, RuntimeError("HTTP 500")]
        with self.assertRaises(SystemExit):
            yt_api.cmd_delete_superseded()
        self.assertEqual(self.read_ledger()["superseded"], ["old2"])
        self.assertEqual(self.read_ledger()["deleted"], ["old1"])

    def test_atomic_save_failure_preserves_existing_ledger(self):
        original = self.ledger.read_bytes()
        with patch("os.replace", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                yt_api.cmd_delete_superseded()
        self.assertEqual(self.ledger.read_bytes(), original)
        self.assertEqual(list(self.ledger.parent.glob("youtube_ids.json.*.tmp")), [])

    def test_quota_error_preserves_pending_entries(self):
        self.write_ledger(["old1", "old2"])
        self.yt.videos().list().execute.side_effect = RuntimeError("quotaExceeded")
        with self.assertRaises(SystemExit):
            yt_api.cmd_delete_superseded()
        self.assertEqual(self.read_ledger()["superseded"], ["old1", "old2"])
        self.yt.videos().delete.assert_not_called()


if __name__ == "__main__":
    unittest.main()
