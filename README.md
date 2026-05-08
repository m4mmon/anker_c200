# anker_c200

The idea is to gain control of the camera and install thingino on it.

I had already gained knowledge on how the camera works by opening it, dumping the complete firmware, and getting a remote shell.

But I wanted to find a method to do so without touching it. That front glass is very brittle...

What I knew was that an Android Debug Bridge (ADB) could be opened. And to open it, you had to modify a configuration file.

What I thought then was, if I could get an official OTA file, if it could be modified and flashed to the camera, then I could activate ADB.

But my camera was already at the latest firmware version and the AnkerWorks application would not let me get the OTA.


## Getting the OTA image

This AnkerWorks windows PC application allows to set up the camera, and update it.

The idea here is to obtain an OTA file for the camera by tricking AnkerWorks into thinking the camera needs it.

AnkerWorks is an Electron app, thus can be launched with the debugging tools attached:

```bash
C:\Users\m4mmon\AppData\Local\Programs\AnkerWork\AnkerWork.exe --remote-debugging-port=9222
```

Then open a browser and go to http://localhost:9222/

Select the first instance of Anker Works, go to the "Sources" and under the "no domain" category, look for the "preload.js" embedded into the app.asar file.

Open it and "pretty print" it, because it is minified.


AnkerWorks gets to know if a device needs an update by sending a payload to a server with the device details like the product code and the firmware version.

So what I did was set a breakpoint in the method "manuallyRequestNewVersion". In AnkerWorks, I went to the firmware part and clicked the firmware check button.

The breakpoint was reached, and there I could access the object representing the camera and alter the version member by issuing the following in the debugging console:
```
this.version = "0.1"
```

I then just had to look at the responses, the server immediately provided the complete URL to the OTA update :) on some amazonaws server.

At the time of writing, the filename is "1683172794421534_Kiva_anker_update_package_c200_7.5_230423171038.img".

You can also find the requests and responses in the file "C:\Users\m4mmon\AppData\Roaming\AnkerWork\logs\renderer.log".

So, I downloaded it for further analysis, and also let AnkerWorks perform the update, which went perfectly fine.

Note that it is only 12MB, it does not contain the bootloader and some other parts. It does not replace a complete backup of the firmware.


## flashing the OTA

Here I will not enter into too many details. What happened is that I used an LLM to assist me reconstructing a flashing tool for the camera.

When using AnkerWorks, a lot of info is written into log files located in C:\Users\m4mmon\AppData\Roaming\AnkerWork\logs.
The most important one is awdevice.log.

It tells everything about what happens when the camera is updated. I fed that to the LLM.

Without too many details, the flashing process is like:
- send a special UVC command to the camera to make it enter into update mode,
- the camera in update mode disconnects as an UVC device (the webcam) and declares itself as a serial port,
- the AnkerWorks app waits for the serial port to be present,
- the AnkerWorks app sends information about the OTA file, its size, checksum
- the AnkerWorks app sends chunks of the OTA with a temporary header indicating the checksum of the chunk,
- once every 2000 chunks, the camera sends an "ACK" message containing the index of the last received chunk, AnkerWorks waits for that and checks it,
- when the last chunk has been sent, the camera will send an ACK with a different byte somewhere, kind of indicating it is done.

Once the transfer is done, *alea jacta est*, the camera reboots itself and the bootloader applies the OTA.
Hopefully at the end, the updated camera restart, declares itself as usual as an UVC device, and works again.

So with the help of the LLM a python script was written to handle all this.

**I tried to make it as safe as possible, I have used it myself numerous times, but cannot guarantee it will not brick your camera.**

The script:
- checks the input firmware file ("magic", CRC in header),
- detects the camera,
- sends a command to read its current firmware version,
- enumerates the current serial devices,
- sends the special UVC command to make the camera switch to update mode,
- enumerates the serial ports and checks if a new one has popped,
- sends the firmware as described, a first packet to describe it, then the chunks, the occasional ACKs and the final one.

