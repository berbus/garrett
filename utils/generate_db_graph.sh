#!/bin/bash

# Add 'django_extensions' to installed apps
# brew install graphviz
# pip install graphviz
python manage.py graph_models -a -o myapp_models.png
