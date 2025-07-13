import os
import sys
import subprocess
from absl import app as absl_app, flags
from dotenv import load_dotenv

FLAGS = flags.FLAGS
flags.DEFINE_string("project_id", None, "GCP project ID.")
flags.DEFINE_string("location", None, "GCP location.")
flags.DEFINE_string("service_name", "course-reviewer-app", "Cloud Run service name.")

def main(argv=None):
    """Main function to deploy to Cloud Run."""
    if argv is None:
        argv = flags.FLAGS(sys.argv)
    else:
        argv = flags.FLAGS(argv)

    load_dotenv()

    project_id = FLAGS.project_id if FLAGS.project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
    location = FLAGS.location if FLAGS.location else os.getenv("GOOGLE_CLOUD_LOCATION")

    if not project_id:
        print("Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        return
    elif not location:
        print("Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        return

    command = [
        "gcloud", "run", "deploy", FLAGS.service_name,
        "--source", ".",
        "--project", project_id,
        "--region", location,
        "--allow-unauthenticated",
        "--platform", "managed",
    ]

    print(f"Running command: {' '.join(command)}")
    subprocess.run(command, check=True)

if __name__ == "__main__":
    absl_app.run(main)
