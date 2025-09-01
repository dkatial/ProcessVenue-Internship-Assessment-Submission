from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import List, Optional

# ----------------- DATABASE SETUP -----------------
DB_FILE = "database.db"
engine = create_engine(f"sqlite:///{DB_FILE}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ----------------- DATABASE MODELS -----------------
class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    education = Column(Text)
    github = Column(String)
    linkedin = Column(String)
    portfolio = Column(String)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"))
    skill_name = Column(String)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"))
    title = Column(String)
    description = Column(Text)
    links = Column(Text)

class Work(Base):
    __tablename__ = "work"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"))
    company = Column(String)
    role = Column(String)
    duration = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# ----------------- FASTAPI SETUP -----------------
app = FastAPI(title="Me-API Playground")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ----------------- Pydantic MODELS -----------------
class ProjectModel(BaseModel):
    title: str
    description: str
    links: str

class WorkModel(BaseModel):
    company: str
    role: str
    duration: str

class ProfileModel(BaseModel):
    name: str
    email: str
    education: str
    github: Optional[str] = ""
    linkedin: Optional[str] = ""
    portfolio: Optional[str] = ""
    skills: List[str]
    projects: List[ProjectModel]
    work: List[WorkModel]

# ----------------- ENDPOINTS -----------------

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Create or update profile
@app.post("/profile")
def create_profile(profile: ProfileModel):
    db = SessionLocal()
    # Clear old data
    db.query(Skill).delete()
    db.query(Project).delete()
    db.query(Work).delete()
    db.query(Profile).delete()
    db.commit()

    # Insert profile
    db_profile = Profile(
        name=profile.name,
        email=profile.email,
        education=profile.education,
        github=profile.github,
        linkedin=profile.linkedin,
        portfolio=profile.portfolio
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    # Insert skills
    for skill in profile.skills:
        db.add(Skill(profile_id=db_profile.id, skill_name=skill))

    # Insert projects
    for p in profile.projects:
        db.add(Project(profile_id=db_profile.id, title=p.title, description=p.description, links=p.links))

    # Insert work
    for w in profile.work:
        db.add(Work(profile_id=db_profile.id, company=w.company, role=w.role, duration=w.duration))

    db.commit()
    db.close()
    return {"message": "Profile saved successfully"}

# Get profile
@app.get("/profile")
def get_profile():
    db = SessionLocal()
    db_profile = db.query(Profile).first()
    if not db_profile:
        db.close()
        return {"name": "", "email": "", "education": "", "github": "", "linkedin": "", "portfolio": "", "skills": [], "projects": [], "work": []}

    # Fetch skills
    skills = [s.skill_name for s in db.query(Skill).filter(Skill.profile_id == db_profile.id).all()]

    # Fetch projects
    projects = [
        {"title": p.title, "description": p.description, "links": p.links}
        for p in db.query(Project).filter(Project.profile_id == db_profile.id).all()
    ]

    # Fetch work
    work = [
        {"company": w.company, "role": w.role, "duration": w.duration}
        for w in db.query(Work).filter(Work.profile_id == db_profile.id).all()
    ]
    db.close()
    return {
        "name": db_profile.name,
        "email": db_profile.email,
        "education": db_profile.education,
        "github": db_profile.github,
        "linkedin": db_profile.linkedin,
        "portfolio": db_profile.portfolio,
        "skills": skills,
        "projects": projects,
        "work": work
    }

# Query projects by skill
@app.get("/projects")
def get_projects_by_skill(skill: str = Query(..., description="Skill to filter projects")):
    db = SessionLocal()
    db_profile = db.query(Profile).first()
    if not db_profile:
        db.close()
        return []

    # Check if skill exists
    skills = [s.skill_name.lower() for s in db.query(Skill).filter(Skill.profile_id == db_profile.id).all()]
    if skill.lower() not in skills:
        db.close()
        return []

    projects = [
        {"title": p.title, "description": p.description, "links": p.links}
        for p in db.query(Project).filter(Project.profile_id == db_profile.id).all()
    ]
    db.close()
    return [p for p in projects if skill.lower() in p["description"].lower() or skill.lower() in p["title"].lower()]

# Top skills endpoint
@app.get("/skills/top")
def get_top_skills():
    db = SessionLocal()
    db_profile = db.query(Profile).first()
    if not db_profile:
        db.close()
        return []
    skills = [s.skill_name for s in db.query(Skill).filter(Skill.profile_id == db_profile.id).all()]
    db.close()
    return skills

# Search endpoint (projects, skills, work)
@app.get("/search")
def search(q: str = Query(..., description="Search query")):
    db = SessionLocal()
    db_profile = db.query(Profile).first()
    if not db_profile:
        db.close()
        return []

    results = []

    # Search skills
    skills = [s.skill_name for s in db.query(Skill).filter(Skill.profile_id == db_profile.id).all()]
    results.extend([{"type": "skill", "name": s} for s in skills if q.lower() in s.lower()])

    # Search projects
    projects = db.query(Project).filter(Project.profile_id == db_profile.id).all()
    results.extend([{"type": "project", "title": p.title, "description": p.description} for p in projects if q.lower() in p.title.lower() or q.lower() in p.description.lower()])

    # Search work
    work = db.query(Work).filter(Work.profile_id == db_profile.id).all()
    results.extend([{"type": "work", "company": w.company, "role": w.role} for w in work if q.lower() in w.company.lower() or q.lower() in w.role.lower()])

    db.close()
    return results
