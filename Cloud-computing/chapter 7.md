Chapter 7
The Core Compute Services
THE AWS CERTIFIED CLOUD PRACTITIONER EXAM OBJECTIVES COVERED IN THIS CHAPTER MAY INCLUDE, BUT ARE NOT LIMITED TO, THE FOLLOWING:

Domain 3: Technology
images 3.1 Define methods of deploying and operating in the AWS Cloud
images 3.3 Identify the core AWS services
Domain 4: Billing and Pricing
images 4.1 Compare and contrast the various pricing models for AWS
images 4.2 Recognize the various account structures in relation to AWS billing and pricing
images 

Introduction
While Elastic Compute Cloud (EC2) wasn’t quite the first service announced by AWS, once it did show up in 2006, it became the obvious cornerstone tool for many cloud deployments. EC2 faithfully mirrors the functionality of traditional on-premises data centers: you provision and launch virtual servers (known as instances) to run the same kinds of application workloads that would once have kept legacy servers busy. The fact that EC2 instances are more resilient and scalable and, often, cheaper than their on-premises cousins was just a happy bonus.

In the years since EC2 appeared, Amazon has introduced other compute tools aimed at providing the same end-user experience but through a simplified or abstracted interface. In this chapter, you’ll learn about how it all happens using EC2 and its more lightweight counterparts like Elastic Beanstalk, Lightsail, Docker (including via the Kubernetes orchestrator), and Lambda.

Deploying Amazon Elastic Compute Cloud Servers
To get your virtual machine (VM) instance running, you’ll first define the elements one at a time. Rather than installing an operating system and a software stack from scratch the traditional way, you’ll select an Amazon Machine Image (AMI). Instead of choosing the right CPU, memory modules, and network adapters and adding them to your physical motherboard, you’ll choose the instance type matching your application needs. And rather than purchasing storage drives and sliding them into your server chassis, you’ll define virtual storage volumes available through the Elastic Block Store (EBS).

Let’s see how all that works.

Amazon Machine Images
An image is a software bundle that was built from a template definition and made available within a single AWS Region. The bundle can be copied to a freshly created storage volume that, once the image is extracted, will become a bootable drive that’ll turn the VM it’s attached to into a fully operational server.

The nice thing about AMIs is that they’re available in so many flavors. You can select AMIs that will give you clean, cloud-optimized operating systems like official versions of Red Hat Enterprise Linux (RHEL), Ubuntu, Windows Server, or Amazon’s own Amazon Linux. But you can also find the OS you need preloaded with one of hundreds of popular software stacks like OpenVPN (secure remote connectivity), TensorFlow (neural networks), or a Juniper firewall already installed and ready to go.

AMIs are organized into four collections: the Quick Start set, any custom AMIs you might have created, the AWS Marketplace, and Community AMIs.

Using Quick Start AMIs
AWS makes the three dozen or so most popular AMIs easily available through the Quick Start tab on the Choose An Amazon Machine Image page—the first page you’ll face when you choose the Launch Instance button in the EC2 Dashboard. For the most part, they’re Free Tier–eligible. This means that launching them on a lightweight instance type within an account’s first year will, as you saw in Chapter 2, “Understanding Your AWS Account,” incur no costs.

The available Linux distributions you’ll find here are mostly categorized as long-term support (LTS) releases, meaning that they’ll be eligible for security and functional updates for at least five years from their original release date. This can be an important consideration for deployment planning since you will often prefer not to have to rebuild your production servers any more than absolutely necessary.

Even outside of the Free Tier, the use of the open source operating systems like Ubuntu and CentOS will always be free. But other choices—like Windows Server and RHEL—will carry the normal licensing charges. Once you launch an instance running one of those images, the charges will be billed through your AWS account.

Besides the general-purpose OS choices available through Quick Start, you can also find images optimized for deep learning, container hosting, .NET Core, and Microsoft SQL Server. Figure 7.1 shows two listings in the Quick Start menu. Note how the OS, release number, volume type (solid-state drive—SSD—in this case), AMI ID, and preferred hardware architecture—64-bit (x86) is selected in this case—are displayed.

The figure shows a couple of EC2 AMI listings displaying features and options.
FIGURE 7.1 A couple of EC2 AMI listings displaying features and options

