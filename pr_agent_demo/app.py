import os
from dotenv import load_dotenv
from httpx import get
from pr_agent import cli
from pr_agent.config_loader import get_settings
import sys

load_dotenv()

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def set_review_settings():
    get_settings().set("pr_reviewer.require_score_review", True)
    get_settings().set("pr_reviewer.require_tests_review", True)
    get_settings().set("pr_reviewer.require_estimate_effort_to_review", True)
    get_settings().set("pr_reviewer.require_security_review", True)
    get_settings().set("pr_reviewer.require_ticket_analysis_review", True)
    get_settings().set("pr_reviewer.persistent_comment", True)
    get_settings().set("pr_reviewer.final_update_message", True)
    get_settings().set("pr_reviewer.enable_review_labels_security", True)
    get_settings().set("pr_reviewer.enable_review_labels_effort", True)
    get_settings().set("pr_reviewer.enable_intro_text", True)
    get_settings().set("pr_reviewer.enable_help_text", False)
    get_settings().set("pr_reviewer.enable_auto_approval", False)
    get_settings().set("pr_review_prompt.system", read_file("settings/pr_reviewer_prompt.txt"))
    

def main():
    if len(sys.argv) < 3:
        raise ValueError("No PR URL provided. Please provide a PR URL as the second argument.")
    
    pr_url = sys.argv[2]
    command = sys.argv[1]
    
    # Setting the configurations
    get_settings().set("CONFIG.git_provider", "github")
    get_settings().set("anthropic.key", os.getenv("ANTHROPIC_KEY"))
    get_settings().set("github.user_token", os.getenv("GITHUB_USER_TOKEN"))
    get_settings().set("config.model", "anthropic/claude-3-5-sonnet-20241022")
    get_settings().set("config.fallback_models", ["anthropic/claude-3-5-sonnet-20241022"])
    get_settings().set("config.max_model_tokens", 128000)
    get_settings().set("config.custom_model_max_tokens", 200000)
    get_settings().set("config.verbosity_level", 1)
    get_settings().set("config.ai_timeout", 300)
    set_review_settings()
    
    
    # Run the command. Feedback will appear in GitHub PR comments
    cli.run_command(pr_url, command)


if __name__ == '__main__':
    main()