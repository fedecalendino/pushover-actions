import os
import argparse

import requests


def main():
    parser = argparse.ArgumentParser(
        description="Pushover Notifications",
    )

    parser.add_argument(
        "--status",
        type=str,
        help="the current status of the job",
    )
    parser.add_argument(
        "--message",
        type=str,
        help="your message",
    )
    parser.add_argument(
        "--device",
        type=str,
        help="the name of one of your devices to send just to that device instead of all devices (multiple devices may be separated by a comma)",
    )
    parser.add_argument(
        "--priority",
        type=str,
        help="a value of -2, -1, 0 (default), 1, or 2 (https://pushover.net/api#priority)",
    )
    parser.add_argument(
        "--sound",
        type=str,
        help="the name of a supported sound to override your default sound choice (https://pushover.net/api#sounds)",
    )
    parser.add_argument(
        "--title",
        type=str,
        help="your message's title, otherwise your app's name is used",
    )
    parser.add_argument(
        "--ttl",
        type=str,
        help="a number of seconds that the message will live, before being deleted automatically",
    )
    parser.add_argument(
        "--url", type=str, help="a supplementary URL to show with your message"
    )
    parser.add_argument(
        "--url_title",
        type=str,
        help="a title for the URL specified as the url parameter, otherwise just the URL is shown",
    )

    args = parser.parse_args()

    try:
        token = os.environ["PUSHOVER_TOKEN"]
        user = os.environ["PUSHOVER_USER"]
        repo = "Repo: " + os.environ["GITHUB_REPOSITORY"]
        sha = "Commit: " + os.environ["GITHUB_SHA"][:8]
        ref = "Ref: " + os.environ["GITHUB_REF"] if "GITHUB_REF" in os.environ else ""

        status = "Status: " + args.status if args.status else ""

        message = args.message if args.message else ""
        message = "\n".join([m for m in [repo, sha, ref, status, message] if m])

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        payload = {
            "user": user,
            "token": token,
            "message": message,
            "device": args.device,
            "priority": args.priority,
            "sound": args.sound,
            "title": args.title,
            "ttl": args.ttl,
            "url": args.url,
            "url_title": args.url_title,
        }

        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            headers=headers,
            data=payload,
            timeout=60,
        )

        response.raise_for_status()

        print(response.text)
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    main()
