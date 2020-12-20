#!/bin/bash

gunicorn -w 3 "app:create_app()"