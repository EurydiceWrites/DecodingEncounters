import sqlite3

conn = sqlite3.connect('ufo_matrix.db')
conn.execute("UPDATE Motif_Dictionary SET current_family_header = REPLACE(current_family_header, 'THEORHANY', 'THEOPHANY')")
conn.execute("UPDATE Motif_Dictionary SET current_family = REPLACE(current_family, 'THEORHANY', 'THEOPHANY')")
conn.execute("UPDATE Motif_Dictionary SET motif_description = REPLACE(motif_description, 'theorhany', 'theophany')")
conn.commit()
conn.close()
print("Spelling Fixed.")
