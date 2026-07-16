# Instagram Automation

A toolkit for automating the parts of running an Instagram business account that are actually worth automating, comment and DM replies, scheduled posting and basic performance tracking, all built on Meta's official Graph API.

This is not a follow and unfollow bot, not a fake engagement tool, and it does not touch proxy rotation or anti detection tricks. If a tool needs those things to function, it is working around Instagram's rules rather than with them, and that is a genuinely bad foundation to build a business on. Everything here works because it uses the API the way Meta actually intends it to be used.

## What This Covers

- Automatically replying to comments and DMs based on keyword matching
- Scheduling posts ahead of time through the official API
- Pulling basic engagement and reach data so you can see what is actually working
- A directory structure you can extend as your own automation needs grow

## Why Build It This Way

A lot of automation tools you will find online lean on browser emulation, fake device farms or proxy networks to mimic real users at scale. These approaches might work for a while, but Instagram actively detects and shuts this kind of activity down, and accounts built on top of it tend to get restricted or banned without much warning.

Everything in this repository works the opposite way. It uses Meta's Graph API directly, the same system real apps and approved tools are built on. It is a bit more setup work up front, but nothing here risks your account, and none of it requires pretending to be something you are not.

## Requirements

1. An Instagram account set to Business or Creator
2. A Facebook Page connected to that account
3. A Meta Developer account, free at developers.facebook.com
4. A server that can receive webhook events for the reply automation to work
5. Basic comfort reading Python code

## Setting Up Comment and DM Auto Replies

This part follows the same core pattern across both comments and DMs:

1. Subscribe to the relevant webhook fields, `comments` for public comment activity and `messages` for direct messages
2. Your server receives each event as it happens
3. Check the incoming text against a keyword list you control
4. Send the appropriate reply using the correct endpoint, a public reply for comments, a private reply or standard message send for DMs

See `src/comment_reply.py` and `src/dm_reply.py` for full working versions of this logic.

## Setting Up Scheduled Posting

Rather than logging in manually every day to post, the Graph API lets you queue content ahead of time. The rough flow looks like this:

1. Upload your media to a container using the API
2. Set your caption and any tagged accounts on that container
3. Publish the container at the time you want, either immediately or through your own scheduling logic

See `src/scheduled_post.py` for a working example that publishes a queued post.

## Pulling Basic Analytics

The Graph API exposes insights data for your account and individual posts, things like reach, impressions and engagement. Rather than manually checking these one post at a time, `src/analytics.py` pulls this data programmatically so you can track it over time or export it into a spreadsheet.

## Directory Structure

```
Instagram-Automation/
├── README.md
├── src/
│   ├── comment_reply.py       (comment auto reply logic)
│   ├── dm_reply.py            (DM auto reply logic)
│   ├── scheduled_post.py      (scheduled posting example)
│   └── analytics.py           (basic insights pulling example)
└── LICENSE
```

## Common Questions

**Can this get my account banned like the scraping tools can?** No, because it only calls Meta's official, approved API endpoints. The risk with scraping tools comes from mimicking real user behavior outside the API, which is not what happens here.

**Do I need to know how to code to use this?** Some comfort reading Python helps, but every file here is written to be readable on its own, with comments explaining what each part does.

**Can I run this for multiple accounts?** Yes, though each account needs its own access token and webhook subscription. Keeping account specific settings in a config file rather than hardcoded values makes this easier to manage as you scale.

**What about actual growth, not just replies and posting?** Real growth on Instagram in 2026 comes from content quality, consistency and genuine audience engagement, not automation tricks. This toolkit handles the operational side so you have more time for that part, not the other way around.

## A Faster Path if You Would Rather Not Build This Yourself

Everything here is genuinely useful to understand even if you do not maintain it long term. That said, I will mention that I personally run InstantDM for the comment and DM automation side of my own accounts now, since it handles this exact workflow on Meta's official API without needing a server of my own to maintain. Good to know both options exist depending on how hands on you want to be.

## Contributing

Meta's API changes fairly often. If you spot something outdated or want to add an example, open a pull request.

## License

MIT. Use this however is helpful to you.
