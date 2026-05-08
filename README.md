# anker_c200

The idea is to gain control of the camera and install thingino without opening the camera.

I had already gained knowledge on how the camera works by opening it, dumping the complete firmware, and opening a remote shell.

But I wanted to find a method to do so without touching it.

What I knew was that an Android Debug Bridge (ADB) could be opened. And to open it, you had to modify a configuration file.

What I thought then was, if I could get an official OTA file, if it could be modified and flashed to the camera, then I can activate ADB.

But my camera was already at the latest firmware version and the AnkerWorks application would not let me get the OTA.


## Getting the OTA

This AnkerWorks windows PC application allows to set the camera up and update it.

The idea here is to obtain an OTA file from the camera by tricking AnkerWorks.

Anker works is an Electron app, thus can be launched with debugging tools attached:

```bash
C:\Users\m4mmon\AppData\Local\Programs\AnkerWork\AnkerWork.exe --remote-debugging-port=9222
```

Then open a browser and go to http://localhost:9222/

Select the first instance of Anker Works, go to the "Sources" and under the "no domain" category, look for the "preload.js" embedded into the app.asar file.

Open it and "pretty print" it.


AnkerWorks gets to know if a device needs an update by sending a payload to a server with the device details like the product code and the firmware version.

So what I did was set a breakpoint in the method "manuallyRequestNewVersion".
There I could access the object representing the camera and alter the version member by issuing the following in the debugging console:
```
this.version = "0.1"
```

I then just had to look at the responses, the server immediately provides the complete URL to the OTA update :) on some amazonaws server.

At the time of writing, the filename is "1683172794421534_Kiva_anker_update_package_c200_7.5_230423171038.img".

You can also find the requests and responses in the file "C:\Users\m4mmon\AppData\Roaming\AnkerWork\logs\renderer.log".

So, I downloaded it for further analysis, and also let AnkerWorks perform the update,which went perfectly fine.

Note that it is only 12MB, it does not contain the bootloader and some other parts.


## flashing the OTA

Here I will not enter into too many details. What happened is that I used an LLM to assist me reconstructing a flashing tool for the camera.

When using AnkerWorks, a lot of info is written into log files located in C:\Users\m4mmon\AppData\Roaming\AnkerWork\logs.
The most important one is awdevice.log.

It tells everything about what happens when the camera is updated.

Without too many details, the flashing process is like:
- send a special command to the camera tmake it enter into update mode,
- the camera in update mode disconnects as an UVC device (the webcam) and declares itself as a serial port,
- the AnkerWorks app waits for the serial port to be present,
- the AnkerWorks app sends chunks of the OTA with a temporary header indicating the checksum of the chunk,
- once every 2000 chunks, the camera sends an "ACK" message containing the index of the last received chunk, AnkerWorks waits for it and checks it,
- when the last chunk has been sent, the camera will send an ACK with a different byte somewhere.

Once the transfer is done, *alea jacta est*, the camera reboots itself and the bootloader applies the OTA.
Hopefully at the end, the updated camera restarts becomes again an UVC device and works again.

So with the help of the LLM a python script was written to handle all this.

**I tried to make it as safe as possible, I have used it myself numerous times, but cannot guarantee it will not brick your camera.**

## patching the OTA

Thanks Anker, the OTA is not encrypted or anything. It can be extracted and rebuilt, exactly what we need to do.