Using AWS Marketplace and Community AMIs
AWS Marketplace is a software store managed by Amazon where vendors make their products available to AWS customers as ready-to-run AMIs (or, alternatively, in additional formats like CloudFormation stacks and containers). Companies like SAP, Oracle, and NVIDIA will package their software solutions into AMIs, often running on one or another Linux distribution.

When you select a Marketplace AMI, you’ll be shown its total billing cost, broken down into separate software license and EC2 infrastructure amounts. The Barracuda CloudGen Firewall AMI, for example, would, at the time of writing, cost $1.68 USD each hour for the software and $0.192 for an M5 Extra Large EC2 instance type, for a total hourly charge of $1.872. Running the same AMI on a much larger M5 Quadruple Extra Large instance type would cost you $5.72 for the software and $0.768 for the instance.

Marketplace AMIs will often offer a limited-time free trial for their software and reduced annual subscription rates. You can also view and search through Marketplace offerings outside of the EC2 Launch Instance interface through the Marketplace site: https://aws.amazon.com/marketplace.

Looking for a more specialized image built with a software stack that’s not available in the Quick Start or Marketplace tab? There are more than 100,000 AMIs to choose from in the Community AMIs tab. Some are supported by recognized vendors such as Canonical, but others are provided as is, often by end users like you. Given the informal sources of some Community AMIs, you must take responsibility for the security and reliability of AMIs you launch. Why not take a quick look at the process by working through Exercise 7.1?

EXERCISE 7.1
Select an EC2 AMI
From the EC2 Dashboard, choose the Launch Instance button.
With the Quick Start tab selected, scroll through the available options, noting the various operating systems (Amazon Linux, SUSE Linux, Windows, etc.).
Try to identify each one’s OS and release number (Ubuntu 18.04, for example), volume type (SSD), AMI ID (for instance, ami-0ac019f4fcb7cb7e6), and the choice of hardware architecture (in most cases, it’ll be either 64-bit x86 or 64-bit ARM).
Now switch to the AWS Marketplace tab, scroll down to the links to specific categories, and choose the Business Intelligence link.
Enter RapidMiner in the search field, and you should see two options: purchase a license along with the AMI, or bring your own license (BYOL) version. While RapidMiner is a popular data analytics tool, it’s only used here as an illustrative example.
Unless you want to go ahead and launch a new instance right now—and are aware of any costs you might incur—choose Cancel and Exit.
Creating Your Own AMIs
It’s possible to convert any EC2 instance into an AMI by creating a snapshot from the EBS volume used with an instance and then creating an image from the snapshot. The resulting image will be available as an AMI either in the AMIs menu on the EC2 Dashboard or on the My AMIs tab in the Choose An Amazon Machine Image page of the instance launch process.

But why bother? Well, suppose you’ve spent a full week carefully configuring an instance as your company’s application server. In fact, you did such a good job that you’d now like to be able to deploy exact copies of the instance to meet growing demand for your application. One way to make that both possible and painless is to create an AMI from your instance and select the AMI whenever another instance is needed.

Understanding EC2 Instance Types
An EC2 instance type is simply a description of the kind of hardware resources your instance will be using. The t2.micro instance type, for instance, comes with 1 GB of memory, low-to-moderate data transfer rates to network connections, and one virtual CPU (vCPU) running on a 2.5 GHz Intel Xeon processor. A c5d.18xlarge instance type, on the other hand, gives you 72 vCPUs on a 3 GHz Intel Xeon Platinum 8124M processor, and 144 GB of memory. You’ll use the instance type definitions to figure out the best match for your application.

A vCPU, by the way, is an arbitrary—and somewhat mysterious—metric used by AWS to describe the compute power you’ll get from a given instance. It’s meant to make you think in terms of the multiprocessor CPUs on consumer and server motherboards, where more is generally better. But it’s notoriously difficult to accurately map the value of a single vCPU against any one real-world device.

While, in general, the more vCPUs and memory you get, the better your instance will perform, that’s definitely not the whole story. EC2 offers instance type families that are optimized for very different computing tasks. The T2, T3, and M5 types are included in the general-purpose family because of their ability to perform well for a wide range of uses. Besides general-purpose, EC2 also offers compute-optimized, memory-optimized, accelerated-computing, and storage-optimized families of instance types. Table 7.1 lists the families and types available at the time of writing. Although you should be aware that this will constantly change, the most up-to-date list will always be available here: https://aws .amazon.com/ec2/instance-types.

