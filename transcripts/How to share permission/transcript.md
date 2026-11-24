# Transcript: How to share permission.mp4

- Source: `C:\Users\hiros\BCIT Study stuff for cursor\Window-server-admin\Lectures\How to share permission.mp4`
- Duration: 00:17:35
- Segments: 184, screenshots: 40
- Whisper model: `small` (auto-generated; may contain recognition errors)

## [00:00:00]

![screenshot at 00:00:00](frames/frame_0001.jpg)

`[00:00:00]` Hello everyone this week. I'm going to teach you how to share the permission `[00:00:05]` So suppose you work for visa it and you're gonna share permissions `[00:00:16]` between the factory group and the student group `[00:00:20]` So from this slide you can find two groups. They are all domino co-group `[00:00:28]` You're gonna ask me why they are domino co-group `[00:00:32]` because you're gonna see that I have a `[00:00:36]` The faculty folder and assignment folder `[00:00:40]` You always gonna sign the permission to domain local last week we learn group nesting

## [00:00:45]

![screenshot at 00:00:45](frames/frame_0002.jpg)

`[00:00:52]` And also we learn how to sign permissions how to sign permission cross the multiple domain `[00:00:58]` Cross the domain domain tree cross the forest `[00:01:02]` so you always `[00:01:07]` signed permission to `[00:01:09]` Domino co `[00:01:11]` So this is the reason why I created two domino co-group faculty and the students `[00:01:18]` Faculty group may have one employee F1 `[00:01:22]` Student group have two students S1 and S2 `[00:01:28]` Okay, so faculty group

## [00:01:30]

![screenshot at 00:01:30](frames/frame_0003.jpg)

`[00:01:31]` Can access the both folder faculty and assignments? `[00:01:35]` But a student group only can access assignment group `[00:01:40]` And also S1 students only can access student one group and the student two only can access `[00:01:48]` student two group the reason why because if `[00:01:54]` Student one can access both `[00:01:57]` student one student two `[00:02:00]` So student one may copy assignment from student two `[00:02:04]` So we allow the both students to log in assignment folder `[00:02:11]` but `[00:02:12]` Each students only can access their own folder

## [00:02:15]

![screenshot at 00:02:15](frames/frame_0004.jpg)

`[00:02:19]` Facting needed to access both folder because fact you needed to mark assignments give them a comment `[00:02:27]` Okay, so `[00:02:29]` In order to complete this live assignment `[00:02:32]` You need to prepare three VMs `[00:02:36]` The first one is server one `[00:02:39]` IP address already provide to you `[00:02:42]` So the one is don't be controller `[00:02:45]` Server six and that is a file server. So you needed to clone another server, which is a server six `[00:02:54]` And also we're gonna need a client `[00:02:57]` Okay, so let's start to work on this lab. So first

## [00:03:00]

![screenshot at 00:03:00](frames/frame_0005.jpg)

`[00:03:06]` file server

## [00:03:08]

![screenshot at 00:03:08](frames/frame_0006.jpg)

`[00:03:08]` You need to log in as domain on the main and also I want you to double check exactly

## [00:03:18]

![screenshot at 00:03:18](frames/frame_0007.jpg)

`[00:03:22]` IP address and make sure you have already joined domain

## [00:03:23]

![screenshot at 00:03:23](frames/frame_0008.jpg)

`[00:03:32]` Okay, pure domain controller. Okay `[00:03:40]` so next

## [00:03:41]

![screenshot at 00:03:41](frames/frame_0009.jpg)

`[00:03:42]` You needed to install a `[00:03:45]` File server row `[00:03:47]` Okay, we want to install the file server. It will take around one minute to finish the installation `[00:04:09]` So at the same time you can go to domain controller

## [00:04:12]

![screenshot at 00:04:12](frames/frame_0010.jpg)

`[00:04:16]` to create the two `[00:04:18]` Domain local group already created two domain local group one factory group

## [00:04:29]

![screenshot at 00:04:29](frames/frame_0011.jpg)

`[00:04:37]` If you look at the members only include one employee `[00:04:43]` Students group also domain local `[00:04:48]` members `[00:04:49]` Is Lisa on the team? `[00:04:51]` So you probably ask me how to add a student add a student to the student group `[00:04:57]` So right click add it to a group and then search students. Okay, so this is how to add `[00:05:10]` Students to student group `[00:05:13]` Okay

