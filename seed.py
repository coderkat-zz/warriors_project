import model

db = model.connect_db()

user = model.new_user(db, 'smith@mediasmith.com', 'warriors123', 'David Smith')
gary_id = model.new_participant(db, 'Gary', 18)
smith_id = model.new_participant(db, 'Smith', 15)
art_id = model.new_participant(db, 'Art', 15)
ken_id = model.new_participant(db, 'Ken', 9)
steve_d_id = model.new_participant(db, 'Steve Dinetz', 9)
steve_n_id = model.new_participant(db, 'Steve Neely', 6)
jay_id = model.new_participant(db, 'Jay', 4)
gilbert_id = model.new_participant(db, 'Gilbert', 3)
stein_id = model.new_participant(db, 'Stein', 2)
cate_id = model.new_participant(db, 'Cate', 1)