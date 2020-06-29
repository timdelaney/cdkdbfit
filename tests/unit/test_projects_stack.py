import json
import pytest

from aws_cdk import core
from projects.projects_stack import ProjectsStack


def get_template():
    app = core.App()
    ProjectsStack(app, "projects")
    return json.dumps(app.synth().get_stack("projects").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
