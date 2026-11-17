import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import create_access_token, get_password_hash
from app.main import app
from app.models import (
    User,
    SystemThreshold,
    Aisle,
    AGV,
    BottleneckAlert,
    Report,
    SimulationScenario,
    AuditLog
)

# In-memory SQLite for complete test isolation
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def seed_test_database(db):
    """Seed minimal realistic fixtures for tests."""
    admin_user = User(
        id="USR-TEST-01",
        username="admin",
        name="Test Administrator",
        email="admin@test.twinflow.ai",
        hashed_password=get_password_hash("admin123"),
        role="admin",
        status="Active",
        access_level="Full Administrative Access",
        last_login="Just now"
    )
    operator_user = User(
        id="USR-TEST-02",
        username="operator",
        name="Test Operator",
        email="operator@test.twinflow.ai",
        hashed_password=get_password_hash("operator123"),
        role="user",
        status="Active",
        access_level="Floor Lead Operations",
        last_login="10 mins ago"
    )
    db.add_all([admin_user, operator_user])

    # Threshold
    threshold = SystemThreshold(moderate=40, high=70, critical=85)
    db.add(threshold)

    # Aisles
    aisles = [
        Aisle(id="AISLE-A", name="Aisle A - Fast Movers", zone="Zone 1", capacity=120, current_occupancy=45, status="Optimal", x=12.5, y=34.0),
        Aisle(id="AISLE-B", name="Aisle B - High Density Racks", zone="Zone 2", capacity=150, current_occupancy=132, status="Congested", x=24.0, y=34.0),
        Aisle(id="AISLE-C", name="Aisle C - Reserve Storage", zone="Zone 3", capacity=100, current_occupancy=30, status="Optimal", x=36.0, y=34.0),
        Aisle(id="AISLE-D", name="Aisle D - Cross-Dock Staging", zone="Zone 4", capacity=80, current_occupancy=25, status="Optimal", x=48.0, y=34.0),
    ]
    db.add_all(aisles)

    # AGVs
    agvs = [
        AGV(id="AGV-01", name="Titan-1", status="Moving", battery=94, speed=1.4, current_aisle="AISLE-A", x=10.0, y=20.0),
        AGV(id="AGV-02", name="Titan-2", status="Queued", battery=82, speed=0.0, current_aisle="AISLE-B", x=24.0, y=30.0),
        AGV(id="AGV-03", name="Titan-3", status="Queued", battery=75, speed=0.0, current_aisle="AISLE-B", x=24.0, y=32.0),
    ]
    db.add_all(agvs)

    # Alert
    alert = BottleneckAlert(
        id="ALT-101",
        severity="Critical",
        title="Severe AGV Gridlock Impending in Aisle B",
        location="Aisle B - Cross Section 4",
        eta="12 mins",
        confidence=94,
        status="Active",
        assigned_to="Sam Haddad",
        created_time="10:15 AM",
        expected_delay="+7.2 min",
        affected_zones=["Zone 2", "Dock Bay 3"],
        root_causes=["Inbound Surge", "Aisle B Bottleneck"]
    )
    db.add(alert)

    # Audit Log
    log = AuditLog(
        id="LOG-001",
        user="system",
        action="Initialized test environment",
        module="Test Suite",
        time="08:00",
        ip="127.0.0.1"
    )
    db.add(log)

    db.commit()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create fresh SQLite tables before test session and drop after."""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    seed_test_database(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    """Provides a transactional database session rolled back after each test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """FastAPI TestClient wired to the test SQLite database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token():
    """Valid JWT token for Administrator."""
    return create_access_token(subject="USR-TEST-01", role="admin")


@pytest.fixture
def operator_token():
    """Valid JWT token for Floor Operator."""
    return create_access_token(subject="USR-TEST-02", role="user")


@pytest.fixture
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def operator_headers(operator_token):
    return {"Authorization": f"Bearer {operator_token}"}
