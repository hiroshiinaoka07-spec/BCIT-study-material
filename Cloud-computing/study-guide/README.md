# 3640 Cloud Computing — Study Guide

A weekly guide built from the notes, textbook chapters, GitLab labs, and in-repo lab resources. Each week has learning objectives, a concept deep dive, a repository tour, practical takeaways, a 5-question quiz with a hidden answer key, and a 15-question multiple-choice quiz at the end.

Standalone practice quizzes (MC / short answer / scenario, with answer keys) live in [`../quizzes/`](../quizzes/).

| Week | Topic | Source files |
| ---- | ----- | ------------ |
| [Week 1](week-01-cloud-fundamentals.md) | Cloud fundamentals & your Linux workstation | `wk01.md`, `linux-environment.md` |
| [Week 2](week-02-iam-security.md) | Securing your AWS account with IAM | `chapter 5`, `transcripts/6.1 …`, `transcripts/6.2 …` |
| [Week 3](week-03-ec2-cloud-init.md) | Compute with EC2 & bootstrapping with cloud-init | `chapter 7.md`, `aws-ec2.md` |
| [Week 4](week-04-vpc-networking.md) | Networking with VPCs | `chpater10` (VPC section), `aws-vpc.md`, `assets/vpc-3640.png` |
| [Week 5](week-05-aws-cli-bash.md) | Automating AWS with the CLI & Bash | `aws-cli.md`, `aws-cli-exercise.md`, [GitLab: aws-cli-exercise-start](https://gitlab.com/cit_3640/aws-cli-exercise-start) |
| Week 6 | In-class test (weeks 1–5) | No new flipped material — use [`../quizzes/week_06_quiz.md`](../quizzes/week_06_quiz.md) |
| [Week 7](week-07-aws-storage.md) | AWS storage services: S3, EBS & EFS | `chapter10-week7`, `aws-storage-services.md`, [GitLab: aws-cli-efs-exercise](https://gitlab.com/cit_3640/aws-cli-efs-exercise), [GitLab: aws-cli-s3-exercise](https://gitlab.com/cit_3640/aws-cli-s3-exercise) |
| Week 8 | Midterm (1 hour) | Tue Oct 27, 14:00–15:00, DTC-825 — [`../quizzes/final_comprehensive_review.md`](../quizzes/final_comprehensive_review.md). **No Chapter 5 / IAM theory.** Week 5 Bash (heredoc, `$( )`, lab `if`s) is in. |

Weeks 9–14 (load balancing / auto scaling, DNS, DynamoDB, OpenTofu) are on the course schedule but have no materials in this repo yet.

## How to use this guide

1. Read the source files listed for the week first (this mirrors the course's flipped-classroom setup in `README.md`).
2. Work through the guide's deep dive with the source file open beside it.
3. Take the in-guide quiz **before** opening the answer key, then the standalone quiz in `quizzes/`.
4. Do the hands-on parts in your Linux environment and AWS account — and always log in as your IAM user, not root.

> **Cost reminder:** terminate EC2 instances, delete unused EFS file systems and S3 buckets, and release Elastic IPs when you finish a lab. Idle resources can still bill you.
