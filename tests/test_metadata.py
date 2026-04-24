import json
from unittest.mock import MagicMock, patch

from src.metadata import get_camera_info


def test_get_camera_info_with_pipe():
    # Mock data with a pipe in LensModel
    mock_output = json.dumps(
        [
            {
                "Model": "Test Camera",
                "LensModel": "Lens | Model with Pipe",
                "LensID": "Some ID",
            }
        ]
    )

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout=mock_output, returncode=0)

        camera, lens = get_camera_info("fake_path.jpg")

        assert camera == "Test Camera"
        # The goal is to have the pipe replaced by a newline
        assert lens == "Lens \n Model with Pipe"


def test_get_camera_info_no_pipe():
    mock_output = json.dumps(
        [{"Model": "Test Camera", "LensModel": "Normal Lens", "LensID": "Some ID"}]
    )

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout=mock_output, returncode=0)

        camera, lens = get_camera_info("fake_path.jpg")

        assert camera == "Test Camera"
        assert lens == "Normal Lens"


def test_get_camera_info_with_lens_id_and_pipe():
    # Case where LensModel is missing and LensID has a pipe
    mock_output = json.dumps([{"Model": "Test Camera", "LensID": "ID | with Pipe"}])

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout=mock_output, returncode=0)

        camera, lens = get_camera_info("fake_path.jpg")

        assert lens == "ID \n with Pipe"
