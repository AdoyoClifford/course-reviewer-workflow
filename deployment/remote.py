import os
import sys
import toml

# Force UTF-8 encoding for console output
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Set UTF-8 encoding for console output on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

import vertexai
from absl import app as absl_app, flags
from dotenv import load_dotenv
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

from reviewer import app

FLAGS = flags.FLAGS
flags.DEFINE_string("project_id", None, "GCP project ID.")
flags.DEFINE_string("location", None, "GCP location.")
flags.DEFINE_string("bucket", None, "GCP bucket.")
flags.DEFINE_string("resource_id", None, "ReasoningEngine resource ID.")
flags.DEFINE_string("user_id", "test_user", "User ID for session operations.")
flags.DEFINE_string("session_id", None, "Session ID for operations.")
flags.DEFINE_bool("create", False, "Creates a new deployment.")
flags.DEFINE_bool("delete", False, "Deletes an existing deployment.")
flags.DEFINE_bool("list", False, "Lists all deployments.")
flags.DEFINE_bool("create_session", False, "Creates a new session.")
flags.DEFINE_bool("list_sessions", False, "Lists all sessions for a user.")
flags.DEFINE_bool("get_session", False, "Gets a specific session.")
flags.DEFINE_bool("send", False, "Sends a message to the deployed agent.")
flags.DEFINE_string(
    "message",
    "Shorten this message: Hello, how are you doing today?",
    "Message to send to the agent.",
)
flags.mark_bool_flags_as_mutual_exclusive(
    [
        "create",
        "delete",
        "list",
        "create_session",
        "list_sessions",
        "get_session",
        "send",
    ]
)



def create() -> None:
    """Creates a new deployment."""
    # Dynamically read dependencies from pyproject.toml
    with open("pyproject.toml", "r") as f:
        pyproject_data = toml.load(f)
    dependencies = pyproject_data["project"]["dependencies"]

    # Now deploy to Agent Engine
    remote_app = agent_engines.create(
        agent_engine=app,
        requirements=dependencies,
        extra_packages=["./reviewer"],
    )
    print(f"Created remote app: {remote_app.resource_name}")


def delete(resource_id: str) -> None:
    """Deletes an existing deployment."""
    try:
        remote_app = agent_engines.get(resource_id)
        remote_app.delete(force=True)
        print(f"Deleted remote app: {resource_id}")
    except Exception as e:
        print(f"Error deleting deployment: {e}")


def list_deployments() -> None:
    """Lists all deployments."""
    deployments = agent_engines.list()
    if not deployments:
        print("No deployments found.")
        return
    print("Deployments:")
    for deployment in deployments:
        print(f"- {deployment.resource_name}")


def create_session(resource_id: str, user_id: str) -> None:
    """Creates a new session for the specified user."""
    try:
        remote_app = agent_engines.get(resource_id)
        remote_session = remote_app.create_session(user_id=user_id)
        print("Created session:")
        print(f"  Session ID: {remote_session.get('id')}")
        print(f"  User ID: {remote_session.get('user_id', 'N/A')}")
        print(f"  App name: {remote_session.get('app_name', 'N/A')}")
        print(f"  Last update time: {remote_session.get('last_update_time', 'N/A')}")
        print("\nUse this session ID with --session_id when sending messages.")
    except Exception as e:
        print(f"Error creating session: {e}")


def list_sessions(resource_id: str, user_id: str) -> None:
    """Lists all sessions for the specified user."""
    try:
        remote_app = agent_engines.get(resource_id)
        sessions = remote_app.list_sessions(user_id=user_id)
        print(f"Sessions for user '{user_id}':")
        for session in sessions:
            print(f"- Session ID: {session['id']}")
    except Exception as e:
        print(f"Error listing sessions: {e}")


def get_session(resource_id: str, user_id: str, session_id: str) -> None:
    """Gets a specific session."""
    try:
        remote_app = agent_engines.get(resource_id)
        session = remote_app.get_session(user_id=user_id, session_id=session_id)
        print("Session details:")
        print(f"  ID: {session.get('id')}")
        print(f"  User ID: {session.get('user_id', 'N/A')}")
        print(f"  App name: {session.get('app_name', 'N/A')}")
        print(f"  Last update time: {session.get('last_update_time', 'N/A')}")
    except Exception as e:
        print(f"Error getting session: {e}")


def send_message(resource_id: str, user_id: str, session_id: str, message: str) -> None:
    """Sends a message to the deployed agent."""
    try:
        remote_app = agent_engines.get(resource_id)

        print(f"Sending message to session {session_id}:")
        # Handle Unicode characters safely
        try:
            print("Message:", message)
        except UnicodeEncodeError:
            # Safely encode Unicode characters for Windows console
            safe_message = message.encode('utf-8', errors='replace').decode('utf-8')
            print("Message:", safe_message)
        print("\nResponse:")
        for event in remote_app.stream_query(
            user_id=user_id,
            session_id=session_id,
            message=message,
        ):
            try:
                print(event)
            except UnicodeEncodeError:
                # Safely encode Unicode characters for Windows console
                safe_event = str(event).encode('utf-8', errors='replace').decode('utf-8')
                print(safe_event)
    except Exception as e:
        print(f"Error sending message: {e}")


def main(argv=None):
    """Main function that can be called directly or through app.run()."""
    # Parse flags first
    if argv is None:
        argv = flags.FLAGS(sys.argv)
    else:
        argv = flags.FLAGS(argv)

    load_dotenv()

    # Now we can safely access the flags
    project_id = (
        FLAGS.project_id if FLAGS.project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
    )
    location = FLAGS.location if FLAGS.location else os.getenv("GOOGLE_CLOUD_LOCATION")
    bucket = FLAGS.bucket if FLAGS.bucket else os.getenv("GOOGLE_CLOUD_STAGING_BUCKET")
    user_id = FLAGS.user_id

    if not project_id:
        print("Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        return
    elif not location:
        print("Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        return
    elif not bucket:
        print("Missing required environment variable: GOOGLE_CLOUD_STAGING_BUCKET")
        return

    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=bucket,
    )

    if FLAGS.create:
        create()
    elif FLAGS.delete:
        if not FLAGS.resource_id:
            print("resource_id is required for delete")
            return
        delete(FLAGS.resource_id)
    elif FLAGS.list:
        list_deployments()
    elif FLAGS.create_session:
        if not FLAGS.resource_id:
            print("resource_id is required for create_session")
            return
        create_session(FLAGS.resource_id, user_id)
    elif FLAGS.list_sessions:
        if not FLAGS.resource_id:
            print("resource_id is required for list_sessions")
            return
        list_sessions(FLAGS.resource_id, user_id)
    elif FLAGS.get_session:
        if not FLAGS.resource_id:
            print("resource_id is required for get_session")
            return
        if not FLAGS.session_id:
            print("session_id is required for get_session")
            return
        get_session(FLAGS.resource_id, user_id, FLAGS.session_id)
    elif FLAGS.send:
        if not FLAGS.resource_id:
            print("resource_id is required for send")
            return
        if not FLAGS.session_id:
            print("session_id is required for send")
            return
        
        message_to_send = FLAGS.message
        # If content is piped, read from stdin
        if not sys.stdin.isatty():
            stdin_message = sys.stdin.read().strip()
            if stdin_message:
                message_to_send = stdin_message

        send_message(FLAGS.resource_id, user_id, FLAGS.session_id, message_to_send)
    else:
        print(
            "Please specify one of: --create, --delete, --list, --create_session, --list_sessions, --get_session, or --send"
        )


if __name__ == "__main__":
    absl_app.run(main)

    