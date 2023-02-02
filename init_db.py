from app import app, db, Drucker, Toner, DruTo, User

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        initDB = [
            Drucker(id=1, model="P 501"),
            Drucker(id=2, model="IM C400"),
            Drucker(id=3, model="IM C3000"),
            Drucker(id=4, model="SP C352dn"),
            Drucker(id=5, model="IM C4500"),
            Toner(id=1, name="BL", count=0),
            Toner(id=2, name="RT", count=0),
            Toner(id=3, name="BL", count=0),
            Toner(id=4, name="CY", count=0),
            Toner(id=5, name="MA", count=0),
            Toner(id=6, name="YE", count=0),
            Toner(id=7, name="BL", count=0),
            Toner(id=8, name="CY", count=0),
            Toner(id=9, name="MA", count=0),
            Toner(id=10, name="YE", count=0),
            Toner(id=11, name="RT", count=0),
            Toner(id=12, name="BL", count=0),
            Toner(id=13, name="CY", count=0),
            Toner(id=14, name="MA", count=0),
            Toner(id=15, name="YE", count=0),
            Toner(id=16, name="RT", count=0),
            Toner(id=17, name="BL", count=0),
            Toner(id=18, name="CY", count=0),
            Toner(id=19, name="MA", count=0),
            Toner(id=20, name="YE", count=0),
            DruTo(id=1, drucker=1, toner=1),
            DruTo(id=2, drucker=1, toner=2),
            DruTo(id=3, drucker=2, toner=3),
            DruTo(id=4, drucker=2, toner=4),
            DruTo(id=5, drucker=2, toner=5),
            DruTo(id=6, drucker=2, toner=6),
            DruTo(id=7, drucker=3, toner=7),
            DruTo(id=8, drucker=3, toner=8),
            DruTo(id=9, drucker=3, toner=9),
            DruTo(id=10, drucker=3, toner=10),
            DruTo(id=11, drucker=3, toner=11),
            DruTo(id=12, drucker=4, toner=12),
            DruTo(id=13, drucker=4, toner=13),
            DruTo(id=14, drucker=4, toner=14),
            DruTo(id=15, drucker=4, toner=15),
            DruTo(id=16, drucker=4, toner=16),
            DruTo(id=17, drucker=5, toner=17),
            DruTo(id=18, drucker=5, toner=18),
            DruTo(id=19, drucker=5, toner=19),
            DruTo(id=20, drucker=5, toner=20),
            DruTo(id=21, drucker=5, toner=11)
        ]
        db.session.bulk_save_objects(initDB)
        db.session.commit()

    with app.app_context():
        User(id=1, username="wenzelf", password="")
