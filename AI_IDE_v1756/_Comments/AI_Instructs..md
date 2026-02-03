───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────|
                 
                                                                                                                          |
Folgende neue Aufteilung soll in den bestehenden Code implementiert werden.
Das QMainWidget behält, den primären, vertikalen Splitter und erhält zusätzlich einen horizontalen Splitter. 
Dem horizontalen Splitter werden links das FilesDockWidget und rechts QTabDockWidget hinzugefügt. 
Alle Widgets und Funktionen bleiben erhalten,
nur die Anordnung Von QDockFilesWidget und QDockTabWidget ändern sich. 
#
Übersicht und Anordnung der Widgets im QMainWindow von links nach rechts,und von oben nach unten. 
# 
Ganz links QFilesWidget, rechts QTabDockWidget, beide im vertikalen Splitter. Mittig, 
in der oberen Hälfte des horizpntalen Splitters die Canvas Area, in der unteren Hälfte das Consolen Widget, 
ganz an der rechten Seite das AIQDockWidget.
                                                                                                                                           
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────|
                                                                                                                                            
     central splitting:
     sketch:            
               ┌<–horizonal-splitter
     ┌─────────|───────────────────────────────────────────┐
     │  horizonal-splitter                                 |     
     │  ┌──────┬──────┬──────────────────────────┬──────┐  | 
     |  │Files | Tab  |         -Canvas-         | AI   │  |
   ─>└──| Dock │ Dock |──── vertical-splitter –––| Dock │──┐<─ vertical-splitter
     │  │      │      |         -Console-        │      │  │
     │  └──────┴──────┴──────────────────────────┴──────┘  │
     |         |                                           |
     └─────────|───────────────────────────────────────────┘
             ->┘                                                                                                                           |
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────|
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘




–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|

┌─────────────────────── Hauptfenster ────────────────────────┐  
│  Files  |  Tabs  |  Canvas / Console (vert. Splitter) | AI  │  
└──────────────────────────────────────────────────────────────┘

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
'''Below is the completely refactored, self-contained Python program that already includes every change described in your “fully refactoring directions”.  
Simply replace your existing file with the code block and run it – nothing else has to be touched.
'''
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
'''Nachstehend findest du nur die Stellen, die geändert bzw. neu hinzugefügt werden mussten.  
Alles andere bleibt unverändert – einfach die Schnipsel in dein bestehendes
Skript übernehmen / ersetzen.'''
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|

## fully refactoring ##
## write a full refactored programm
## full refactoring directions above
## ----------------------------- fully directions --------------------------------------- - 

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
