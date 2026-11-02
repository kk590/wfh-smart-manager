from fastapi import Depends, FastAPI, HTTPException, Query

from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

app = FastAPI()

class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str

class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    users: list["User"] = Relationship(back_populates="team")

class TeamCreate(TeamBase):
    pass

class TeamPublic(TeamBase):
    id: int

class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str
    role: str
    manager_id: int | None = Field(default=None, foreign_key="user.id")
    team_id: int | None = Field(default=None, foreign_key="team.id")

    team: Team | None = Relationship(back_populates="users")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)






class UserBase(SQLModel):
    name: str = Field(index=True)
    email: str
    role: str
    manager_id: int | None = Field(default=None, foreign_key="user.id")
    team_id: int | None = Field(default=None, foreign_key="team.id")





class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    team_id: int | None = None



@app.post("/teams/", response_model=TeamPublic)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.get("/teams/", response_model=list[TeamPublic])
def read_teams(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@app.get("/teams/{team_id}", response_model=TeamPublic)
def read_team(*, team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.patch("/teams/{team_id}", response_model=TeamPublic)
def update_team(
    *,
    session: Session = Depends(get_session),
    team_id: int,
    team: TeamUpdate,
):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.model_dump(exclude_unset=True)
    db_team.sqlmodel_update(team_data)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.delete("/teams/{team_id}")
def delete_team(*, session: Session = Depends(get_session), team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}
