import os

# Project directory
ProjectDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data storage directory
dataDir = os.path.join(ProjectDir, 'data')

# Initial database path
initDB_Path = os.path.join(dataDir, 'init.db')

# Configuration file storage directory
etcDir = os.path.join(ProjectDir, 'etc')

# Configuration file path
policyPath = os.path.join(etcDir, 'Policy.txt')
