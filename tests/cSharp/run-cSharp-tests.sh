#!/bin/bash

pytest --cov=app --cov-branch --cov-report=html -vv tests/cSharp
