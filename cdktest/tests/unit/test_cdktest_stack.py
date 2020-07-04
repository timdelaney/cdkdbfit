import json
import pytest

from aws_cdk import core
from cdktest.cdktest_stack import CdktestStack


def get_template():
    app = core.App()
    CdktestStack(app, "cdktest")
    return json.dumps(app.synth().get_stack("cdktest").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
