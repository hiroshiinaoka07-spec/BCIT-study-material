# Transcript: Class Demo.mp4

- Source: `C:\Users\hiros\BCIT Study stuff for cursor\Window-server-admin\Lectures\Class Demo.mp4`
- Duration: 00:44:29
- Segments: 364, screenshots: 103
- Whisper model: `small` (auto-generated; may contain recognition errors)

## [00:00:00]

![screenshot at 00:00:00](frames/frame_0001.jpg)

`[00:00:01]` Hello everyone, this week I will teach you how to install and config DNS Zoom. `[00:00:08]` So first, let's talk about what is DNS Zoom. `[00:00:13]` A DNS Zoom is a portion of a DNS named space that has been divided for administration purpose. `[00:00:23]` Each DNS server may have many different zones. `[00:00:29]` Each DNS server may have more than one zone, that's pretty normal. `[00:00:35]` But the complete DNS named space could not be hold on one server. `[00:00:43]` Have you still remember?

## [00:00:45]

![screenshot at 00:00:45](frames/frame_0002.jpg)

`[00:00:45]` In week 3 or week 4, I created a forest, like a subdomain domain tree. `[00:00:55]` Your subdomain DNS you can create on your domain controller, which is your parent's domain, `[00:01:07]` or you can delegate it to the subdomain domain controller, or any server from your forest. `[00:01:17]` There are many different types of zones, such as primary zone, secondary zone, `[00:01:24]` active directory, integrated zone, and stop zone. `[00:01:29]` Before you work on this lab, I want you to figure out, to completely understand,

## [00:01:30]

![screenshot at 00:01:30](frames/frame_0003.jpg)

`[00:01:36]` the major difference between the primary zone, secondary zone, active directory, `[00:01:43]` integrated zone, and stop zone. `[00:01:46]` Why do we need AD integrated zone? `[00:01:51]` What is the purpose? `[00:01:53]` And it benefits and it drawback. `[00:01:58]` So what is the primary zone? `[00:02:00]` What is the secondary zone? `[00:02:02]` In which scenarios you need a primary zone? `[00:02:05]` You need a secondary zone? `[00:02:07]` You need a stop zone? `[00:02:09]` So I want you to figure out. `[00:02:11]` I want you to know that before you continue. `[00:02:14]` If you don't know, talk to me or ask me.

## [00:02:15]

![screenshot at 00:02:15](frames/frame_0004.jpg)

`[00:02:21]` As I told you before, this week I will teach you how to install and config a secondary zone. `[00:02:30]` So first, what is secondary zone? `[00:02:35]` You probably already know it. `[00:02:38]` In Term 2, I believe you learned the Linux DNS. `[00:02:44]` So I also hope you already know how to install and configure the Linux DNS, `[00:02:51]` on the Linux DNS zone. `[00:02:56]` So the secondary zone can be the copy of a primary zone.

## [00:03:00]

![screenshot at 00:03:00](frames/frame_0005.jpg)

`[00:03:03]` The secondary zone can be a copy of the secondary zone. `[00:03:08]` The secondary zone can be copies of active directory integrated zone. `[00:03:15]` So you will know that. `[00:03:18]` The secondary zone is a copy from another zone. `[00:03:25]` It comes from the primary zone, master room, or secondary zone. `[00:03:33]` This is the only zone. `[00:03:36]` Any changes must be made on the original zone, which is the primary zone. `[00:03:41]` So the primary zone must be available if you want to make some changes.

## [00:03:45]

![screenshot at 00:03:45](frames/frame_0006.jpg)

`[00:03:47]` The data must be replicated from the master room, primary zone, or secondary zone. `[00:04:01]` You need to keep the updates. `[00:04:05]` The data must be replicated from the master copy to keep the secondary zone up to date. `[00:04:26]` So next questions you probably ask me, who can hold the secondary zone?

## [00:04:30]

![screenshot at 00:04:30](frames/frame_0007.jpg)