## [00:05:14]

![screenshot at 00:05:14](frames/frame_0012.jpg)

`[00:05:15]` Next one. Hopefully already install. Yes already done `[00:05:20]` Okay, so after you install `[00:05:23]` Go to a server manager `[00:05:26]` Expand the file and you can see shares click that one. I want to create a file `[00:05:38]` And I want to use the quick options `[00:05:43]` The quick options and advanced options the major difference is `[00:05:49]` The advanced options you have access deny assistant `[00:05:54]` okay `[00:05:56]` But for this level summit we don't need that one

## [00:05:59]

![screenshot at 00:05:59](frames/frame_0013.jpg)

`[00:05:59]` Okay, and NFS so that it can be used to `[00:06:04]` share permission `[00:06:05]` for Linux or unix `[00:06:08]` Okay, and I wanted to `[00:06:15]` Put my share folder on the d drive. Okay, if you don't have a d drive you can put on the c drive `[00:06:22]` I'm going to use the name is `[00:06:28]` factory next `[00:06:37]` You will see one options enable access based `[00:06:42]` Ineurations

## [00:06:44]

![screenshot at 00:06:44](frames/frame_0014.jpg)

`[00:06:45]` So if you use if you enable these functions `[00:06:49]` So that means if you don't have permissions `[00:06:54]` You cannot see that folder `[00:06:57]` Okay, if you don't have the permissions you cannot see that folder `[00:07:02]` so that can give you a lot of benefit because `[00:07:07]` Some employee `[00:07:08]` Probably you careless `[00:07:10]` Why I have that folder why cannot open? `[00:07:15]` Okay `[00:07:16]` So if you allow them to see `[00:07:18]` You give them the chance to mess up the folders `[00:07:23]` To bother you to send email `[00:07:26]` to file tickets `[00:07:28]` And ask you to explain why cannot access

## [00:07:29]

![screenshot at 00:07:29](frames/frame_0015.jpg)

`[00:07:32]` Okay, so I want you to enable that one `[00:07:35]` So next we need to confirm configure the permissions `[00:07:41]` So first `[00:07:44]` I want you to disable the inheritance `[00:07:47]` So that is a pre-configure the permissions `[00:07:51]` But that permission cannot satisfy our scenarios because we only allowed `[00:07:57]` faculty to access faculty group `[00:08:00]` So I'm going to use disable inheritance `[00:08:03]` Remove all the inheritance permissions from this object `[00:08:09]` Okay, so you will see that right now `[00:08:13]` The local administrator have a full control. I also want to remove that one

## [00:08:14]

![screenshot at 00:08:14](frames/frame_0016.jpg)

`[00:08:19]` I want to give it a permission to `[00:08:23]` Don't know me I want to give it a full control `[00:08:32]` So what's that different between the full control and modify? `[00:08:36]` Full control you can take the ownership `[00:08:39]` Okay `[00:08:42]` Next I want to share `[00:08:44]` to faculty `[00:08:48]` That is a group `[00:08:51]` I'll give you the modified permissions `[00:08:54]` Share `[00:08:56]` I don't want to share everyone. I only want to share to

## [00:08:59]

![screenshot at 00:08:59](frames/frame_0017.jpg)

`[00:09:00]` faculty `[00:09:07]` You can give it a change permission apply `[00:09:15]` Okay `[00:09:16]` Next create `[00:09:21]` If you go to the `[00:09:23]` D drive `[00:09:24]` Shares you will see the `[00:09:27]` faculty folder `[00:09:28]` Okay, we want to create another one. We want to create a `[00:09:38]` student folder `[00:09:40]` or assignment from disable everything

## [00:09:44]

![screenshot at 00:09:44](frames/frame_0018.jpg)

`[00:09:52]` You only want to give the permission to `[00:09:56]` Don't mind me and also this is a student folder `[00:10:10]` I'll give it to students keep students to modify because students need to sum in their assignments `[00:10:23]` You can create a sub folder `[00:10:26]` Okay

## [00:10:30]

![screenshot at 00:10:30](frames/frame_0019.jpg)

`[00:10:40]` Next we'll give the faculty so faculty can give some comments `[00:10:44]` So faculty also can have a modify permissions `[00:10:49]` I want to give the faculty this folder or the sub folder `[00:10:55]` share I want to share to `[00:10:57]` faculty `[00:11:01]` And the student only apply. Okay next close dmd not share

