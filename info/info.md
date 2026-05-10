# Information about the Anker C200

If you get a serial console on the camera, the username is "root" without password.

## boot serial output

```
Serial init OK!jz_serial_init ok
pll_init:366
pll_cfg.pdiv = 10, pll_cfg.h2div = 5, pll_cfg.h0div = 5, pll_cfg.cdiv = 1, pll_cfg.l2div = 2
nf=116 nr = 1 od0 = 1 od1 = 2
cppcr is 07405100
CPM_CPAPCR 0740510d
nf=100 nr = 1 od0 = 1 od1 = 2
cppcr is 06405100
CPM_CPMPCR 0640510d
nf=96 nr = 1 od0 = 1 od1 = 2
cppcr is 06005100
CPM_CPVPCR 1200990d
cppcr 0x9a7b5510
apll_freq 1392000000
mpll_freq 1200000000
vpll_freq = 1152000000
ddr sel mpll, cpu sel apll
ddrfreq 600000000
cclk  1392000000
l2clk 696000000
h0clk 240000000
h2clk 240000000
pclk  120000000
sdram init start
REG_DDR_LMR: 00000210
REG_DDR_LMR: 00000310
REG_DDR_LMR: 00000110
REG_DDR_LMR, MR0: 00f73011
T31_0x5: 00000007
T31_0x15: 0000000c
T31_0x4: 00000000
T31_0x14: 00000002
INNO_TRAINING_CTRL 1: 00000000
INNO_TRAINING_CTRL 2: 000000a1
T31_cc: 00000003
INNO_TRAINING_CTRL 3: 000000a0
T31_118: 0000003c
T31_158: 0000003c
T31_190: 0000001f
T31_194: 0000001d
DDR PHY init OK
DDR Controller init
SDRAM init ok

spl_sfc_nor_load_kernel flash_flag=0xffffffff...

uImage size = [3321347]
OK
images->ep = 802c2790
[    0.000000] Initializing cgroup subsys cpu
[    0.000000] Initializing cgroup subsys cpuacct
[    0.000000] Linux version 3.10.14__isvp_swan_1.0__ (iotbuild@115892f10c38) (gcc version 4.7.2 (Ingenic r2.3.3 2016.12) ) #1 PREEMPT Sun Apr 23 17:11:07 CST 2023
[    0.000000] bootconsole [early0] enabled
[    0.000000] CPU0 RESET ERROR PC:9C789498
[    0.000000] CPU0 revision is: 00d00100 (Ingenic Xburst)
[    0.000000] FPU revision is: 00b70000
[    0.000000] CCLK:1392MHz L2CLK:696Mhz H0CLK:200MHz H2CLK:200Mhz PCLK:100Mhz
[    0.000000] Determined physical RAM map:
[    0.000000]  memory: 003a6000 @ 00010000 (usable)
[    0.000000]  memory: 0030a000 @ 003b6000 (usable after init)
[    0.135852] drivers/rtc/hctosys.c: unable to open rtc device (rtc0)
mdev is ok......

Ingenic-uc1_1 login: [    0.513563] dw9714-input 0-000c: misc_deregister is ok!
/media/uvc.attr exist
brgain:03290153
Invalid config param: focus_trigger_value
[Ucamera]: ---ovo---warning: config 11--00000064--100

[Ucamera]: ---ovo---warning: config 1--00000000--0

[Ucamera]: ---ovo---warning: config 2--00000000--0

[Ucamera]: ---ovo---warning: config 3--0000005f--95

[Ucamera]: ---ovo---warning: config 4--00000000--0

[Ucamera]: ---ovo---warning: config 5--00000000--0

[Ucamera]: ---ovo---warning: config 6--00000000--0

[Ucamera]: ---ovo---warning: config 7--00000001--1

---ovo-----af--1---1--
[Ucamera]: ---ovo---warning: config 8--00000286--646

++++af value = 646 +++++
[Ucamera]: ---ovo---warning: config 9--03290153--53018963

[Ucamera]: [INFO]: Video Start.

---- FPGA board is ready ----
  Board UID : 30AB6E51
  Board HW ID : 72000460
  Board rev.  : 5DE5A975
  Board date  : 20190326
-----------------------------
warn: shm_init,53shm init already
auaglo_init, channel:2, rate:48000, ifsamples:1440, frame_size:5760
ovo-0-,init process!
mod_this:2,mod:2,angle:0
[Ucamera]: [INFO]: Audio Start.

[Ucamera]: gaudio unkonwn event:0

------RECORD  OFF------
------RECORD  OFF------
------RECORD  OFF------
------RECORD  OFF------
data_copy is 0, 0 ,95, 0, 0, 0, 0, 0
###eu set cmd =16, len =60, ###
[Ucamera]: IMP Set Fcrop failed=504

[Ucamera]: IMP Set Fcrop failed=864

[Ucamera]: ERROR: set BrightNess failed :-1

[Ucamera]: set Sharpness failed:-1

[Ucamera]: set Saturation failed:-1

###eu set cmd =17, len =60, ###
 key val = 1
[Ucamera]:ERROR:: set hvflip is faild

data_copy is 0, 1 ,95, 0, 0, 0, 0, 0
[Ucamera]: UVC: Setting format to: MJPG 2560x1440

[Ucamera]: UVC: uvc event stream on!

[Ucamera]: ---ovo---warning: config 11--00000064--100

[Ucamera]: ---ovo---warning: config 1--00000000--0

[Ucamera]: ---ovo---warning: config 2--00000000--0

[Ucamera]: ---ovo---warning: config 3--0000005f--95

[Ucamera]: ---ovo---warning: config 4--00000000--0

[Ucamera]: ---ovo---warning: config 5--00000000--0

[Ucamera]: ---ovo---warning: config 6--00000000--0

[Ucamera]: ---ovo---warning: config 7--00000001--1

---ovo-----af--1---1--
[Ucamera]: ---ovo---warning: config 8--00000286--646

++++af value = 646 +++++
[Ucamera]: ---ovo---warning: config 9--03290153--53018963

 key val = 1
INFO(camera_off_pic_prepare_process): prepare camera_off_pic data ok
[Ucamera]: IMP SDK reinit!

[Ucamera]: IMP: Scaler enable w:2560 h:1440

[Ucamera]: set Antiflicker level:1 fps:25

[Ucamera]: UVC: Starting video stream.

jdwp_service.c::jdwp_control_init():jdwp control socket started (6)

```