`[00:04:32]` It really depends on your community environment. `[00:04:35]` You can use Windows or Windows, or you can use all Linux, `[00:04:42]` or you can use the mixed community environment. `[00:04:45]` For example, we use Linux as the primary zone, and Windows as the secondary zone. `[00:04:53]` Last questions, why do we need a secondary zone? `[00:05:00]` So this is a similar question that I asked you, why do you need a secondary domain controller? `[00:05:09]` For tolerance and load balance. `[00:05:15]` So if the primary zone failed,

## [00:05:15]

![screenshot at 00:05:15](frames/frame_0008.jpg)

`[00:05:19]` you can change the secondary zone to become a primary zone. `[00:05:25]` I don't want to use the key words promote. `[00:05:28]` I use key words to change or switch. `[00:05:31]` So if the primary zone failed, you can change your secondary zone to primary zone. `[00:05:39]` In order, you have permission to modify the DNS record. `[00:05:44]` If you fix the problem for your primary zone, `[00:05:49]` you can change your current server back to the secondary zone again. `[00:05:54]` For this class, I also want you to familiar some DNS records,

## [00:06:00]

![screenshot at 00:06:00](frames/frame_0009.jpg)

`[00:06:02]` such as Start Authority, Name Server, A record, `[00:06:09]` Quad A record, and MS record, which is for exchange server. `[00:06:15]` Okay, let's look at the network topology. `[00:06:24]` In order to complete this live assignment, `[00:06:28]` first, you need to prepare two servers, `[00:06:31]` Server 1, which is your domain controller, `[00:06:35]` hold the master room, and that one also is a Start Authority, `[00:06:43]` and also you need to prepare a new server, which is Server 4.

## [00:06:45]

![screenshot at 00:06:45](frames/frame_0010.jpg)

`[00:06:48]` If you already have Server 4, you can create a Server 5. `[00:06:54]` I already have a Server 4 for my domain tree, `[00:06:58]` so I'm going to create a Server 5 instead of a Server 4. `[00:07:02]` So the IP, I'm going to use a .5, not a .4. `[00:07:07]` Okay, let's start it. `[00:07:09]` First, you need to power on your DC1.

## [00:07:11]

![screenshot at 00:07:11](frames/frame_0011.jpg)

## [00:07:16]

![screenshot at 00:07:16](frames/frame_0012.jpg)

`[00:07:17]` Second, I'm going to clone one server. `[00:07:20]` I'm going to create a full clone.

## [00:07:25]

![screenshot at 00:07:25](frames/frame_0013.jpg)

`[00:07:39]` Name, ACIT, Server 420, NS. `[00:07:49]` Second, create a new folder. `[00:08:06]` I have another folder, I created a long time ago.

## [00:08:10]

![screenshot at 00:08:10](frames/frame_0014.jpg)

## [00:08:28]

![screenshot at 00:08:28](frames/frame_0015.jpg)

`[00:08:38]` I'm going to remove the folder. `[00:08:51]` So you can remove the folder after reboot.

## [00:08:54]

![screenshot at 00:08:54](frames/frame_0016.jpg)

`[00:08:54]` Okay, I have already successfully to clone that one,

## [00:09:39]

![screenshot at 00:09:39](frames/frame_0017.jpg)

`[00:10:02]` so I'm going to next step. `[00:10:04]` So we need to config the server, `[00:10:09]` which is a basic configuration, `[00:10:12]` like a committed name, joint domain, IP address.

## [00:10:19]

![screenshot at 00:10:19](frames/frame_0018.jpg)

## [00:10:25]

![screenshot at 00:10:25](frames/frame_0019.jpg)

`[00:10:26]` First, I wanted to verify my server has been successfully to plug in VM99.

## [00:10:29]

![screenshot at 00:10:29](frames/frame_0020.jpg)

`[00:10:34]` And also, if you haven't removed your IPv6 yet,

## [00:10:34]

![screenshot at 00:10:34](frames/frame_0021.jpg)

## [00:10:40]

![screenshot at 00:10:40](frames/frame_0022.jpg)

## [00:10:47]

![screenshot at 00:10:47](frames/frame_0023.jpg)

## [00:10:58]

![screenshot at 00:10:58](frames/frame_0024.jpg)

## [00:11:02]

![screenshot at 00:11:02](frames/frame_0025.jpg)

`[00:11:10]` I want you to remove your IPv6 right now. `[00:11:14]` After you remove, I want you to run ipconfig.flacildines.

