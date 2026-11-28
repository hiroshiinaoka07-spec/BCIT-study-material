# Transcript: w12_vid1_logs_pseudocode.mp4

- Source: `C:\Users\hiros\BCIT-study-material\Algorithms\week 12 quiz\w12_vid1_logs_pseudocode.mp4`
- Duration: 00:21:18
- Segments: 188, screenshots: 29
- Whisper model: `large-v3` (auto-generated; may contain recognition errors)

## [00:00:00]

![screenshot at 00:00:00](frames/frame_0001.jpg)

`[00:00:01]` Hello! This is a video about logarithms. We've looked at a few things about logarithms previously. `[00:00:09]` We've looked at sort of improving our intuition about what logarithms are even for. And we looked `[00:00:35]` at how to do empirical estimation of a logarithm when we've got a bunch of timing data. So anyway,

## [00:00:45]

![screenshot at 00:00:45](frames/frame_0002.jpg)

`[00:00:58]` that's all well and good. Currently, we're interested in two things. We're interested in `[00:01:06]` spotting logarithmic behavior in code or in pseudocode. And we're interested in `[00:01:25]` sort of, is it just logarithms on their own or can other stuff happen too?

## [00:01:30]

![screenshot at 00:01:30](frames/frame_0003.jpg)

`[00:01:30]` Okay, so that's kind of what's on the on the schedule for this video. `[00:01:37]` So I want to remind you back here, `[00:01:40]` in terms of our intuition about this, that a logarithm is the mathematical phrasing of `[00:01:46]` the question, you know, if I say log base b of x, what that means is how many times would I have to `[00:02:04]` multiply by b to get from 1 to x? Or alternately, if I was going the other direction,

## [00:02:15]

![screenshot at 00:02:15](frames/frame_0004.jpg)

`[00:02:24]` then it would be dividing instead of multiplying. So you have that line `[00:02:27]` up the same number of letters just because I did that underlying thing. `[00:02:31]` So this is what logarithms are for. Is there the math that matches this? Well, `[00:02:36]` this is sort of math still, but it's a bit more, a bit less formal math. `[00:02:41]` So for example, if I ask for the log base 2, let me see, I have to look this number up. `[00:02:47]` I should have it memorized, but I don't. It's 32,768. That is to say how many twos to get to 32k.

## [00:03:00]

![screenshot at 00:03:00](frames/frame_0005.jpg)

`[00:03:00]` Let's see. One, two, sorry, one, I mean there. Two, three, four, five, six. Should I keep going? `[00:03:11]` Anyway, it's 15, I think. So, you know, we're going to have to do this 15 numbers here, `[00:03:18]` plus the one at the beginning, and that's going to get us up to there. So that's what logs are. `[00:03:25]` That's old news though, right? So the question here is, what does this look like in code, right? `[00:03:31]` When we see code, what sort of code is going to make us think that this might be happening and `[00:03:35]` think that our asymptotic complexity might be a logarithm? And don't get me wrong, it can look `[00:03:40]` like all sorts of things. There's not like one pattern. You're like, ah, I saw the pattern. `[00:03:44]` That's it. Or I didn't see the pattern. It's not a log. Like, I don't want to pretend everything's

## [00:03:45]

![screenshot at 00:03:45](frames/frame_0006.jpg)

`[00:03:49]` always simple, but it is pretty common that we see something that actually involves something `[00:03:55]` getting cut in half over and over and over again, or cut more or less than half, or occasionally it `[00:04:00]` gets cut into some other ratio. So that's something that's going to make us think that this might be `[00:04:01]` like thirds or quarters, or sometimes it gets doubled. You know, this kind of like literally `[00:04:06]` matching this pattern is not that rare, right? So it's not a hundred percent of the story, `[00:04:12]` but it's a big chunk. And the most common example of that is cutting a list in half.

## [00:04:30]

![screenshot at 00:04:30](frames/frame_0007.jpg)

`[00:04:32]` And that's the example that we're going to review. Okay. So I've got a function. `[00:04:46]` I'm going to start off. In this case, I'm going to implement this recursively. `[00:04:56]` If `[00:04:57]` the haystack has no capacity, then the needle can't be in it. So we're going to return `[00:05:03]` a failure indicator, which I've decided to use none here. And then I'm going to say, `[00:05:09]` well, what's the halfway index? Okay. So that's the index that's halfway through the haystack

## [00:05:15]

![screenshot at 00:05:15](frames/frame_0008.jpg)

