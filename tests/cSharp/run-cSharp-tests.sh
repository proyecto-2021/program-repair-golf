#!/bin/bash

pytest --cov=app/cSharp --cov-branch --cov-report=html ./tests/cSharp