## [00:11:22]

![screenshot at 00:11:22](frames/frame_0026.jpg)

`[00:11:26]` I wanted to do it later.

## [00:11:40]

![screenshot at 00:11:40](frames/frame_0027.jpg)

`[00:11:50]` Password, login as a local administrator,

## [00:12:02]

![screenshot at 00:12:02](frames/frame_0028.jpg)

`[00:12:08]` because you haven't joined domain yet. `[00:12:11]` Next step, you need to verify your time zoom.

## [00:12:22]

![screenshot at 00:12:22](frames/frame_0029.jpg)

## [00:12:33]

![screenshot at 00:12:33](frames/frame_0030.jpg)

`[00:12:49]` Okay, 540 to make sure all the servers are located in the same zoom.

## [00:12:53]

![screenshot at 00:12:53](frames/frame_0031.jpg)

## [00:12:58]

![screenshot at 00:12:58](frames/frame_0032.jpg)

`[00:12:59]` Your join domain.

## [00:13:05]

![screenshot at 00:13:05](frames/frame_0033.jpg)

`[00:13:12]` So you're probably going to ask me, `[00:13:15]` why do we need join domain? `[00:13:17]` The reason we join domain is because it's for administration purpose. `[00:13:26]` So if you want to create a second reason, `[00:13:37]` VM99 IP address, as I told you before,

## [00:13:51]

![screenshot at 00:13:51](frames/frame_0034.jpg)

`[00:14:05]` I'm going to use this one. `[00:14:08]` I'm going to use server 5, you're going to use server 4.

## [00:14:36]

![screenshot at 00:14:36](frames/frame_0035.jpg)

## [00:14:53]

![screenshot at 00:14:53](frames/frame_0036.jpg)

## [00:14:57]

![screenshot at 00:14:57](frames/frame_0037.jpg)

## [00:15:07]

![screenshot at 00:15:07](frames/frame_0038.jpg)

## [00:15:13]

![screenshot at 00:15:13](frames/frame_0039.jpg)

## [00:15:20]

![screenshot at 00:15:20](frames/frame_0040.jpg)

## [00:15:37]

![screenshot at 00:15:37](frames/frame_0041.jpg)

## [00:15:44]

![screenshot at 00:15:44](frames/frame_0042.jpg)

`[00:15:46]` Okay, change the commit name. `[00:15:49]` You also can go to DC1 to verify.

## [00:16:29]

![screenshot at 00:16:29](frames/frame_0043.jpg)

## [00:16:46]

![screenshot at 00:16:46](frames/frame_0044.jpg)

## [00:16:55]

![screenshot at 00:16:55](frames/frame_0045.jpg)

## [00:17:01]

![screenshot at 00:17:01](frames/frame_0046.jpg)

`[00:17:03]` Commuter, if you can see server 5, `[00:17:06]` that means your secondary domain controller

## [00:17:09]

![screenshot at 00:17:09](frames/frame_0047.jpg)

`[00:17:10]` has been successfully to join domain. `[00:17:13]` Next step, you need to reboot. `[00:17:16]` So we're going to login as a domain administrator.

## [00:17:16]

![screenshot at 00:17:16](frames/frame_0048.jpg)

## [00:17:25]

![screenshot at 00:17:25](frames/frame_0049.jpg)

## [00:17:44]

![screenshot at 00:17:44](frames/frame_0050.jpg)

## [00:17:56]

![screenshot at 00:17:56](frames/frame_0051.jpg)

`[00:17:58]` So you're going to ask me, `[00:18:08]` can we login as a local administrator to install the `[00:18:12]` secondary domain controller, secondary DNS zoom? `[00:18:16]` The answer is yes. `[00:18:18]` You just need an administrator. `[00:18:21]` No matter for domain administrator or local administrator, `[00:18:26]` it doesn't matter. `[00:18:27]` If you believe you type the password is correct,

## [00:18:41]

![screenshot at 00:18:41](frames/frame_0052.jpg)

`[00:19:01]` but you cannot login. `[00:19:03]` So that means the keyboard may have some issues. `[00:19:08]` I had the problem before. `[00:19:12]` It looked like my keyboard is not compatible well `[00:19:17]` with the zoomware. `[00:19:19]` So if I use the caps lock, `[00:19:24]` so I supposed to use the capital key,