You can find it [here](scripts/AnkerC200_flashtool.py).
**Use at your own risk**

I tested it with the downloaded OTA file at first. Success :)

## patching the OTA

Thanks Anker, the OTA is not encrypted or anything. It can be extracted and rebuilt, exactly what we need to do.

You can find the script [here](scripts/build_adb_firmware.py).

It extracts and patches some files:
- config/uvc.config: I am not sure about that one. It looks like a default configuration file, and might be used if resetting the camera. Really not sure, in doubt, I decided to make the change there also.
- init/app_init.sh: this script is executed at camera startup. It modifies the uvc.config (not the previous one, but the one actually used by the running system) in order to activate the Android Debug Bridge.
 
Then the script repacks a new OTA file that can be flashed to the camera with the AnkeC200_flashtool.py script.

Once flashed, you can get a root shell by issuing:
```
$ adb shell
[root@Ingenic-uc1_1:modules]# uname -a
Linux Ingenic-uc1_1 3.10.14__isvp_swan_1.0__ #1 PREEMPT Sun Apr 23 17:09:25 CST 2023 mips GNU/Linux
[root@Ingenic-uc1_1:modules]# ps w
  PID USER       VSZ STAT COMMAND
    1 root      1824 S    init
    2 root         0 SW   [kthreadd]
    3 root         0 SW   [ksoftirqd/0]
    4 root         0 SW   [kworker/0:0]
    5 root         0 SW<  [kworker/0:0H]
    6 root         0 SW   [kworker/u2:0]
    7 root         0 SW   [rcu_preempt]
    8 root         0 SW   [rcu_bh]
    9 root         0 SW   [rcu_sched]
   10 root         0 SW   [watchdog/0]
   11 root         0 SW<  [khelper]
   12 root         0 SW<  [writeback]
   13 root         0 SW<  [bioset]
   14 root         0 SW<  [kblockd]
   15 root         0 SW   [kworker/0:1]
   16 root         0 SW   [kswapd0]
   17 root         0 SW   [fsnotify_mark]
   18 root         0 SW<  [crypto]
   32 root         0 SW<  [deferwq]
   33 root         0 SW   [kworker/u2:1]
   45 root      1812 S    telnetd
   48 root         0 SWN  [jffs2_gcd_mtd2]
   50 root      1824 S    /sbin/getty -L console 115200 vt100
   52 root         0 SWN  [jffs2_gcd_mtd3]
   88 root         0 SW   [irq/37-isp-m0]
   90 root         0 SW   [irq/38-isp-w02]
  111 root      165m S    ucamera
  134 root         0 DW   [isp_fw_process]
  140 root     11484 S    hid_update
  143 root      3048 S    adbd
  147 root      1824 S    /bin/sh -l
  151 root      1816 R    ps w

```

## Building thingino

https://thingino.com/
https://github.com/themactep/thingino-firmware/tree/master

The camera is not supported yet, some stuff is missing.
As of today, there is no sound, and no autofocus (though focus can be manually set).

So there is an experimental profile, but you'll have to build an image yourself.

Follow the instructions to build a firmware on the thingino page or wiki.
Instead of issuing the "make" command, you want to:
```
GROUP=exp make
```
and select the "anker_c200_t31x_sc500ai".

Hopefully you'll get a file named "thingino-anker_c200_t31x_sc500ai.bin" at the end.

## backup the original firmware

TODO
- dump the bootloader

## Installing thingino

There you have to take a leap of faith.

If the camera fails to boot, it enters into a special "USB-boot" mode, allowing to read or write the flash chip contents.

You can read everything about that [here](https://github.com/themactep/thingino-firmware/wiki/Ingenic-USB-Cloner).

So, the idea is to make the system unbootable. To do this, simply erase the bootloader. ***WARNING: this makes the camera unusable*** until you flash something back on it with the cloner tool. So, to erase the bootloader:
```
adb shell flash_eraseall /dev/mtd0
```
This was suggested by [gtxaspec](https://github.com/gtxaspec), thanks.

