import csv
import os

from datetime import datetime

INCIDENT_TYPES = {
    "access": "Access Issue (login/permissions)",
    "network": "Network Failure (connectivity/VPN)",
    "service": "System Service Down (app/server stopped)",
    "phishing": "Phishing / Security Alert"
}

PRIORITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


def normalize(text: str) -> str:
    return text.strip().lower()


def ask_incident_type():
    print("\nChoose incident type:")
    for key, label in INCIDENT_TYPES.items():
        print(f"- {key}: {label}")
    print("- back: Return to main menu")

    while True:
        choice = normalize(input("Type one (access/network/service/phishing/back): "))

        if choice == "back":
            return None

        if choice in INCIDENT_TYPES:
            return choice

        print("Invalid incident type. Try again.")


def ask_impact_level():
    print("\nImpact level:")
    print("1 = Single user")
    print("2 = Multiple users")
    print("3 = Whole department")
    print("4 = Entire company")
    print("Type 'back' to return.")

    while True:
        raw = normalize(input("Enter impact (1-4/back): "))

        if raw == "back":
            return None

        if raw.isdigit():
            level = int(raw)
            if 1 <= level <= 4:
                return level

        print("Invalid impact level. Enter 1-4 or 'back'.")


def ask_yes_no(prompt):
    print("Type 'back' to return.")

    while True:
        ans = normalize(input(prompt))

        if ans == "back":
            return None

        if ans in {"y", "yes"}:
            return True

        if ans in {"n", "no"}:
            return False

        print("Please type y/n or 'back'.")


def calculate_priority(incident_type: str, impact: int, business_blocked: bool) -> str:
    # Base priority by incident type
    if incident_type == "phishing":
        base = "HIGH"
    elif incident_type == "network":
        base = "MEDIUM"
    elif incident_type == "service":
        base = "MEDIUM"
    else:  # access
        base = "LOW"

    # Escalate by impact
    if impact == 4:
        base = "CRITICAL" if incident_type == "network" and business_blocked else "HIGH"
    elif impact == 3:
        if business_blocked and base in {"LOW", "MEDIUM"}:
            base = "HIGH"
    elif impact == 2:
        if business_blocked and base == "LOW":
            base = "MEDIUM"

    # Escalate by business blocked
    if business_blocked:
        if base == "LOW":
            base = "MEDIUM"
        elif base == "MEDIUM":
            base = "HIGH"

    return base


def response_plan(incident_type: str, priority: str) -> list[str]:
    if incident_type == "access":
        steps = [
            "Verify account status (locked/disabled).",
            "Reset password or assist with MFA.",
            "Check group membership / permissions.",
            "Document the fix in the ticket."
        ]
        if priority in {"HIGH", "CRITICAL"}:
            steps.append("Escalate to IT admin if access is blocking a department workflow.")

    elif incident_type == "network":
        steps = [
            "Check if issue is local or widespread (ask affected users).",
            "Test connectivity (ping gateway / DNS).",
            "Check router/switch/VPN status.",
            "Notify users about progress and ETA."
        ]
        if priority in {"HIGH", "CRITICAL"}:
            steps.append("Escalate immediately to senior admin / network team.")

    elif incident_type == "service":
        steps = [
            "Check service status and logs.",
            "Restart service safely (if allowed).",
            "Check server resources (CPU/RAM/disk).",
            "Notify affected department."
        ]
        if priority in {"HIGH", "CRITICAL"}:
            steps.append("Escalate if restart fails or outage affects multiple systems.")

    else:  # phishing
        steps = [
            "Advise user: do not click links, do not reply.",
            "Collect details (sender, subject, time, screenshots).",
            "Isolate affected account if suspicious activity is suspected.",
            "Reset credentials and enforce MFA if needed.",
            "Report to security / compliance team."
        ]
        if priority == "CRITICAL":
            steps.append("Start incident response protocol (possible breach).")

    return steps

def next_incident_id(rows: list[dict]) -> str:
    # rows come from read_incident_log()
    if not rows:
        return "INC-0001"

    last_id = rows[-1].get("id", "INC-0000")
    try:
        num = int(last_id.split("-")[1])
    except Exception:
        num = len(rows)

    return f"INC-{num + 1:04d}"


def log_incident(incident_id: str, timestamp: str, incident_type: str, impact: int, business_blocked: bool, priority: str):
    file_name = "incident_log.csv"
    file_exists = os.path.isfile(file_name)

    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["id", "time", "incident", "impact", "business_blocked", "priority", "status"])

        writer.writerow([incident_id, timestamp, incident_type, impact, business_blocked, priority, "OPEN"])


def read_incident_log():
    file_name = "incident_log.csv"
    if not os.path.isfile(file_name):
        return []

    with open(file_name, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def print_incidents(rows, title="Incident History"):
    print(f"\n=== {title} ===")
    if not rows:
        print("No incidents to show.")
        return

    for i, r in enumerate(rows, start=1):
        print(
    f"{i}. {r.get('id','(no-id)')} | {r['time']} | {r['incident']} | impact={r['impact']} | blocked={r['business_blocked']} | priority={r['priority']} | status={r.get('status','OPEN')}"
)


def history_menu():
    rows = read_incident_log()

    while True:
        print("\nHistory options:")
        print("1) Show ALL incidents")
        print("2) Show only HIGH + CRITICAL")
        print("3) Filter by incident type (access/network/service/phishing)")
        print("4) Back")

        choice = input("Choose 1-4: ").strip()

        if choice == "4":
            return

        if choice == "1":
            print_incidents(rows, "All Incidents")

        elif choice == "2":
            filtered = [r for r in rows if r["priority"] in {"HIGH", "CRITICAL"}]
            print_incidents(filtered, "HIGH + CRITICAL Incidents")

        elif choice == "3":
            t = normalize(input("Type incident (access/network/service/phishing): "))
            filtered = [r for r in rows if r["incident"] == t]
            print_incidents(filtered, f"Incidents: {t}")

        else:
            print("Invalid choice.")


def main():
    print("=== Incident & Response Simulator v3 ===")

    while True:
        print("\nMain menu:")
        print("1) Run new incident")
        print("2) View incident history")
        print("3) Quit")

        choice = input("Choose 1-3: ").strip()

        if choice == "3":
            print("Goodbye!")
            break

        if choice == "2":
            history_menu()
            continue

        if choice != "1":
            print("Invalid choice.")
            continue

        incident_type = ask_incident_type()
        if incident_type is None:
            continue
        impact = ask_impact_level()
        if impact is None:
            continue
        business_blocked = ask_yes_no("Is business blocked? (y/n): ")
        if business_blocked is None:
            continue

        priority = calculate_priority(incident_type, impact, business_blocked)
        rows = read_incident_log()
        incident_id = next_incident_id(rows)
        timestamp = datetime.now().isoformat(timespec="seconds")
        log_incident(incident_id, timestamp, incident_type, impact, business_blocked, priority)


        print("\n--- Summary ---")
        print(f"Time: {timestamp}")
        print(f"Incident: {INCIDENT_TYPES[incident_type]}")
        print(f"Impact: {impact} (1=single user ... 4=company)")
        print(f"Business blocked: {business_blocked}")
        print(f"Priority: {priority}")
        print(f"Incident ID: {incident_id}")

        print("\n--- Response Plan ---")
        for i, step in enumerate(response_plan(incident_type, priority), start=1):
            print(f"{i}. {step}")

        print("\nSaved to incident_log.csv")



if __name__ == "__main__":
    main()