TABLE 7.1 EC2 Instance Type Families (At the Time of This Writing)

Family	Instance types
General purpose	A1 T3 T2 M5 M5a M4 T3a
Compute optimized	C5 C5n C4
Memory optimized	R5 R5a R4 X1e X1 High Memory z1d
Accelerated computing	P3 P2 G3 F1
Storage optimized	H1 I3 D2
The bottom line is that choosing the right instance type family will sometimes let you get away with fewer vCPUs and less memory—and a lower cost.

If regulatory restrictions or company policy requires you to use only physically isolated instances, you can request either a dedicated instance or a dedicated host. What’s the difference? A dedicated instance is a regular EC2 instance that, instead of sharing a physical host with other AWS customers, runs on an isolated host that’s set aside exclusively for your account. A dedicated host also gives you instance isolation but, in addition, allows a higher level of control over how your instances will be placed and run within the host environment. Dedicated hosts can also simplify and reduce the costs of running licensed software. Both levels involve extra per-hour pricing and are available using on-demand, reserved, or spot models (which we’ll discuss a bit later in this chapter).

Server Storage: Elastic Block Store and Instance Store Volumes
Like everything else in the cloud, the storage volumes holding your instance’s OS and data are going to be virtual. In most cases, that’ll mean the 20 or 30 (or 2,000) GB drive holding your application is really just a 20 or 30 GB partition cleverly disguised to look like a stand-alone device. In fact, however, it was actually carved out of a much larger drive. What’s going on with the rest of the drive space? It’s probably being used for instances run by other AWS customers.

Some instance types support only volumes from the Elastic Block Store (EBS), others get their storage from instance store volumes, and some can happily handle both.

Amazon Elastic Block Store
The physical drive where an EBS volume actually exists may live quite a distance from the physical server that’s giving your instance life. Rather than connecting directly to the motherboard via, say, a SATA cable the way a physical drive plugs into a physical computer, EBS volumes speak with your instance over a super low-latency network connection spanning the data center.

As fast as the EBS-EC2 responses are, they’re still not quite as good as the experience you’ll get from EC2 instance store volumes. So, what does EBS offer to compensate?

Unlike the instance store that’s ephemeral, the data stored on EBS volumes will survive shutdowns and system crashes. That can be a factor for workloads where data persistence is necessary.
EBS volumes can be encrypted, which, when you’re working with sensitive data, can make a big difference.
EBS volumes can be moved around, mounted on other instances, and, as you’ve seen, converted to AMIs.
Amazon EC2 Instance Store Volumes
Unlike EBS, those instance types compatible with instance store volumes can enjoy the benefits of having their data on physical drives attached directly to the physical instance server. The downsides of instance store volumes (ephemeral data, no encryption, and lack of flexibility) are offset by faster data reads and writes. This can be useful for processing and analyzing fast-moving data streams where the data itself doesn’t need to be persistent.

Understanding EC2 Pricing Models
What you’ll pay for your EC2 instances will depend on the way you consume the service. Here’s where you’ll learn about the consumption options EC2 offers.

On-Demand Instances
The most expensive pricing tier is on-demand, where you pay for every hour the instance is running regardless of whether you’re actually using it. Depending on the instance type you’re using and the AWS Region where it’s running, you could pay as little as $0.0058 per hour (that’s around half a U.S. penny) for a t2.nano or as much as $24.48 per hour for a p3.16xlarge.

On-demand is great for workloads that need to run for a limited time without interruption. You could, for instance, schedule an on-demand instance in anticipation of increased requests against your application—perhaps your ecommerce site is offering a one-day, 50% off sale. But running an on-demand instance 24/7 for months at a time when you need it for only a couple of hours a day is going to cost you far more than it’s worth. Instead, for such cases you should consider an alternative pricing model.

Reserved Instances
If your application needs to run uninterrupted for more than a month at a time, then you’ll usually be better off purchasing a reserved instance. Practically, however, you’re unlikely to find an available reservation with a term shorter than 12 months. One- and three-year terms are always available.