## [00:19:27]

![screenshot at 00:19:27](frames/frame_0053.jpg)

`[00:19:27]` but actually that is a small key. `[00:19:30]` So I want to use a small key, `[00:19:32]` but that is a capital key. `[00:19:35]` So it's really strange. `[00:19:37]` After reboot, everything is fine. `[00:19:39]` So this time I will teach you the different solutions

## [00:19:56]

![screenshot at 00:19:56](frames/frame_0054.jpg)

## [00:20:08]

![screenshot at 00:20:08](frames/frame_0055.jpg)

## [00:20:15]

![screenshot at 00:20:15](frames/frame_0056.jpg)

`[00:20:21]` to install the role and features. `[00:20:24]` You want to disable the edge.

## [00:20:34]

![screenshot at 00:20:34](frames/frame_0057.jpg)

## [00:20:41]

![screenshot at 00:20:41](frames/frame_0058.jpg)

## [00:20:49]

![screenshot at 00:20:49](frames/frame_0059.jpg)

`[00:21:15]` So you're also going to see the event critical. `[00:21:18]` Microsoft Windows kernel power. `[00:21:22]` So that means you choose the power off `[00:21:24]` or you lost power before. `[00:21:26]` I have these issues because one day I choose `[00:21:34]` Sadam by using my zoomware functions.

## [00:21:34]

![screenshot at 00:21:34](frames/frame_0060.jpg)

`[00:21:40]` And sometimes that can cause the issues. `[00:21:43]` So when you want to do Sadam from here, `[00:21:46]` don't use the zoomware Sadam.

## [00:21:48]

![screenshot at 00:21:48](frames/frame_0061.jpg)

`[00:21:52]` Sometimes this function will be considered as power off. `[00:21:55]` It's very strange. `[00:21:57]` That is a software issues. `[00:22:02]` I want to disable the edge.

## [00:22:04]

![screenshot at 00:22:04](frames/frame_0062.jpg)

`[00:22:04]` So you're probably going to ask me, `[00:22:10]` we need the browser.

## [00:22:10]

![screenshot at 00:22:10](frames/frame_0063.jpg)

`[00:22:13]` Why you want to disable that one? `[00:22:15]` So this is the server. `[00:22:16]` This is not a member server. `[00:22:18]` So you cannot use the browser on the server. `[00:22:23]` That can bring some virus. `[00:22:27]` Disable.

## [00:22:55]

![screenshot at 00:22:55](frames/frame_0064.jpg)

`[00:22:59]` Okay, so next we can install a role feature in here. `[00:23:02]` Add a role in feature. `[00:23:07]` Add the DNS on your server five. `[00:23:09]` But at this time I wanted to use a different way.

## [00:23:13]

![screenshot at 00:23:13](frames/frame_0065.jpg)

`[00:23:14]` So lock in your DC1. `[00:23:17]` I want to add a server five to my domain controller. `[00:23:23]` So that can help me to build or centralize the community environment. `[00:23:31]` I can use a wine server to manage all. `[00:23:34]` This is the reason why I ask you to join domain. `[00:23:48]` You will see that. `[00:23:53]` I can find a server five. `[00:23:56]` So next, add a role in features.

## [00:23:58]

![screenshot at 00:23:58](frames/frame_0066.jpg)

`[00:24:00]` I want to install on server five. `[00:24:02]` Okay, if you see all those agree `[00:24:13]` and you can reboot your server five. `[00:24:20]` You can reboot your server five. `[00:24:22]` This problem I saw in Windows Server 2019. `[00:24:27]` You can refresh or you can reboot.

## [00:24:33]

![screenshot at 00:24:33](frames/frame_0067.jpg)

`[00:24:34]` You can sign out and sign in.

## [00:24:38]

![screenshot at 00:24:38](frames/frame_0068.jpg)

## [00:24:43]

![screenshot at 00:24:43](frames/frame_0069.jpg)

`[00:24:45]` If doesn't work, reboot.

## [00:24:50]

![screenshot at 00:24:50](frames/frame_0070.jpg)

