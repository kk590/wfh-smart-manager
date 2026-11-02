from sqlmodel import Session
from maindb import engine, User, Team, create_db_and_tables

def populate():
    create_db_and_tables()
    with Session(engine) as session:
        # Clear existing
        for u in session.query(User).all():
            session.delete(u)
        for t in session.query(Team).all():
            session.delete(t)
        session.commit()

        eng = Team(name="Engineering", headquarters="Building A")
        sales = Team(name="Sales", headquarters="Building B")
        session.add(eng)
        session.add(sales)
        session.commit()

        alice = User(name="Alice", email="alice@example.com", role="admin", team_id=eng.id)
        bob = User(name="Bob", email="bob@example.com", role="manager", team_id=eng.id, manager_id=None)
        charlie = User(name="Charlie", email="charlie@example.com", role="employee", team_id=eng.id, manager_id=bob.id)
        session.add(alice)
        session.add(bob)
        session.add(charlie)
        session.commit()
        print("Data populated.")

if __name__ == "__main__":
    populate()