As it turns out, when you go shopping for a reservation, you’re not actually purchasing an instance of any sort. Instead, you’re paying AWS—or other AWS customers who are selling reservations they’re no longer using—for the right to run an EC2 instance at a specified cost during the reservation term. Once you have your reservation, it will automatically be applied against any instance you launch in the specified AWS Region that matches the reservation instance type.

Reserved instances are paid for using an All Upfront, Partial Upfront, or No Upfront payment option. Predictably, the more you pay up front, the less it’ll cost you overall.

Spot Instances
For workloads that don’t need to run constantly and can survive unexpected shutdowns, your cheapest option will probably involve requesting instances on the EC2 spot market. AWS makes unused compute capacity available at steep discounts—as much as 90% off the on-demand cost. The catch is that the capacity can, on two minutes’ notice, be reclaimed by shutting down your instance.

This wouldn’t be an option for many typical use cases that require persistence and predictability. But it can be perfect for certain classes of containerized big data workloads or test and development environments.

Spot deployments can also be automated by defining your capacity and pricing needs as part of a spot fleet. The use of spot instances can, in addition, be incorporated into sophisticated, multitier operations that are deeply integrated with other automation and deployment orchestration tools. The https://aws.amazon.com/ec2/spot page provides helpful background and links.

Why not follow the steps in Exercise 7.2 to configure and launch an actual EC2 on-demand instance from start to finish?

EXERCISE 7.2
Launch an Apache Web Server on an EC2 Instance
From the EC2 Dashboard, choose the Launch Instance button. With the Quick Start tab selected, choose the Select button next to one of the Amazon Linux instance types.
On the Choose An Instance Type page, make sure the box next to the t2.micro entry is selected, and choose Next: Configure Instance Details.
Accept the default settings, but expand the Advanced Details section at the bottom of the page. You’re going to copy the following text and paste it into the User Data field so it’ll be run as a script when the instance boots. The first line tells Linux that the lines that follow should be executed as commands. The first command will install the Apache web server package, and the next one will fire up the Apache process:
!/bin/bash
yum install httpd -y
systemctl start httpd
Choose the Next: Add Storage button and, when you’re satisfied with the default (8 GB) storage volume you’re shown, choose Next: Add Tags. You won’t need to add any tags for this demo, so choose the Next: Configure Security Group button.
Since the plan is to configure your instance as a web server, you’ll need to choose Add Rule to add a new security group rule to permit HTTP traffic into your instance. Choose the Type drop-down button in your new rule, and select HTTP (not HTTPS—encrypted access won’t be necessary for this demo). Note how the Port Range setting is automatically populated with 80—the default port used for HTTP browser access. Note also how the value of Source is 0.0.0.0/0, ::/0. Those will permit access to your web server from any location using either Internet Protocol: IPv4 or IPv6.
Once you’ve reviewed your settings and chose the Launch button, you’ll be prompted to select an existing authentication key pair. You can create a new pair and download it to your local computer if you like, but you won’t need to access the instance through the Secure Shell (SSH) protocol for this demo. Otherwise, acknowledge the consequences of launching an instance without a key pair (something that would normally be a bit crazy), and go ahead with the launch.
The blue View Instances button at the bottom of the confirmation screen will take you to the EC2 Instances Dashboard where you should see your instance status. When the Instance State indicator turns green and the word running appears next to it, your web server should be live.
Making sure this instance is selected, find the IPv4 Public IP entry on the Description tab in the bottom half of the screen. Hover your mouse over the IP address that’s listed there, and choose the Copy To Clipboard icon to its right. Open a new tab in your browser, and paste the IP address into the URL field. You should see the default Apache test page.
When you’re done admiring your handiwork, you can shut down the instance from the Actions menu at the top of the Instances page. With your instance selected, choose Action, then Instance State, and finally Terminate. When you confirm the action, your instance will be shut down, and you won’t be billed any further. If your account is still in its first year and you haven’t been running similar instances for more than 750 hours this month, this Free Tier instance won’t have cost you anything anyway.
Simplified Deployments Through Managed Services
Building and administrating software applications can be complex wherever you deploy them. Whether they’re on-premises or in the cloud, you’ll face a lot of moving parts existing in a universe where they all have to play nicely together or the whole thing can collapse. To help lower the bar for entry into the cloud, some AWS services will handle much of the underlying infrastructure for you, allowing you to focus on your application needs. The benefits of a managed service are sometimes offset by premium pricing. But it’s often well worth it.

