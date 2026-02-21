from fastapi import HTTPException
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def check_admin(role: str):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

@app.get("/")
def read_root():
    return {"message": "Governance Backend Running"}


# ----------- SEGMENT LOGIC -----------

def determine_segment(age, occupation):
    occupation = occupation.lower()

    if age < 30:
        return "Youth"
    elif age >= 60:
        return "Senior Citizen"
    elif "farmer" in occupation:
        return "Farmer"
    elif "business" in occupation:
        return "MSME Owner"
    else:
        return "General"


# ----------- BOOTH APIs -----------

@app.post("/booths/")
def create_booth(name: str, ward: str, db: Session = Depends(get_db)):
    booth = models.Booth(name=name, ward=ward)
    db.add(booth)
    db.commit()
    db.refresh(booth)
    return booth


@app.get("/booths/")
def get_booths(db: Session = Depends(get_db)):
    return db.query(models.Booth).all()


# ----------- STREET APIs -----------

@app.post("/streets/")
def create_street(name: str, booth_id: int, db: Session = Depends(get_db)):
    street = models.Street(name=name, booth_id=booth_id)
    db.add(street)
    db.commit()
    db.refresh(street)
    return street


@app.get("/streets/")
def get_streets(db: Session = Depends(get_db)):
    return db.query(models.Street).all()


# ----------- CITIZEN APIs -----------

@app.post("/citizens/")
def create_citizen(
    name: str,
    age: int,
    gender: str,
    mobile: str,
    occupation: str,
    street_id: int,
    consent: bool = True,
    db: Session = Depends(get_db)
):
    segment = determine_segment(age, occupation)

    citizen = models.Citizen(
        name=name,
        age=age,
        gender=gender,
        mobile=mobile,
        occupation=occupation,
        consent=consent,
        segment=segment,
        street_id=street_id
    )

    db.add(citizen)
    db.commit()
    db.refresh(citizen)
    return citizen


@app.get("/citizens/")
def get_citizens(db: Session = Depends(get_db)):
    return db.query(models.Citizen).all()


# ----------- HYPERLOCAL FILTER -----------

@app.get("/streets/{street_id}/citizens")
def get_citizens_by_street(street_id: int, db: Session = Depends(get_db)):
    return db.query(models.Citizen).filter(models.Citizen.street_id == street_id).all()
# ----------- SCHEME APIs -----------

@app.post("/schemes/")
def create_scheme(name: str, description: str, db: Session = Depends(get_db)):
    scheme = models.Scheme(name=name, description=description)
    db.add(scheme)
    db.commit()
    db.refresh(scheme)
    return scheme


@app.get("/schemes/")
def get_schemes(db: Session = Depends(get_db)):
    return db.query(models.Scheme).all()


@app.post("/beneficiaries/")
def add_beneficiary(citizen_id: int, scheme_id: int, db: Session = Depends(get_db)):
    beneficiary = models.Beneficiary(
        citizen_id=citizen_id,
        scheme_id=scheme_id
    )
    db.add(beneficiary)
    db.commit()
    db.refresh(beneficiary)
    return beneficiary
@app.get("/schemes/{scheme_id}/coverage")
def scheme_coverage(scheme_id: int, db: Session = Depends(get_db)):
    total_citizens = db.query(models.Citizen).count()

    total_beneficiaries = db.query(models.Beneficiary).filter(
        models.Beneficiary.scheme_id == scheme_id
    ).count()

    coverage_rate = 0
    if total_citizens > 0:
        coverage_rate = (total_beneficiaries / total_citizens) * 100

    return {
        "scheme_id": scheme_id,
        "total_citizens": total_citizens,
        "beneficiaries": total_beneficiaries,
        "coverage_percentage": round(coverage_rate, 2)
    }
@app.get("/schemes/{scheme_id}/gap-analysis")
def scheme_gap_analysis(scheme_id: int, db: Session = Depends(get_db)):
    
    scheme = db.query(models.Scheme).filter(models.Scheme.id == scheme_id).first()

    if not scheme:
        return {"error": "Scheme not found"}

    # SIMPLE ELIGIBILITY RULES (you can expand later)
    if "farmer" in scheme.name.lower():
        eligible_citizens = db.query(models.Citizen).filter(models.Citizen.segment == "Farmer").all()
    elif "youth" in scheme.name.lower():
        eligible_citizens = db.query(models.Citizen).filter(models.Citizen.segment == "Youth").all()
    else:
        eligible_citizens = db.query(models.Citizen).all()

    eligible_ids = [c.id for c in eligible_citizens]

    beneficiaries = db.query(models.Beneficiary).filter(
        models.Beneficiary.scheme_id == scheme_id
    ).all()

    beneficiary_ids = [b.citizen_id for b in beneficiaries]

    not_covered = list(set(eligible_ids) - set(beneficiary_ids))

    return {
        "scheme_name": scheme.name,
        "eligible_count": len(eligible_ids),
        "beneficiary_count": len(beneficiary_ids),
        "not_covered_count": len(not_covered),
        "gap_percentage": round((len(not_covered) / len(eligible_ids)) * 100, 2) if eligible_ids else 0
    }
