'''
This is a converter to convert (roughly) from music xml files (.mxl) to arduino buzzer code (for tone())

A pitches.h note in arduino code looks like

NOTE_CS4

Where the C is the note, S means sharp, and 4 is the octave

'''
import os
rootdir = os.getcwd()
extensions = ('.xml', '.musicxml')

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            musicFile = open(file) #music xml file
            music = musicFile.read() #str with music data

            writeFile = open(file + ".txt", "w") #file to write code to


            #limit of notes to go into arduino file
            noteLimit = 2000;

            # parallel arrays that will then be converted to arduino code
            notesArr = []
            durationsArr = []

            #for a second voice if there is one
            notesArr2 = []
            durationsArr2 = []

            #to keep track of voice
            currentVoice = 1;

            """function area"""

            """getAttribute(note, "<step>") would return what's between <step> and </step> in the note string"""
            def getAttribute(xmlStr, attribute):
              #if attribute = "<step>"" then attributeEndTag = "</step>""
              attributeEndTag = attribute[:1] + '/' + attribute[1:]
              attributeStart = xmlStr.find(attribute);
              if(attributeStart == -1):
                return -1 #if no attribute, return -1
              attributeEnd = xmlStr.find(attributeEndTag)
              return xmlStr[attributeStart + len(attribute) : attributeEnd]

            def getX(note):
              return note[17:23]

            """converts the given duration 'd' to 8 for 8th note, 4 for quarter note, etc"""
            def realDuration(d):
              #need to change it to work for divisions other than 4

              d = int(d)
              #divisions = duration of quarter note
              divisions = int(getAttribute(music, "<divisions>"))
              #first set it to quarter note
              duration = 4;
              #change it depending on 'd'
              if(d == divisions*4):
                duration = 1;
              if(d == divisions*2):
                duration = 2;
              for i in range(1, 8):
                if(d == divisions/i):
                  duration = 4*i;
              return int(duration)

            def realDuration2(t):
              pass

            #beginning and end of (first) note
            beginNote = music.find("<note")
            endNote = music.find("</note")

            #note string
            note = music[beginNote:endNote+7]
            noteCounter = 0;

            #two notes at same x can't be played since buzzer only plays one note at a time
            usedX = 0
            #for staff 2
            usedX2 = 0

            #loop through notes
            while(endNote != -1):
              noteCounter += 1
              
              """get step from current note and add to note array
                #note: alter 1 means sharp"""
              
              #need to fix copying of code but:
              if(currentVoice == 1):
                #if note is rest note, but skip rests on staff2:
                if(note.find("<rest/>") != -1):
                  notesArr.append("0");
                  duration = getAttribute(note, "<duration>")
                  durationsArr.append(realDuration(duration))
                else:
                  if(getX(note) != usedX):
                    usedX = getX(note)

                    #add note
                    noteLetter = getAttribute(note, "<step>")
                    alter = getAttribute(note, "<alter>")
                    octave = getAttribute(note, "<octave>")

                    if(alter == "1"):
                      noteLetter += "S"
                    noteLetter += octave

                    notesArr.append("NOTE_" + str(noteLetter))

                    #add duration
                    duration = getAttribute(note, "<duration>")
                    durationsArr.append(realDuration(duration))
              else:
                #if note is rest note:
                if(note.find("<rest/>") != -1):
                  notesArr2.append("0");
                  duration = getAttribute(note, "<duration>")
                  durationsArr2.append(realDuration(duration))
                else:
                  if(getX(note) != usedX2):
                    usedX2 = getX(note)

                    noteLetter = getAttribute(note, "<step>")
                    alter = getAttribute(note, "<alter>")
                    octave = getAttribute(note, "<octave>")

                    if(alter == "1"):
                      noteLetter += "S"
                    noteLetter += octave

                    notesArr2.append("NOTE_" + str(noteLetter))

                    duration = getAttribute(note, "<duration>")
                    durationsArr2.append(realDuration(duration))

              """USE EITHER FROM CODE ARCHIVE DEPENDING ON MUSIC
              *Since this is a WIP file, I haven't explained this very well*"""
              #skip staff 2, have to work that in later
              if(music[endNote+14 : endNote+22] == "<backup>"):
                nextMeasure = music.find("<measure", endNote+1)
                beginNote = music.find("<note", nextMeasure)
                endNote = music.find("</note", nextMeasure)
              else:
                beginNote = music.find("<note", endNote+1)
                endNote = music.find("</note", endNote+1)

              """move on to next note"""
              note = music[beginNote:endNote+7]

            writeFile.write(musicFile.name)

            """Write voice 1"""

            writeFile.write("\n\n <<VOICE 1>> \n\n")

            if(noteLimit > len(notesArr)):
              noteLimit = len(notesArr)
              writeFile.write("NOTES LIMIT CHANGED TO" + str(noteLimit) + "! (MAX)")

            writeFile.write("NUMBER OF NOTES: " + str(noteLimit) + "\n\n")

            for i in range(0, noteLimit):
              writeFile.write(notesArr[i] + ", ")
              if(i % 10 == 0):
                writeFile.write("\n")

            writeFile.write("\n\n <<durations>> \n\n")

            for i in range(0, noteLimit):
              writeFile.write(str(durationsArr[i]) + ", ")
              if(i % 10 == 0):
                writeFile.write("\n")

            """Write voice 2"""
            #will be length of notesArr 2

            writeFile.write("\n\n <<VOICE 2>> \n\n")

            if(noteLimit > len(notesArr2)):
              noteLimit = len(notesArr2)
              writeFile.write("!!!!!!!WARNING NOTE NUMBERS DON'T MATCH!!!!!!!")

            writeFile.write("NUMBER OF NOTES: " + str(noteLimit) + "\n\n")

            for i in range(0, noteLimit):
              writeFile.write(notesArr2[i] + ", ")
              if(i % 10 == 0):
                writeFile.write("\n")

            writeFile.write("\n\n <<durations>> \n\n")

            for i in range(0, noteLimit):
              writeFile.write(str(durationsArr2[i]) + ", ")
              if(i % 10 == 0):
                writeFile.write("\n")

            writeFile.close()




            """Code archive

            #skip staff 2, have to work that in later
              if(music[endNote+14 : endNote+22] == "<backup>"):
                nextMeasure = music.find("<measure", endNote+1)
                beginNote = music.find("<note", nextMeasure)
                endNote = music.find("</note", nextMeasure)
              else:
                beginNote = music.find("<note", endNote+1)
                endNote = music.find("</note", endNote+1)


            #if going into staff 2 switch voice
              if(music[endNote+14 : endNote+22] == "<backup>"):
                currentVoice = 2
              #if exiting staff 2 switch voice
              if("measu" in music[beginNote-50: beginNote-(25)]):
                currentVoice = 1
            beginNote = music.find("<note", endNote+1)
            endNote = music.find("</note", endNote+1)

            """