One important example of such a managed service is the Relational Database Service (RDS). RDS, as you’ll see in Chapter 9, “The Core Database Services,” lets you set the basic configuration parameters for the database engine of your choice, gives you an endpoint address through which your applications can connect to the database, and takes care of all the details invisibly. Besides being responsible for making top-level configuration decisions, you won’t need to worry about maintaining the database instance hosting the database, software updates, or data replication.

One step beyond a managed service—which handles only one part of your deployment stack for you—is a managed deployment, where the whole stack is taken care of behind the scenes. All you’ll need to make things work with one of these services is your application code or, if it’s a website you’re after, your content. Until Amazon figures out how to secretly listen in on your organization’s planning meetings and then automatically convert your ideas to code without you knowing, things are unlikely to get any simpler than this.

Two AWS services created with managed deployments in mind are Amazon Lightsail and AWS Elastic Beanstalk.

Amazon Lightsail
Lightsail is promoted as a low-stress way to enter the Amazon cloud world. It offers blueprints that, when launched, will automatically provision all the compute, storage, database, and network resources needed to make your deployment work. You set the pricing level you’re after (currently that’ll cost you somewhere between $3.50 and $160 USD each month) and add an optional script that will be run on your instance at startup, and AWS will take over. For context, $3.50 will get you 512 MB of memory, 1 vCPU, a 20 GB solid-state drive (SSD) storage volume, and 1 TB of transfers.

Lightsail uses all the same tools—such as the AMIs and instances you saw earlier in the chapter—to convert your plans to reality. Since it’s all AWS from top to bottom, you’re also covered should you later decide to move your stack directly to EC2, where you’ll have all the added access and flexibility standard to that platform.

Because things are packaged in blueprints, you won’t have the unlimited range of tools for your deployments that you’d get from EC2 itself. But, as you can see from these lists, there’s still a nice selection:

Operating systems: Amazon Linux, Ubuntu, Debian, FreeBSD, OpenSUSE, and Windows Server
Applications: WordPress, Magento, Drupal, Joomla, Redmine, and Plesk
Stacks: Node.js, GitLab, LAMP, MEAN, and Nginx
 In case you’re curious, a LAMP stack is a web server built on Linux, Apache, MySQL (or MariaDB), and PHP (or Python). By contrast, MEAN is a JavaScript stack for dynamic websites consisting of MongoDB, Express.js, AngularJS (or Angular), and Node.js.

AWS Elastic Beanstalk
If anything, Elastic Beanstalk is even simpler than Lightsail. All that’s expected from you is to define the application platform and then upload your code. That’s it. You can choose between preconfigured environments (including Go, .NET, Java Node.js, and PHP) and a number of Docker container environments. The “code” for Docker applications is defined with specially formatted Dockerrun.aws.json files.

One key difference between the two services is that while Lightsail bills at a flat rate (between $3.50 and $160 per month, as you saw), Beanstalk generates costs according to how resources are consumed. You don’t get to choose how many vCPUs or how much memory you will use. Instead, your application will scale its resource consumption according to demand. Should, say, your WordPress site go viral and attract millions of viewers one day, AWS will invisibly ramp up the infrastructure to meet demand. As demand falls, your infrastructure will similarly drop. Keep this in mind, as such variations in demand will determine how much you’ll be billed each month.

Deploying Container and Serverless Workloads
Even virtualized servers like EC2 instances tend to be resource-hungry. They do, after all, act like discrete, stand-alone machines running on top of a full-stack operating system. That means that having 5 or 10 of those virtual servers on a single physical host involves some serious duplication because each one will require its own OS kernel and device drivers.

Containers
Container technologies such as Docker avoid a lot of that overhead by allowing individual containers to share the Linux kernel with the physical host. They’re also able to share common elements (called layers) with other containers running on a single host. This makes Docker containers fast to load and execute and also lets you pack many more container workloads on a single hardware platform.

