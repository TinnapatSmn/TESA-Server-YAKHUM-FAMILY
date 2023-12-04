---Software requirment---
-vb cable virtual audio (https://vb-audio.com/Cable/)
-VTube studio(https://store.steampowered.com/app/1325860/VTube_Studio/)
-Discord or Platform to send output by Camera and Audio

---module requirements---
pip install all in "requirements.txt"
run this
pip install -r "requirements.txt"

---VB cable virtual audio---
install vb cable virtual audio
set speaker output but to CABLE INPUT

---VTube studio---
Import model Vtube model
In Character setting Set mouth open by VoiceVolume
In setting open microphone set to CABLE OUTPUT

---Discord or other Platform---
Open camera from VTuber VTube Studio
set input to CABLE OUTPUT

---Run on terminal(or in VScode)---
1. Activate Environment by run this
    c:/somthing/venv/Scripts/Activate.ps1
2.open terminal in Python
3.Run Sever by this
    py .\server.py   
4. wait until server ready
5. split terminal and run client by this 
    py .\sttclient.py