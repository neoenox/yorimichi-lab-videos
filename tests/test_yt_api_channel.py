"""Offline channel-identity safety tests; no real YouTube API calls."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import yt_api


class ChannelGuardTests(unittest.TestCase):
    def setUp(self):
        self.yt = MagicMock()
        self.yt.videos().list().execute.return_value = {
            "items": [{"status": {"privacyStatus": "private", "embeddable": True},
                       "snippet": {"title": "existing", "description": "old"}}]
        }
        self.yt.videos().update().execute.return_value = {
            "status": {"privacyStatus": "private", "publishAt": "2026-11-03T10:00:00.000Z"}
        }
        self.yt.reset_mock()
        self.service_patch = patch.object(yt_api, "service", return_value=self.yt)
        self.mine_patch = patch.object(yt_api, "mine", return_value=[{"id": yt_api.CHANNEL_ID}])
        self.service_patch.start()
        self.mock_mine = self.mine_patch.start()
        self.addCleanup(self.service_patch.stop)
        self.addCleanup(self.mine_patch.stop)

        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / "upload" / "pack").mkdir(parents=True)
        (root / "upload" / "pack" / "description.txt").write_text("updated", encoding="utf8")
        root_patch = patch.object(yt_api, "R", root)
        ids_patch = patch.object(yt_api, "load_ids", return_value={"pack": {"video_id": "video123"}})
        root_patch.start()
        ids_patch.start()
        self.addCleanup(root_patch.stop)
        self.addCleanup(ids_patch.stop)

    def assert_no_video_access(self):
        self.yt.videos.assert_not_called()

    def test_schedule_wrong_channel_aborts_before_video_access(self):
        self.mock_mine.return_value = [{"id": "wrong-channel"}]
        with self.assertRaises(SystemExit):
            yt_api.cmd_schedule("video123", "2026-11-03 19:00")
        self.assert_no_video_access()

    def test_schedule_no_channel_aborts_before_video_access(self):
        self.mock_mine.return_value = []
        with self.assertRaises(SystemExit):
            yt_api.cmd_schedule("video123", "2026-11-03 19:00")
        self.assert_no_video_access()

    def test_schedule_channel_lookup_error_aborts_before_video_access(self):
        self.mock_mine.side_effect = RuntimeError("channel lookup unavailable")
        with self.assertRaises(RuntimeError):
            yt_api.cmd_schedule("video123", "2026-11-03 19:00")
        self.assert_no_video_access()

    def test_schedule_matching_channel_can_update(self):
        yt_api.cmd_schedule("video123", "2026-11-03 19:00")
        self.mock_mine.assert_called_once_with(self.yt)
        self.yt.videos().update.assert_called_once()
        self.assertEqual(self.yt.videos().update.call_args.kwargs["body"]["id"], "video123")

    def test_redesc_wrong_channel_aborts_before_video_access(self):
        self.mock_mine.return_value = [{"id": "wrong-channel"}]
        with self.assertRaises(SystemExit):
            yt_api.cmd_redesc("pack")
        self.assert_no_video_access()

    def test_redesc_no_channel_aborts_before_video_access(self):
        self.mock_mine.return_value = []
        with self.assertRaises(SystemExit):
            yt_api.cmd_redesc("pack")
        self.assert_no_video_access()

    def test_redesc_channel_lookup_error_aborts_before_video_access(self):
        self.mock_mine.side_effect = RuntimeError("channel lookup unavailable")
        with self.assertRaises(RuntimeError):
            yt_api.cmd_redesc("pack")
        self.assert_no_video_access()

    def test_redesc_matching_channel_can_update(self):
        yt_api.cmd_redesc("pack")
        self.mock_mine.assert_called_once_with(self.yt)
        self.yt.videos().update.assert_called_once()
        self.assertEqual(self.yt.videos().update.call_args.kwargs["body"]["snippet"]["description"], "updated")


if __name__ == "__main__":
    unittest.main()