You’re always free to fire up one or more EC2 instances, install Docker, and use them to run as many containers as you’d like. But keeping all the bits and pieces talking to each other can get complicated. Instead, you can use either Amazon Elastic Container Service (ECS) or Amazon Elastic Container Service for Kubernetes (EKS) to orchestrate swarms of Docker containers on AWS using EC2 resources. Both of those services manage the underlying infrastructure for you, allowing you to ignore the messy details and concentrate on administrating Docker itself.

What’s the difference between ECS and EKS? Broadly speaking, they both have the same big-picture goals. But EKS gets there by using the popular open source Kubernetes orchestration tool. They are different paths to the same place.

Serverless Functions
The serverless computing model uses a resource footprint that’s even smaller than the one left by containers. Not only do serverless functions not require their own OS kernel, but they tend to spring into existence, perform some task, and then just as quickly die within minutes, if not seconds.

On the surface, Amazon’s serverless service—AWS Lambda—looks a bit like Elastic Beanstalk. You define your function by setting a runtime environment (like Node.js, .NET, or Python) and uploading the code you want the function to run. But, unlike Beanstalk, Lambda functions run only when triggered by a preset event. It could be a call from your mobile application, a change to a separate AWS resources (like an S3 bucket), or a log-based alert.

If an hour or a week passes without a trigger, Lambda won’t launch a function (and you won’t be billed anything). If there are a thousand concurrent executions, Lambda will scale automatically to meet the demand. Lambda functions are short-lived: they’ll time out after 15 minutes.

Summary
Configuring EC2 instances is designed to mirror the process of provisioning and launching on-premises servers. Instances are defined by your choice of AMIs, instance type, storage volumes, and pricing model.

AMIs are organized into four categories: Quick Start, custom (My AMIs), AWS Marketplace, and Community. You can create your own AMI from a snapshot based on the EBS volume of an EC2 instance.

EC2 instance types are designed to fit specific application demands, and individual optimizations are generally available in varying sizes.

EBS storage volumes can be encrypted and are more like physical hard drives in the flexibility of their usage. Instance store volumes are located on the same physical server hosting your instance and will, therefore, deliver faster performance.

EC2 on-demand pricing is best for short-term workloads that can’t be interrupted. Longer-term workloads—like ecommerce websites—will often be much less expensive when purchased as reserved instances. Spot instances work well for compute-intensive data operations that can survive unexpected shutdowns.

Lightsail, Elastic Beanstalk, Elastic Container Service, Elastic Container Service for Kubernetes, and Lambda are all designed to provide abstracted compute services that simplify, automate, and reduce the cost of compute operations.

Exam Essentials
Understand the elements required to provision an EC2 instance. An instance requires a base OS (AMI) and—optionally—an application stack, an instance type for its hardware profile, and either an EBS or an instance volume for storage.

Understand the sources, pricing, and availability of EC2 AMIs. The Quick Start and Marketplace AMIs are supported by Amazon or a recognized third-party vendor, which may not be true of AMIs selected from the Community collection. In any case, you should confirm whether using a particular AMI will incur extra charges beyond the normal EC2 usage.

Understand how EC2 instance types determine the compute power of your instance. Instance types are divided into type families, each of which focuses on a functional niche (general purpose, compute optimized, memory optimized, accelerated computing, and storage optimized). Your application needs and budget will determine which instance type you choose.

Understand the differences between EBS and instance store volumes. EBS volumes are versatile (they can, for instance, be converted into AMIs) and will survive an instance shutdown. Instance store volumes, on the other hand, provide faster reads and writes and can be more secure for some purposes. Which storage you use will often depend on the instance type you choose.

Understand the differences between EC2 pricing models. On-demand is the most expensive way to consume EC2 instances, but it’s also flexible and reliable (you control when an instance starts or stops). Reserved instances work well for instances that must remain running for longer periods of time. Spot instances are the least expensive but can be shut down with only a two-minute warning.

Be familiar with Amazon’s managed deployment services. Amazon Lightsail provides blueprints for simplified flat-rate deployments using EC2 resources under the hood. Lightsail deployments can, if needed, be transferred to regular EC2 infrastructure without service interruption. Elastic Beanstalk manages the underlying infrastructure for your application and automatically scales according to demand.

Understand how container and serverless models work in the cloud. Containers—like Docker—share the OS kernel and device drivers with their host and share common software layers with each other to produce fast and lightweight applications. ECS and EKS are AWS services focused on simplifying Docker orchestration within the EC2 framework. Lambda functions are designed to respond to event triggers to launch short-lived operations.

