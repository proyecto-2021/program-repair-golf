#!/bin/bash

pytest --cov=app/cSharp --cov-branch --cov-report=html -vv ./tests/cSharp