## [00:11:15]

![screenshot at 00:11:15](frames/frame_0020.jpg)

## [00:11:23]

![screenshot at 00:11:23](frames/frame_0021.jpg)

`[00:11:28]` You can see that right now two folder are ready to `[00:11:32]` share

## [00:11:32]

![screenshot at 00:11:32](frames/frame_0022.jpg)

`[00:11:34]` And also you can modify the permission if you set up something wrong `[00:11:41]` You can remodify `[00:11:44]` Okay, let's modify

## [00:11:47]

![screenshot at 00:11:47](frames/frame_0023.jpg)

`[00:11:49]` So first I'm going to use my account lobby, which is a faculty folder backslash backslash c

## [00:11:59]

![screenshot at 00:11:59](frames/frame_0024.jpg)

`[00:12:13]` win `[00:12:16]` spr6 `[00:12:20]` So you can see that I can access `[00:12:23]` assignment and the faculty folder `[00:12:31]` so next I want to create a

## [00:12:31]

![screenshot at 00:12:31](frames/frame_0025.jpg)

## [00:12:36]

![screenshot at 00:12:36](frames/frame_0026.jpg)

`[00:12:38]` A folder for so this folder is only for team `[00:12:51]` to `[00:12:52]` access `[00:13:02]` So when teams sum in assignment, so team can have a permission `[00:13:07]` to modify `[00:13:09]` Okay, yeah, but next I'm going to create `[00:13:19]` A folder for Lisa

## [00:13:21]

![screenshot at 00:13:21](frames/frame_0027.jpg)

`[00:13:21]` So when Lisa login Lisa only can see this folder `[00:13:24]` So let's look at the faculty make sure faculty can access the both folder

## [00:13:38]

![screenshot at 00:13:38](frames/frame_0028.jpg)

`[00:13:55]` faculty can `[00:13:57]` Create a folder in here can give some comments `[00:14:06]` Excellent `[00:14:10]` Okay, so this is can verify faculty have both permissions to modify and create folders can give some comments

## [00:14:17]

![screenshot at 00:14:17](frames/frame_0029.jpg)

`[00:14:18]` So let's `[00:14:21]` Switch the user I want to log in as a Lisa when Lisa login

## [00:14:21]

![screenshot at 00:14:21](frames/frame_0030.jpg)

## [00:14:31]

![screenshot at 00:14:31](frames/frame_0031.jpg)

`[00:14:37]` Let's try `[00:14:48]` Lisa can only see `[00:14:50]` her folder `[00:14:51]` She cannot `[00:14:54]` Find any folder related to team, right?

## [00:15:00]

![screenshot at 00:15:00](frames/frame_0032.jpg)

`[00:15:01]` Let's log in as a team team only can see his folder

## [00:15:05]

![screenshot at 00:15:05](frames/frame_0033.jpg)

## [00:15:13]

![screenshot at 00:15:13](frames/frame_0034.jpg)

`[00:15:30]` Okay `[00:15:32]` team also can `[00:15:34]` create a folder like `[00:15:36]` assignment `[00:15:42]` Six check my and team also cannot

## [00:15:58]

![screenshot at 00:15:58](frames/frame_0035.jpg)

`[00:16:07]` See Lisa's folder, right? `[00:16:10]` And also team don't have permission to modify the faculty `[00:16:16]` So when we switch

## [00:16:20]

![screenshot at 00:16:20](frames/frame_0036.jpg)

`[00:16:20]` Back to the faculty group

## [00:16:28]

![screenshot at 00:16:28](frames/frame_0037.jpg)

`[00:16:49]` So I can see both folder `[00:16:51]` team `[00:16:54]` Can give some comments `[00:16:58]` Good job `[00:17:04]` Also can modify Lisa's folder to modify this code

## [00:17:13]

![screenshot at 00:17:13](frames/frame_0038.jpg)

## [00:17:18]

![screenshot at 00:17:18](frames/frame_0039.jpg)

`[00:17:18]` Okay, so this is a demonstration how to `[00:17:21]` share the permissions

## [00:17:23]

![screenshot at 00:17:23](frames/frame_0040.jpg)

`[00:17:25]` If you have questions talk to me `[00:17:28]` Okay `[00:17:30]` And `[00:17:31]` See you in the lecture