Review Questions
What is the function of an EC2 AMI?

To define the hardware profile used by an EC2 instance
To serve as an instance storage volume for high-volume data processing operations
To serve as a source image from which an instance’s primary storage volume is built
To define the way data streams are managed by EC2 instances
Where can you find a wide range of verified AMIs from both AWS and third-party vendors?

AWS Marketplace
Quick Start
Community AMIs
My AMIs
Which of the following could be included in an EC2 AMI? (Select TWO.)

A networking configuration
A software application stack
An operating system
An instance type definition
Which of the following are EC2 instance type families? (Select TWO.)

c5d.18xlarge
Compute optimized
t2.micro
Accelerated computing
When describing EC2 instance types, what is the role played by the vCPU metric?

vCPUs represent an instance’s potential resilience against external network demands.
vCPUs represent an instance type’s system memory compared to the class of memory modules on a physical machine.
vCPUs represent an AMI’s processing power compared to the number of processors on a physical machine.
vCPUs represent an instance type’s compute power compared to the number of processors on a physical machine.
Which of the following describes an EC2 dedicated instance?

An EC2 instance running on a physical host reserved for the exclusive use of a single AWS account
An EC2 instance running on a physical host reserved for and controlled by a single AWS account
An EC2 AMI that can be launched only on an instance within a single AWS account
An EC2 instance optimized for a particular compute role
Which of the following describes an EBS volume?

A software stack archive packaged to make it easy to copy and deploy to an EC2 instance
A virtualized partition of a physical storage drive that’s directly connected to the EC2 instance it’s associated with
A virtualized partition of a physical storage drive that’s not directly connected to the EC2 instance it’s associated with
A storage volume that’s encrypted for greater security
Why might you want to use an instance store volume with your EC2 instance rather than a volume from the more common EBS service? (Select TWO.)

Instance store volumes can be encrypted.
Instance store volumes, data will survive an instance shutdown.
Instance store volumes provide faster data read/write performance.
Instance store volumes are connected directly to your EC2 instance.
Your web application experiences periodic spikes in demand that require the provisioning of extra instances. Which of the following pricing models would make the most sense for those extra instances?

Spot
On-demand
Reserved
Dedicated
Your web application experiences periodic spikes in demand that require the provisioning of extra instances. Which of the following pricing models would make the most sense for the “base” instances that will run constantly?

Spot
On-demand
Spot fleet
Reserved
Which of the following best describes what happens when you purchase an EC2 reserved instance?

Charges for any instances you run matching the reserved instance type will be covered by the reservation.
Capacity matching the reserved definition will be guaranteed to be available whenever you request it.
Your account will immediately and automatically be billed for the full reservation amount.
An EC2 instance matching your reservation will automatically be launched in the selected AWS Region.
Which of the following use cases are good candidates for spot instances? (Select TWO.)

Big data processing workloads
Ecommerce websites
Continuous integration development environments
Long-term, highly available, content-rich websites
Which AWS services simplify the process of bringing web applications to deployment? (Select TWO.)

Elastic Block Store
Elastic Compute Cloud
Elastic Beanstalk
Lightsail
Which of the following services bills at a flat rate regardless of how it’s consumed?

Lightsail
Elastic Beanstalk
Elastic Compute Cloud
Relational Database Service
Which of these stacks are available from Lightsail blueprints? (Select TWO.)

Ubuntu
Gitlab
WordPress
LAMP
Which of these AWS services use primarily EC2 resources under the hood? (Select TWO.)

Elastic Block Store
Lightsail
Elastic Beanstalk
Relational Database Service
Which of the following AWS services are designed to let you deploy Docker containers? (Select TWO.)

Elastic Container Service
Lightsail
Elastic Beanstalk
Elastic Compute Cloud
Which of the following use container technologies? (Select TWO.)

Docker
Kubernetes
Lambda
Lightsail
What role can the Python programming language play in AWS Lambda?

Python cannot be used for Lambda.
It is the primary language for API calls to administrate Lambda remotely.
It is used as the underlying code driving the service.
It can be set as the runtime environment for a function.
What is the maximum time a Lambda function may run before timing out?

15 minutes
5 minutes
1 minute
1 hour