## dmesg (with ADB enabled, and kernek patched to show mtd4.

```
[    0.000000] Initializing cgroup subsys cpu
[    0.000000] Initializing cgroup subsys cpuacct
[    0.000000] Linux version 3.10.14__isvp_swan_1.0__ (iotbuild@115892f10c38) (gcc version 4.7.2 (Ingenic r2.3.3 2016.12) ) #1 PREEMPT Sun Apr 23 17:11:07 CST 2023
[    0.000000] bootconsole [early0] enabled
[    0.000000] CPU0 RESET ERROR PC:9C789498
[    0.000000] CPU0 revision is: 00d00100 (Ingenic Xburst)
[    0.000000] FPU revision is: 00b70000
[    0.000000] cgu_get_rate, parent = 1392000000, rate = 0, m = 0, n = 0, reg val = 0x081000ff
[    0.000000] cgu_get_rate, parent = 1392000000, rate = 0, m = 0, n = 0, reg val = 0x081000ff
[    0.000000] CCLK:1392MHz L2CLK:696Mhz H0CLK:200MHz H2CLK:200Mhz PCLK:100Mhz
[    0.000000] Determined physical RAM map:
[    0.000000]  memory: 003a6000 @ 00010000 (usable)
[    0.000000]  memory: 0030a000 @ 003b6000 (usable after init)
[    0.000000] User-defined physical RAM map:
[    0.000000]  memory: 04000000 @ 00000000 (usable)
[    0.000000] Initrd not found or empty - disabling initrd
[    0.000000] Zone ranges:
[    0.000000]   Normal   [mem 0x00000000-0x03ffffff]
[    0.000000] Movable zone start for each node
[    0.000000] Early memory node ranges
[    0.000000]   node   0: [mem 0x00000000-0x03ffffff]
[    0.000000] On node 0 totalpages: 16384
[    0.000000] free_area_init_node: node 0, pgdat 803b4490, node_mem_map 81000000
[    0.000000]   Normal zone: 128 pages used for memmap
[    0.000000]   Normal zone: 0 pages reserved
[    0.000000]   Normal zone: 16384 pages, LIFO batch:3
[    0.000000] Primary instruction cache 32kB, 8-way, VIPT, linesize 32 bytes.
[    0.000000] Primary data cache 32kB, 8-way, VIPT, no aliases, linesize 32 bytes
[    0.000000] pls check processor_id[0x00d00100],sc_jz not support!
[    0.000000] MIPS secondary cache 128kB, 8-way, linesize 32 bytes.
[    0.000000] pcpu-alloc: s0 r0 d32768 u32768 alloc=1*32768
[    0.000000] pcpu-alloc: [0] 0
[    0.000000] Built 1 zonelists in Zone order, mobility grouping off.  Total pages: 16256
[    0.000000] Kernel command line:  console=ttyS1,115200n8 mem=64M@0x0 rmem=64M@0x4000000 init=/linuxrc root=/dev/ram0 rw mtdparts=jz_sfc:32k(boot),4064k(kernel),8192k(appfs),256k(configfs),3840k(ota_kernel) quiet
[    0.000000] PID hash table entries: 256 (order: -2, 1024 bytes)
[    0.000000] Dentry cache hash table entries: 8192 (order: 3, 32768 bytes)
[    0.000000] Inode-cache hash table entries: 4096 (order: 2, 16384 bytes)
[    0.000000] Memory: 57636k/65536k available (2793k kernel code, 7900k reserved, 940k data, 3112k init, 0k highmem)
[    0.000000] SLUB: HWalign=32, Order=0-3, MinObjects=0, CPUs=1, Nodes=1
[    0.000000] Preemptible hierarchical RCU implementation.
[    0.000000] NR_IRQS:358
[    0.000000] clockevents_config_and_register success.
[    0.000014] Calibrating delay loop... 1391.00 BogoMIPS (lpj=6955008)
[    0.090039] pid_max: default: 32768 minimum: 301
[    0.090224] Mount-cache hash table entries: 512
[    0.090630] Initializing cgroup subsys debug
[    0.090647] Initializing cgroup subsys freezer
[    0.092233] regulator-dummy: no parameters
[    0.092363] NET: Registered protocol family 16
[    0.093024] set gpio strength: 32-2
[    0.093032] set gpio strength: 33-2set gpio strength: 34-2
[    0.093042] set gpio strength: 35-2set gpio strength: 36-2
[    0.093050] set gpio strength: 37-2set gpio pull: 59-90
[    0.099454] bio: create slab <bio-0> at 0
[    0.100972] jz-dma jz-dma: JZ SoC DMA initialized
[    0.101174]  (null): set:249  hold:250 dev=100000000 h=500 l=500
[    0.101246] media: Linux media interface: v0.10
[    0.101285] Linux video capture interface: v2.00
[    0.101653] Switching to clocksource jz_clocksource
[    0.102075] dwc2 otg probe start
[    0.102099] jz-dwc2 jz-dwc2: cgu clk gate get error
[    0.102120] DWC IN DEVICE ONLY MODE
[    0.102746] dwc2 dwc2: Keep PHY ON
[    0.102754] dwc2 dwc2: Using Buffer DMA mode
[    0.102764] dwc2 dwc2: Core Release: 3.00a
[    0.102987] dwc2 dwc2: enter dwc2_gadget_plug_change:2595: plugin = 1 pullup_on = 0 suspend = 0
[    0.102996] dwc2 otg probe success
[    0.103121] NET: Registered protocol family 2
[    0.103598] TCP established hash table entries: 512 (order: 0, 4096 bytes)
[    0.103621] TCP bind hash table entries: 512 (order: -1, 2048 bytes)
[    0.103635] TCP: Hash tables configured (established 512 bind 512)
[    0.103680] TCP: reno registered
[    0.103692] UDP hash table entries: 256 (order: 0, 4096 bytes)
[    0.103709] UDP-Lite hash table entries: 256 (order: 0, 4096 bytes)
[    0.103896] NET: Registered protocol family 1
[    0.122778] freq_udelay_jiffys[0].max_num = 10
[    0.122788] cpufreq  udelay  loops_per_jiffy
[    0.122794] 12000     59956   59956
[    0.122800] 24000     119913  119913
[    0.122805] 60000     299784  299784
[    0.122811] 120000    599569  599569
[    0.122816] 200000    999282  999282
[    0.122822] 300000    1498924         1498924
[    0.122828] 600000    2997848         2997848
[    0.122833] 792000    3957159         3957159
[    0.122838] 1008000   5036385         5036385
[    0.122844] 1200000   5995696         5995696
[    0.126346] squashfs: version 4.0 (2009/01/31) Phillip Lougher
[    0.126486] jffs2: version 2.2. © 2001-2006 Red Hat, Inc.
[    0.126738] msgmni has been set to 112
[    0.127715] io scheduler noop registered
[    0.127749] io scheduler cfq registered (default)
[    0.128848] jz-uart.1: ttyS1 at MMIO 0x10031000 (irq = 58) is a uart1
[    0.129930] console [ttyS1] enabled, bootconsole disabled
[    0.130326] brd: module loaded
[    0.131607] loop: module loaded
[    0.132412] zram: Created 2 device(s) ...
[    0.132474] logger: created 256K log 'log_main'
[    0.132860] jz TCU driver register completed
[    0.133147] the id code = 204018, the flash name is XM25QH128C
[    0.133158] JZ SFC Controller for SFC channel 0 driver register
[    0.133176] 5 cmdlinepart partitions found on MTD device jz_sfc
[    0.133182] Creating 5 MTD partitions on "jz_sfc":
[    0.133192] 0x000000000000-0x000000008000 : "boot"
[    0.133602] 0x000000008000-0x000000400000 : "kernel"
[    0.133975] 0x000000400000-0x000000c00000 : "appfs"
[    0.134328] 0x000000c00000-0x000000c40000 : "configfs"
[    0.134660] 0x000000c40000-0x000001000000 : "ota_kernel"
[    0.135012] SPI NOR MTD LOAD OK
[    0.135406] TCP: cubic registered
[    0.135420] NET: Registered protocol family 17
[    0.135852] drivers/rtc/hctosys.c: unable to open rtc device (rtc0)
[    0.148139] Freeing unused kernel memory: 3112K (803b6000 - 806c0000)
[    0.432464] gpio_key_init ok !!!
[    0.513271] dac_value is 100
[    0.513563] dw9714-input 0-000c: misc_deregister is ok!
[    0.554275] es8374_codec_register, probe() successful!
[    0.555820] cgu_set_rate, parent = 1392000000, rate = 2048000, n = 10875, reg val = 0x01002a7b
[    0.555832] cgu_enable,cgu_i2s_spk reg val = 0x21002a7b
[    0.555853] cgu_set_rate, parent = 1392000000, rate = 2048000, n = 10875, reg val = 0x01002a7b
[    0.555860] cgu_enable,cgu_i2s_mic reg val = 0x21002a7b
[    0.555871] ------------- i2s reset now...
[    0.556089] dma dma0chan24: Channel 24 have been requested.(phy id 7,type 0x06 desc a0481000)
[    0.556374] dma dma0chan25: Channel 25 have been requested.(phy id 6,type 0x06 desc a0459000)
[    0.556688] dma dma0chan26: Channel 26 have been requested.(phy id 5,type 0x04 desc a0463000)
[    0.739400] @@@@ tx-isp-probe ok(version H20220608a), compiler date=Jun  9 2022 @@@@@
[    0.915747] g_camera gadget: g_camera ready
[    0.922877] INFO(key_drv_read): key drv read !!!
[    0.944914] probe ok ------->sc500ai
[    1.002312] -----sc500ai_detect: 846 ret = 0, v = 0xce
[    1.002933] -----sc500ai_detect: 854 ret = 0, v = 0x1f
[    1.002940] sc500ai chip found @ 0x30 (i2c0)
[    1.002945] sensor driver version H20210615a
[    1.418702] cgu_set_rate, parent = 1392000000, rate = 12288000, n = 3625, reg val = 0x22000e29
[    1.418775] cgu_set_rate, parent = 1392000000, rate = 12288000, n = 3625, reg val = 0x22000e29
[    7.155256] g_camera gadget: high-speed config #1: ucamera
[    7.155273] g_camera gadget: uac_function_set_alt(2, 0)
[    7.155285] g_camera gadget: uac_function_set_alt(3, 0)
[    7.155423] g_camera gadget: uac_function_set_alt(3, 0)
[    7.156716] g_camera gadget: uac_function_set_alt(3, 0)
[    7.181713] dwc2 dwc2: dwc2_ep0_stall_and_restart
[    7.224184] g_camera gadget: uac_function_set_alt(3, 0)
[    8.822731] adb_open
```