`[00:24:59]` See, after I log out. `[00:25:01]` In the login, you can see that I can install now. `[00:25:05]` It's only the first time. `[00:25:07]` And also I want you to spend time to read the descriptions for DNS. `[00:25:20]` Restore if needed. `[00:25:23]` Normally don't need it. `[00:25:24]` It's only for ADDS and HyperB. `[00:25:27]` Okay, I already successfully to install on the server five.

## [00:25:35]

![screenshot at 00:25:35](frames/frame_0071.jpg)

## [00:26:21]

![screenshot at 00:26:21](frames/frame_0072.jpg)

`[00:26:50]` So let's go to server five to take a look at. `[00:26:54]` I can refresh.

## [00:26:57]

![screenshot at 00:26:57](frames/frame_0073.jpg)

`[00:27:01]` You can see DNS manager pop up. `[00:27:11]` Okay, let's look at DC1.

## [00:27:18]

![screenshot at 00:27:18](frames/frame_0074.jpg)

`[00:27:27]` You also can connect to a DNS server. `[00:27:31]` You can connect this computer or you can connect to the following one. `[00:27:35]` You can connect the server five. `[00:27:47]` Okay, but this time I wanted to go to the server five. `[00:27:55]` Okay, I don't want to confuse you.

## [00:27:56]

![screenshot at 00:27:56](frames/frame_0075.jpg)

`[00:27:58]` Okay, so we're going to create a secondary zone. `[00:28:12]` We're going to use a new zone. `[00:28:14]` Next, secondary zone. `[00:28:18]` What is the stop zone? `[00:28:22]` Stop zone is to create a copy of a zoom. `[00:28:25]` Continue only the name server and that server. `[00:28:29]` Start authority and the possible clue a record. `[00:28:33]` So stop zone is used to forward to the name server primary zone and secondary zone. `[00:28:39]` We want to create a forward local zone.

## [00:28:41]

![screenshot at 00:28:41](frames/frame_0076.jpg)

`[00:28:45]` So what's the difference between the forward local zone and the reverse local zone? `[00:28:53]` We're going to use a delta and make sure if you use different domain name. `[00:29:02]` So you're going to put a different zone name IP address. `[00:29:08]` So you need to specify where you want to get as a data. `[00:29:15]` So we want to get a data from our server one, which is a primary zone. `[00:29:21]` So we're going to use IP. `[00:29:23]` You tap the valid IP address.

## [00:29:26]

![screenshot at 00:29:26](frames/frame_0077.jpg)

`[00:29:48]` Okay, so next you will see that successfully to create a delta zone.

## [00:30:11]

![screenshot at 00:30:11](frames/frame_0078.jpg)

`[00:30:51]` And in here you can see that there's no record. `[00:30:55]` And even you use the f5 to refresh.

## [00:30:56]

![screenshot at 00:30:56](frames/frame_0079.jpg)

`[00:31:01]` It doesn't work. `[00:31:06]` Why doesn't work? `[00:31:07]` Because this is a secondary zone. `[00:31:14]` So you're going to fetch the data from the primary zone. `[00:31:18]` So you need to make sure your primary zone allow you to fetch the data. `[00:31:24]` So we're going to go to DC1 and we're going to look at our forward local zone.

## [00:31:26]

![screenshot at 00:31:26](frames/frame_0080.jpg)

`[00:31:39]` And look at the property from here. `[00:31:47]` You will see zoom transfer. `[00:31:50]` So zoom transfer, you can configure in here. `[00:31:55]` So you can specify which server you're allowed to transfer all the DNS records. `[00:32:03]` Because DNS is the key components of your network infrastructures. `[00:32:10]` So if you allowed anyone to access your DNS record,

## [00:32:11]

![screenshot at 00:32:11](frames/frame_0081.jpg)

`[00:32:17]` that can cause the big issues for your network infrastructure. `[00:32:22]` Because we can know who is the DNS, who is the domain controller, who is the DCP. `[00:32:29]` So what kind of services you set up on your network. `[00:32:36]` So therefore, you only allowed some limited specified server can fetch the data. `[00:32:45]` So I'm going to allow only the following servers.

## [00:32:56]