`[00:05:20]` letting us say something like this, right? So if we can find the needle at this location, `[00:05:33]` and that's the thing we should return. There hand, if it's not right there and the thing we find there `[00:05:48]` is bigger than the needle then if we happen to know that the haystack is a sorted list which `[00:05:54]` is a thing i haven't told you until now then we could cut it in half and then we go looking in

## [00:06:00]

![screenshot at 00:06:00](frames/frame_0009.jpg)

`[00:06:10]` that second half on the other hand if it's not finding it and it's not gonna go left `[00:06:26]` then we it could go right like i got that minus one there correct i hope anyway uh i i think

## [00:06:45]

![screenshot at 00:06:45](frames/frame_0010.jpg)

`[00:06:47]` that's right but if it's wrong just pretend it's right okay now two facts about this function before `[00:06:53]` we get going in our real work the first is have you recognized this yet right is this a function `[00:07:00]` that we've already studied that you should recognize that i gave a stupid name to on purpose `[00:07:03]` okay and second there's actually a bug in this implementation uh and i'm not counting `[00:07:09]` the possibility of off by one error here or somebody somewhere else uh `[00:07:13]` maybe i mean that actually anyway look i'm not counting it off by one error here `[00:07:19]` i'm not counting it off by one error here i'm not counting it off by one error here `[00:07:19]` there's another bug here right this will not correctly find the index of the needle `[00:07:25]` in the input list except in certain special cases and this is not uh purely hypothetical when we

## [00:07:30]

![screenshot at 00:07:30](frames/frame_0011.jpg)

`[00:07:33]` studied this function earlier in the semester some students tried to do it more or less this way and `[00:07:39]` they got an error and i said i want you to solve without recursion there's two reasons one is that `[00:07:44]` i want to study recursion later and the other is that the way you're doing it it's easy to make a `[00:07:49]` mistake and i don't want to just give you the answer i want you to figure out for yourself and `[00:07:51]` it's hard to figure out if you're doing recursively blah blah blah this isn't really recursion's fault `[00:07:56]` it just kind of works out clumsiness anyway it's all a bit of a digression so maybe at this point `[00:08:00]` in the semester you're sophisticated enough that you can fix this bug um as this implementation of `[00:08:06]` this well-known function binary search obviously if you look it up you're not learning anything so

## [00:08:15]

![screenshot at 00:08:15](frames/frame_0012.jpg)

`[00:08:16]` i don't you know why bother you have to figure it out for yourself okay so moving on to our real thing `[00:08:24]` let's count let's do an analysis of this asymptotically right so we're gonna start `[00:08:29]` by just not counting the recursive calls and look at all the rest of it `[00:08:33]` okay so this is linear work len is linear um it's some magic i don't actually understand `[00:08:41]` but it is linear oh sorry oh my goodness i'm saying all wrong let me just back that up i `[00:08:47]` was just testing you i was just testing you that wasn't me being confused len is constant time `[00:08:54]` some kind of magic but it is true checking for equality is constant time doing if is constant `[00:08:58]` time do lan again still constant time divide by two constant time assigned to a variable constant time

## [00:09:00]

![screenshot at 00:09:00](frames/frame_0013.jpg)

`[00:09:05]` look up something in a list to find out if it is something or not test equality do an if more `[00:09:10]` constant time more constant time more constant time more constant whoop hate it when that happens `[00:09:15]` more constant time more constant time okay so it's all constant actually i lied this slice is linear time `[00:09:38]` so for reasons we're going to both ignore the recursive calls for a second but only for well

## [00:09:45]

![screenshot at 00:09:45](frames/frame_0014.jpg)

`[00:09:45]` just for one minute we're also going over the slices well the slices actually are linear but `[00:09:51]` it turns out there's a way to get rid of the slicing here but it makes the rest of the code `[00:09:54]` a little bit harder to read so to keep this code easier to read i'm not fixing this problem right `[00:10:02]` so hopefully i get around to discussing that later like maybe in class or maybe another week how to do `[00:10:07]` this in the equivalent of this in actually constant time but doing it actually like this `[00:10:13]` is linear and it makes the whole thing a lot slower so just pretend i did it the fancy way `[00:10:20]` it's harder to read and so this is just pretend that this is constant time right and that applies

## [00:10:30]

![screenshot at 00:10:30](frames/frame_0015.jpg)

