#!/usr/bin/env python3

from aws_cdk import core

from cdkdbfit.cdkdbfit_stack import cdkdbfitStack


app = core.App()
cdkdbfitStack(app, "cdkdbfit", env={
    'region': 'us-west-2', 'account': '136232051126'})

app.synth()