![screenshot at 00:32:56](frames/frame_0082.jpg)

`[00:32:57]` I'm going to add an IP address. `[00:32:59]` This IP address is your secondary zone DNS server. `[00:33:06]` Click OK. `[00:33:14]` Apply. `[00:33:15]` OK. `[00:33:16]` So after you apply it, and then we can look at here. `[00:33:25]` Refresh.

## [00:33:31]

![screenshot at 00:33:31](frames/frame_0083.jpg)

`[00:33:31]` Just refresh a little bit. `[00:33:33]` And sometimes it will take less than 1 minute to get the data. `[00:33:39]` Sometimes it may take longer. `[00:33:41]` That is network. `[00:33:42]` Let's try again. `[00:34:05]` Refresh. `[00:34:07]` Refresh. `[00:34:08]` If that doesn't work, I'm going to delete that one. `[00:34:14]` To create again. `[00:34:15]` Yeah, you found it out.

## [00:34:16]

![screenshot at 00:34:16](frames/frame_0084.jpg)

`[00:34:56]` You found out right now I can get all the records. `[00:35:01]` Maybe I forgot to put it at .com.

## [00:35:01]

![screenshot at 00:35:01](frames/frame_0085.jpg)

`[00:35:05]` Maybe. `[00:35:06]` I think that probably the reason why I cannot fetch the data. `[00:35:14]` But I don't think so. `[00:35:15]` You know, last term I use the .com. `[00:35:18]` Without .com, that's fine. `[00:35:20]` But you know, if you have the problem, just put it at .com. `[00:35:25]` And double check to use your domain name. `[00:35:30]` OK. `[00:35:31]` How do you know this is the secondary zone? `[00:35:34]` Red click. `[00:35:36]` And you cannot create a new record in here.

## [00:35:39]

![screenshot at 00:35:39](frames/frame_0086.jpg)

`[00:35:47]` Refresh. `[00:35:49]` Because, you know, if you log in your DC1, I connect to server 5. `[00:35:54]` Server 5 is not a local server. `[00:35:57]` So sometimes it takes a while to fetch the data from the server 5.

## [00:36:03]

![screenshot at 00:36:03](frames/frame_0087.jpg)

## [00:36:08]

![screenshot at 00:36:08](frames/frame_0088.jpg)

`[00:36:09]` I'm going to close that one to re-log in.

## [00:36:16]

![screenshot at 00:36:16](frames/frame_0089.jpg)

`[00:36:20]` I want you to add a server, you know, to manage. `[00:36:24]` Because your computer is not powerful enough. `[00:36:27]` Sometimes, you know, the data delay or you're going to use more resource. `[00:36:32]` Your computer is going to extremely slow. `[00:36:35]` But in the production environment, you know, you can ignore that. `[00:36:39]` That's totally fine. `[00:36:40]` We can see that, you know.

## [00:37:01]

![screenshot at 00:37:01](frames/frame_0090.jpg)

`[00:37:05]` I can connect to the server 5, you know. `[00:37:08]` So I cannot create a new record. `[00:37:10]` If you go to the server 1, right click. `[00:37:16]` So I can create any new record. `[00:37:20]` I can create a record. `[00:37:24]` Because this is my web server. `[00:37:29]` IP address. `[00:37:30]` I type one more dot here.

## [00:37:46]

![screenshot at 00:37:46](frames/frame_0091.jpg)

`[00:37:58]` OK. `[00:38:02]` So I create the web. `[00:38:05]` This is for my web.

## [00:38:06]

![screenshot at 00:38:06](frames/frame_0092.jpg)

`[00:38:07]` So if I pin... `[00:38:09]` So you see that? `[00:38:15]` IP address is dot 11.

## [00:38:18]

![screenshot at 00:38:18](frames/frame_0093.jpg)

`[00:38:21]` OK. `[00:38:22]` Let's look at my secondary zone. `[00:38:39]` Let me take a while to get all the records. `[00:38:43]` It takes almost one minute after the refresh.

## [00:38:50]

![screenshot at 00:38:50](frames/frame_0094.jpg)

## [00:39:07]

![screenshot at 00:39:07](frames/frame_0095.jpg)