## gpio

```
[root@Ingenic-uc1_1:~]# mount -t debugfs none /sys/kernel/debug; cat /sys/kernel
/debug/gpio
GPIOs 0-31, GPIO A:
 gpio-18  (sc500ai_reset       ) out hi
 gpio-26  (PA26                ) in  hi

GPIOs 32-63, GPIO B:
 gpio-42  (sw9714_xsd          ) out hi
 gpio-49  (sysfs               ) out lo
 gpio-57  (key1_irq            ) in  hi

GPIOs 64-95, GPIO C:
[root@Ingenic-uc1_1:~]#
```

## UVC

```bash
$ v4l2-ctl -d /dev/video0 -L

User Controls

                     brightness 0x00980900 (int)    : min=0 max=100 step=1 default=50 value=50
                       contrast 0x00980901 (int)    : min=0 max=100 step=1 default=50 value=50
                     saturation 0x00980902 (int)    : min=0 max=100 step=1 default=50 value=50
                            hue 0x00980903 (int)    : min=0 max=3 step=1 default=1 value=0
        white_balance_automatic 0x0098090c (bool)   : default=1 value=1
                          gamma 0x00980910 (int)    : min=0 max=800 step=1 default=400 value=400
           power_line_frequency 0x00980918 (menu)   : min=0 max=2 default=0 value=1 (50 Hz)
                                0: Disabled
                                1: 50 Hz
                                2: 60 Hz
      white_balance_temperature 0x0098091a (int)    : min=2300 max=6500 step=1 default=4500 value=168 flags=inactive
                      sharpness 0x0098091b (int)    : min=0 max=100 step=1 default=50 value=50

Camera Controls

                  auto_exposure 0x009a0901 (menu)   : min=0 max=3 default=0 value=0
                                1: Manual Mode
         exposure_time_absolute 0x009a0902 (int)    : min=1 max=1000 step=1 default=156 value=156 flags=inactive
                   pan_absolute 0x009a0908 (int)    : min=-36000 max=36000 step=3600 default=0 value=0
                  tilt_absolute 0x009a0909 (int)    : min=-36000 max=36000 step=3600 default=0 value=0
                 focus_absolute 0x009a090a (int)    : min=300 max=650 step=1 default=300 value=300 flags=inactive
     focus_automatic_continuous 0x009a090c (bool)   : default=1 value=1
                  zoom_absolute 0x009a090d (int)    : min=100 max=400 step=1 default=100 value=100
```

```bash
$ v4l2-ctl -d /dev/video0 --list-formats-ext
ioctl: VIDIOC_ENUM_FMT
        Type: Video Capture

        [0]: 'MJPG' (Motion-JPEG, compressed)
                Size: Discrete 2560x1440
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 1920x1080
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 1280x720
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 640x480
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 640x360
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 320x240
                        Interval: Discrete 0.033s (30.000 fps)
        [1]: 'YUYV' (YUYV 4:2:2)
                Size: Discrete 640x480
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 640x360
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 320x240
                        Interval: Discrete 0.033s (30.000 fps)
        [2]: 'H264' (H.264, compressed)
                Size: Discrete 2560x1440
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 1920x1080
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 1280x720
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 640x480
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 640x360
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 320x240
                        Interval: Discrete 0.033s (30.000 fps)
```
