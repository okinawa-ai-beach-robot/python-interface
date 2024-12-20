from beachbot.utils.github import download
from beachbot.config import config

def test_github_download():
    local_path = "roarm_m1_recorder_3finger.ttt"
    # See also config.BEACHBOT_HARDWARE_REPO
    repo = "okinawa-ai-beach-robot/beach-cleaning-hardware"
    remote_path = "models/coppeliasim/roarm_m1_recorder_3finger.ttt"  # File path in the repo
    branch = "pr2"  # Specify the branch name
    github_token = None  # Provide your GitHub token here if needed
    download(local_path, repo, remote_path, branch, github_token)