`[00:39:37]` And the records can stop in here. `[00:39:40]` So if a refresh doesn't work, I'm going to tell you another way. `[00:39:46]` So you can right click. `[00:39:48]` Choose reload. `[00:39:52]` So this one can ask the server to refresh.

## [00:39:52]

![screenshot at 00:39:52](frames/frame_0096.jpg)

`[00:39:58]` Force refresh to reload the data from the primary. `[00:40:03]` Or you can see transfer from master. `[00:40:07]` So use these two commands. `[00:40:09]` Two functions. `[00:40:11]` And you're going to see the record zone. `[00:40:15]` OK. `[00:40:18]` The next one I'm going to show you is as I told you before. `[00:40:23]` And this is the secondary zone. `[00:40:26]` You can change the room to the primary zone if you want. `[00:40:30]` If server 1 failed. `[00:40:33]` So you can change from the secondary zone to primary zone.

## [00:40:37]

![screenshot at 00:40:37](frames/frame_0097.jpg)

`[00:40:37]` And then you're going to have a full permission. `[00:40:40]` Which is read, write and modify permissions. `[00:40:44]` OK. `[00:40:45]` Otherwise, you only have read permissions. `[00:40:48]` You cannot create any record in here.

## [00:40:51]

![screenshot at 00:40:51](frames/frame_0098.jpg)

`[00:40:51]` After I add the server 5 to my server 1, DNS manager. `[00:41:08]` So it's extremely slow. `[00:41:15]` I believe probably that is the bug for the 2022. `[00:41:19]` And I want you to try on your 2019. `[00:41:23]` Do you have the similar issues? `[00:41:27]` OK. `[00:41:31]` OK. `[00:41:32]` So this is for the lab. `[00:41:33]` And also the questions is ask you to create a DNS namespace.

## [00:41:36]

![screenshot at 00:41:36](frames/frame_0099.jpg)

`[00:41:45]` OK. `[00:41:46]` So suppose you work for one company. `[00:41:48]` And you have the following servers. `[00:41:51]` You're going to create the server name for each one. `[00:41:55]` For example, human resource file server. `[00:41:59]` So you can create a human resource folders here. `[00:42:15]` And then you can create a new delegation. `[00:42:19]` OK. `[00:42:20]` And then you can create the file server record in here.

## [00:42:21]

![screenshot at 00:42:21](frames/frame_0100.jpg)

`[00:42:29]` Some students probably ask me, hey, I don't want to create a new delegation. `[00:42:34]` I don't want to create a new domain. `[00:42:36]` So how should I do? `[00:42:39]` You also can create a folder in here. `[00:42:42]` Create a folder. `[00:42:44]` But I need you to create a new domain. `[00:42:48]` OK. `[00:42:49]` You can create a new domain for HR. `[00:42:53]` Click OK. `[00:42:57]` So this is a folder. `[00:42:59]` And in here you can create a new file server. `[00:43:03]` Let's look at the DNS record. `[00:43:06]` You don't need to create a physical to create a domain controller.

## [00:43:06]

![screenshot at 00:43:06](frames/frame_0101.jpg)

`[00:43:10]` OK. `[00:43:11]` But you need to create a folder in here. `[00:43:14]` That is a new domain. `[00:43:16]` So HR file server can call that one file. `[00:43:22]` File one. `[00:43:27]` OK. `[00:43:28]` You can see that. `[00:43:29]` It's file.hr.adultum.com. `[00:43:33]` You can give IP. `[00:43:35]` You can use 208.10. `[00:43:42]` It's up to you. `[00:43:43]` OK. `[00:43:48]` It is a seminar for the web server.

## [00:43:49]

![screenshot at 00:43:49](frames/frame_0102.jpg)

`[00:43:52]` OK. `[00:43:53]` You can create a web server in here. `[00:43:56]` 192. `[00:44:03]` 209.0. `[00:44:04]` 12. `[00:44:05]` So I want you to create several DNS record in here.

## [00:44:16]

![screenshot at 00:44:16](frames/frame_0103.jpg)

`[00:44:17]` And also fill out this form. `[00:44:19]` OK. `[00:44:20]` If you have any questions, let me know. `[00:44:24]` OK. `[00:44:25]` Bye-bye.