@app.get("/booths/{booth_id}/scheme-coverage/{scheme_id}")
def booth_scheme_coverage(booth_id: int, scheme_id: int, db: Session = Depends(get_db)):

    # Get all citizens in that booth
    citizens = db.query(models.Citizen).join(models.Street).filter(
        models.Street.booth_id == booth_id
    ).all()

    total_citizens = len(citizens)
    citizen_ids = [c.id for c in citizens]

    beneficiaries = db.query(models.Beneficiary).filter(
        models.Beneficiary.scheme_id == scheme_id,
        models.Beneficiary.citizen_id.in_(citizen_ids)
    ).all()

    total_beneficiaries = len(beneficiaries)

    coverage = (total_beneficiaries / total_citizens * 100) if total_citizens else 0

    return {
        "booth_id": booth_id,
        "scheme_id": scheme_id,
        "total_citizens": total_citizens,
        "beneficiaries": total_beneficiaries,
        "coverage_percentage": round(coverage, 2)
    }
@app.get("/booths/{booth_id}/street-coverage/{scheme_id}")
def street_level_coverage(booth_id: int, scheme_id: int, db: Session = Depends(get_db)):

    streets = db.query(models.Street).filter(models.Street.booth_id == booth_id).all()

    result = []

    for street in streets:
        citizens = db.query(models.Citizen).filter(
            models.Citizen.street_id == street.id
        ).all()

        total = len(citizens)
        citizen_ids = [c.id for c in citizens]

        beneficiaries = db.query(models.Beneficiary).filter(
            models.Beneficiary.scheme_id == scheme_id,
            models.Beneficiary.citizen_id.in_(citizen_ids)
        ).count()

        coverage = (beneficiaries / total * 100) if total else 0

        result.append({
            "street_id": street.id,
            "street_name": street.name,
            "coverage_percentage": round(coverage, 2)
        })

    return result
from sqlalchemy import func

@app.get("/booths/{booth_id}/segment-distribution")
def segment_distribution(booth_id: int, db: Session = Depends(get_db)):

    distribution = db.query(
        models.Citizen.segment,
        func.count(models.Citizen.id)
    ).join(models.Street).filter(
        models.Street.booth_id == booth_id
    ).group_by(models.Citizen.segment).all()

    return {segment: count for segment, count in distribution}
@app.get("/booths/{booth_id}/summary")
def booth_summary(booth_id: int, db: Session = Depends(get_db)):

    streets = db.query(models.Street).filter(models.Street.booth_id == booth_id).all()
    total_streets = len(streets)

    citizens = db.query(models.Citizen).join(models.Street).filter(
        models.Street.booth_id == booth_id
    ).all()

    total_citizens = len(citizens)

    total_beneficiaries = db.query(models.Beneficiary).join(
        models.Citizen
    ).join(models.Street).filter(
        models.Street.booth_id == booth_id
    ).count()

    return {
        "booth_id": booth_id,
        "total_streets": total_streets,
        "total_citizens": total_citizens,
        "total_beneficiaries": total_beneficiaries
    }
# ----------- ISSUE APIs -----------

@app.post("/issues/")
def create_issue(description: str, category: str, street_id: int, db: Session = Depends(get_db)):
    issue = models.Issue(
        description=description,
        category=category,
        street_id=street_id
    )
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


@app.get("/streets/{street_id}/issues")
def get_street_issues(street_id: int, db: Session = Depends(get_db)):
    return db.query(models.Issue).filter(models.Issue.street_id == street_id).all()
# ----------- NOTIFICATION SIMULATION -----------
@app.post("/notifications/")
def send_notification(street_id: int, message: str, role: str, db: Session = Depends(get_db)):

    check_admin(role)

    citizens = db.query(models.Citizen).filter(
        models.Citizen.street_id == street_id,
        models.Citizen.consent == True
    ).all()

    notification = models.Notification(
        message=message,
        street_id=street_id
    )

    db.add(notification)
    db.commit()

    return {
        "street_id": street_id,
        "message": message,
        "targeted_households": len(citizens)
    }