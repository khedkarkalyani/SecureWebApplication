import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "dev-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "jwt-secret-key"
    # 🔽 ADD THESE TWO LINES
    GITHUB_CLIENT_ID = "Ov23liytuNLdouTLoGrAE"
    GITHUB_CLIENT_SECRET = "5c8141a6f5bab6969c5ad4094bf32b1eefc94942"
