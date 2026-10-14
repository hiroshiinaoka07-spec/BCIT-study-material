# Transcript: 6.2 Create IAM role with S3 permissions [1_9sl6sq6n].mp4

- Source: `C:\Users\hiros\study stuff for cursor\Cloud-comp\6.2 Create IAM role with S3 permissions [1_9sl6sq6n].mp4`
- Duration: 00:01:00
- Segments: 5, screenshots: 2
- Whisper model: `large-v3` (auto-generated; may contain recognition errors)

## [00:00:00]

![screenshot at 00:00:00](frames/frame_0001.jpg)

`[00:00:06]` While you may be familiar with IAM users and groups, there is another way to work with permissions in AWS that is fairly common, and chances are you're going to be using them at some point. `[00:00:19]` They're called IAM roles. Roles can be assumed by certain types of principles, whether that is an IAM user or a federated identity or an AWS resource like an EC2 instance. `[00:00:32]` And so we're going to take a look at a scenario where we have an application running on EC2, and we need to grant access to that application to be able to work with an S3 bucket.

## [00:00:45]

![screenshot at 00:00:45](frames/frame_0002.jpg)

`[00:00:45]` So the first thing we're going to do is we're going to go to S3, and let's identify the bucket that we want to use here. `[00:00:52]` The one that we're going to be working with is called BreakKeyDemoS3Bucket. I'm just going to go ahead and copy that name into the buffer.
