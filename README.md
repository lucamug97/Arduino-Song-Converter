# Arduino-Song-Converter
Tutorial to convert midi to be playable by Arduino.

# Step 1: Download midi file
You can download midi file searching #song name# midi on google

# Step 2: Convert MIDI file to xml
You can convert midi file in xml using online website like [this](http://flashmusicgames.com/midi/mid2xml.php).
I suggest to use [musescore](https://musescore.org/it/download) because with this you can also edit the musical score.

Considering that arduino has only one buzzer it can play only one note, so you have to use musical score that have one note at beat. With musescore you can edit score and keep only one of these notes.

In musescore you can export in xml by clicking on File -> Export... -> Select **File MusicXML uncompressed (.musicxml)**

# Step 3: Convert to Arduino NOTEs
Insert the Converter.py file and your .musicxml file in the same directory.
Execute the Converter.py file.
It create .txt file in which you can find notes and durations

# Example
Inside example directory you can find some song already converted