`[00:10:39]` up here as well okay if we ignore those two things then this is all constant time `[00:10:53]` so i you know so what right so i said i was only ignore the recursion for a minute so now we're not `[00:10:58]` ignoring the recursion so if we stop ignoring the recursion then we can see that it starts `[00:11:05]` somewhere it does a bunch of constant time work and it might either do this recursive `[00:11:11]` call or this recursive call and then it goes up to the top and it does some stuff and it does

## [00:11:15]

![screenshot at 00:11:15](frames/frame_0016.jpg)

`[00:11:15]` either it just stops or stops or it does a recursive call on a recursive call `[00:11:22]` right so the total cost is big o of one times the number of recursive `[00:11:28]` calls it makes how many recursive calls does it make right does that make sense in a video i can't `[00:11:41]` wait for you to uh say yes or no oh i put this on the wrong line okay so except for the slices which `[00:11:50]` we could fix and the recursive calls it's all constant time so when we bring the recursive `[00:11:57]` calls back in the total cost is the constant times the number of recursive calls how many

## [00:12:00]

![screenshot at 00:12:00](frames/frame_0017.jpg)

`[00:12:03]` recursive calls does it make becomes the important question right and so if you imagine that `[00:12:07]` initially i run this on a haystack say i have a haystack with length right that's a weird choice `[00:12:17]` jeremy 16. and after it hits one if it hasn't stopped by now then when it splits it again `[00:12:39]` it'll go down to zero then that's got to be the last one my spelling mistakes plague me right so

## [00:12:45]

![screenshot at 00:12:45](frames/frame_0018.jpg)

`[00:12:55]` and if you go all the way up to 32 it's really just one more step `[00:12:58]` right so the point is how many recursive calls does it make makes big o of log base 2 of n `[00:13:14]` which we tend to write as just big o of login and that's how we write that okay so `[00:13:24]` that's the sort of pattern you know i mean it's not the only one by far but i said that we will `[00:13:29]` often see in our code just something literally being cut in half over and over again until it

## [00:13:30]

![screenshot at 00:13:30](frames/frame_0019.jpg)

`[00:13:35]` eventually hits one and then maybe it goes one more round to go to zero and this is just like `[00:13:40]` that we have this cutting `[00:13:41]` in half here and so therefore the next call is on half as much list and then it goes round again `[00:13:51]` and then the next call maybe it's this one this time is on half as much list another time and so `[00:13:55]` on the list shrinks by halves so it takes logarithmic number of times to get all the `[00:13:59]` way down to the base okay now i don't want you to get into some trap and think oh i see recursion `[00:14:09]` and i see dividing by two of course it's logarithms so i'm going to show you another example `[00:14:14]` that looks kind of similar but actually

## [00:14:15]

![screenshot at 00:14:15](frames/frame_0020.jpg)

`[00:14:18]` it's a trick okay so so watch for the trick so i'm going to find the minimum element of a list `[00:14:35]` now this is even aside from the fact that i'm going to trick you pretend that's you know `[00:14:39]` pretend that we don't care about that right this is not a better way `[00:14:43]` than the obvious way to find a minimum where you just make a loop and you `[00:14:47]` have a best and you keep going until you find the something better and as long as you find a better `[00:14:52]` you preserve it and so on this is not better than that it's not really worse either it's just

## [00:15:00]

![screenshot at 00:15:00](frames/frame_0021.jpg)

`[00:15:00]` different i guess but anyway it's just what it is so pretend somebody wrote this code `[00:15:07]` and then you were going to try to um uh try to guess its big o complexity right `[00:15:18]` if the number of numbers is zero then you shouldn't be trying to find the minimum that's a that's a `[00:15:30]` mess up right `[00:15:31]` if the number of numbers is one then the minimum of a list of one is that value right the minimum `[00:15:41]` the maximum the average are all the same there's only one thing in the list so these are going to

## [00:15:45]

![screenshot at 00:15:45](frames/frame_0022.jpg)

`[00:15:45]` be our base case well this is our sort of proper base case and this is our um explosion base case `[00:15:52]` um and then we're gonna do this business up here again right where we grab some of this `[00:16:11]` code actually i'm just gonna grab a bunch of this code and edit it let's grab a bunch of this code `[00:16:16]` let's see i want `[00:16:17]` all right so i have this one `[00:16:21]` and i want this one and i want this one and i want this one maybe that's it for now um

## [00:16:30]

![screenshot at 00:16:30](frames/frame_0023.jpg)

