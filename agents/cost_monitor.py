#!/usr/bin/env python3
"""
Cloud Cost Monitor Agent for Artemis CodexOps.
- Checks AWS for running paid resources (RDS, EC2, etc).
- Notifies (print, email, webhook, or SMS) if any billable instance found.
"""
import os, boto3

def notify(msg):
    print("COST ALERT:", msg)
    # Optionally: integrate with email, Slack, webhook, etc.

def check_aws_costs():
    try:
        rds = boto3.client("rds")
        dbs = rds.describe_db_instances()
        for db in dbs.get("DBInstances", []):
            if db["DBInstanceStatus"] == "available":
                notify(f"RDS instance running: {db['DBInstanceIdentifier']}")
        ec2 = boto3.client("ec2")
        running = ec2.describe_instances(Filters=[{"Name":"instance-state-name","Values":["running"]}])
        for r in running["Reservations"]:
            for inst in r["Instances"]:
                notify(f"EC2 instance running: {inst['InstanceId']}")
    except Exception as e:
        print("AWS Cost Monitor error:", e)

if __name__ == "__main__":
    check_aws_costs()
