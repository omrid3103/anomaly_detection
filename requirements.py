import sqlalchemy
from sqlalchemy.orm.session import sessionmaker
import hashlib
import uvicorn
from fastapi import FastAPI
from validate_email import validate_email
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from datetime import datetime, timedelta
import random
import pdfplumber
import csv
import flet as ft
import requests
import time
from typing import Union
import math
import statistics
import datetime
from io import StringIO
from cryptography.fernet import Fernet
import os
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