`[00:16:41]` okay so because there's `[00:16:45]` more than one here these must have at least `[00:16:49]` oh i changed the name gotta fix all this oops okay because there's more than one there's only `[00:16:55]` one we stopped here so there's more than one so there's either these two have the same one we're `[00:16:57]` So, these will each have, oh, I got to change this part here. `[00:17:02]` It doesn't apply anymore. `[00:17:03]` These will each have at least one of them. `[00:17:05]` So, I can safely call mid on them. `[00:17:06]` So, I'm going to do that, right? `[00:17:08]` I'm going to go, so, what did I do?

## [00:17:15]

![screenshot at 00:17:15](frames/frame_0024.jpg)

`[00:17:36]` I cut the list in half, and then I went and checked the left, and I checked the right, right? `[00:17:42]` And then whichever one of those two is smaller, that's my overall smallest one, right? `[00:17:47]` Now, this is a correct implementation of minimum, and it is recursive. `[00:17:52]` I mean, I think it is. `[00:17:52]` I don't know. `[00:17:52]` I didn't test it. `[00:17:53]` Maybe you should test it for me. `[00:17:55]` It is recursive, as it happens, and there is something sort of logarithmic about it.

## [00:18:00]

![screenshot at 00:18:00](frames/frame_0025.jpg)

`[00:18:02]` But nonetheless, the total is not logarithmic. `[00:18:05]` Why? `[00:18:06]` Well, because if I first do it on eight things, then when that gets split in half, the first `[00:18:15]` four have to be done, but also the next four have to be done. `[00:18:22]` And when I split those in half, those have to be done, and those have to be done, and `[00:18:26]` those have to be done. `[00:18:27]` And those have to be done. `[00:18:27]` And those have to be done. `[00:18:27]` And I split those in half, that has to be done, that has to be done, that has to be `[00:18:29]` done, that has to be done, that has to be done, that has to be done, that has to be `[00:18:31]` done, that has to be done, that has to be done, right? `[00:18:32]` And so the point is, they all eventually get done. `[00:18:41]` So this does not end up just going eight, four, two, one, down one of the paths.

## [00:18:45]

![screenshot at 00:18:45](frames/frame_0026.jpg)

`[00:18:49]` It has to go down all the paths. `[00:18:52]` And because it goes down all the paths, it's not only not logarithmic, it's in fact slower `[00:18:57]` than linear. `[00:18:59]` We'll come back to that in class. `[00:19:02]` So, you know, I want you to, like, remember to apply your critical thinking, right? `[00:19:10]` I've had people in past exams just say, it's recursive, so it's logarithmic. `[00:19:15]` That is not only the correct, not the correct answer, it's not a good way to get part marks `[00:19:19]` either, right? `[00:19:21]` You have to apply your brain a little bit and think about, you know, does it go down `[00:19:25]` one path or something else? `[00:19:26]` But that said, when you see this halving, I'm not saying that guarantees logarithmic,

## [00:19:30]

![screenshot at 00:19:30](frames/frame_0027.jpg)

`[00:19:32]` but it should make you think about logarithms and you should be, like, looking, you should `[00:19:37]` be on the alert for the possibility it's logarithmic. `[00:19:39]` That's what I'm saying. `[00:19:42]` Okay? `[00:19:44]` So that's a short introduction to the most common pattern in code that causes big O of `[00:19:49]` log n behavior with both a genuine example and a kind of a false alarm example. `[00:19:58]` Okay? `[00:19:58]` So just in parting, here's a sort of a... `[00:20:02]` Parting question for you. `[00:20:06]` I feel sort of like I'm fumbling my words tonight.

## [00:20:15]

![screenshot at 00:20:15](frames/frame_0028.jpg)

`[00:20:18]` What is the asymptotic behavior if you do big O of log n loops, or like, if you do a `[00:20:30]` loop that goes, that runs big O of log n times, and inside that loop, here, I'll just put `[00:20:39]` it inside in the file here. `[00:20:41]` You do... `[00:20:41]` You do big O of log, big O of n work, right? `[00:20:48]` And actually I have another question as well, which is what is the asymptotic behavior if you have a loop, `[00:20:56]` an outer loop that runs n times, and inside that loop, you do big O of log n work.

## [00:21:00]

![screenshot at 00:21:00](frames/frame_0029.jpg)

`[00:21:07]` Okay? `[00:21:08]` So these are just little things for you to think about, set up to prepare you for class. `[00:21:12]` And I'm just going to leave you with those two thoughts. `[00:21:16]` And that's it.
