#!/usr/bin/env python3

from aws_cdk import core

from cdktest.cdktest_stack import CdktestStack


app = core.App()
CdktestStack(app, "cdktest", env={
             'region': 'us-west-2', 'account': '136232051126'})

app.synth()
