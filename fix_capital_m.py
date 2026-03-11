import sqlite3
import re

def fix_m(text):
    if not isinstance(text, str): return text
    
    # Do not touch exact Motif Codes
    if re.fullmatch(r'[A-Za-z]\d+', text): return text
    
    # 1. Replace all 'M' with 'm'
    text = text.replace('M', 'm')
    
    # 2. Restore Proper Nouns
    proper_nouns = ['Mack', 'Mexico', 'Mary', 'Michael', 'Michigan', 'Mountbatten', 'March', 'Monday', 'Mac']
    for p in proper_nouns:
        text = re.sub(rf'\b{p.lower()}\b', p, text, flags=re.IGNORECASE)
        
    # 3. Restore 'M.' for Motif family headers (e.g. "m. supernatural" -> "M. supernatural")
    text = re.sub(r'\bm\.\s', 'M. ', text)
    text = re.sub(r'^m\.\s', 'M. ', text)
    
    # 4. Restore sentence capitalization
    text = re.sub(r'(^|[\.\?\!]\s+)([a-z])', lambda match: match.group(1) + match.group(2).upper(), text)
    text = re.sub(r'(^[^a-zA-Z]*)([a-z])', lambda match: match.group(1) + match.group(2).upper(), text)
    
    return text

def run():
    conn = sqlite3.connect('ufo_matrix.db')
    cursor = conn.cursor()
    
    # 1. Motif_Dictionary
    rows = cursor.execute('SELECT motif_number, motif_description, current_family_header, current_family FROM Motif_Dictionary').fetchall()
    for row in rows:
        motif_number = row[0]
        desc = fix_m(row[1])
        cfh = fix_m(row[2])
        cf = fix_m(row[3])
        cursor.execute('''
            UPDATE Motif_Dictionary 
            SET motif_description=?, current_family_header=?, current_family=?
            WHERE motif_number=?
        ''', (desc, cfh, cf, motif_number))
        
    # 2. Encounter_Events
    rows = cursor.execute('SELECT Event_ID, Source_Citation, Emotional_Marker, ai_justification FROM Encounter_Events').fetchall()
    for row in rows:
        eid = row[0]
        cit = fix_m(row[1])
        emo = fix_m(row[2])
        aij = fix_m(row[3])
        cursor.execute('''
            UPDATE Encounter_Events 
            SET Source_Citation=?, Emotional_Marker=?, ai_justification=?
            WHERE Event_ID=?
        ''', (cit, emo, aij, eid))
        
    # 3. Encounters
    rows = cursor.execute('SELECT Encounter_ID, Location_Type, Source_Material FROM Encounters').fetchall()
    for row in rows:
        eid = row[0]
        loc = fix_m(row[1])
        src = fix_m(row[2])
        cursor.execute('''
            UPDATE Encounters 
            SET Location_Type=?, Source_Material=?
            WHERE Encounter_ID=?
        ''', (loc, src, eid))
        
    # 4. Subjects
    rows = cursor.execute('SELECT Subject_ID, Pseudonym FROM Subjects').fetchall()
    for row in rows:
        sid = row[0]
        pseudo = fix_m(row[1])
        cursor.execute('''
            UPDATE Subjects 
            SET Pseudonym=?
            WHERE Subject_ID=?
        ''', (pseudo, sid))
        
    conn.commit()
    conn.close()
    print("Successfully normalized 'M' anomalies across the entire matrix!")

if __name__ == '__main__':
    run()
