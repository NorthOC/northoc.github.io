# Road to 5 million: the stack (part 3)

## Context

In the previous one, I picked a problem to solve and what business would fit my criteria. This post is about programming details

## Picking the medium

I am a programmer, so I get to code my rental friend platform from scratch.

That means I have to decide on a couple of things - but the first one is definitely the medium, through which people will use my solution. 

Software, Website or Phone app? 

And the only choice I would ever pick in the current market is obvious: Website.

Why? Because you do not need to get approval from le Google or the Apple Corp. for uploading it to the official store. 

Host it, get a domain and you're good to go. This means that I will retain maximum control over my project.

Another reason is that I only need to worry about my rental friend platform being responsive, for it to work both on computers and phones, instead of worrying about handling operating system versions. Again, less headaches.

## Front-end + Back-end + Database

Every realistic business on the internet has to choose these things. It is the minimal standard for a site to be functional, and is called the stack.

So what is a stack? It is a combination of technologies, set up in a way that lets you code things faster.

So how do you choose a stack? Well, from experience, the best choice is to use what you know.

In my case, I know Django. It's a full-stack framework (containing front-end, back-end and database technologies) which has a lot of features already implemented for you, like security measures, user models, sessions, templating, etc. On top of that, to make the website more interactive and modern, I will use the Django Rest Framework and cook up an API for editing a profile. 

At some point, I might slap Redis in there, to cache commonly retrieved database records and reduce loading times. This will be my back-end architecture. 

Django also comes with a sqlite database. This lets me store various information like User profiles, Order history, payments/withdrawals, etc. But sqlite is more for development than production, so I will choose PostgreSQL. Any database is fine, but I chose this one because the I can use it for my business for free.

For the front-end I plan to use Django templates + HTMX. Why not a front-end framework like React? Because I am not coding a single-page application like Google Sheets, Photopea, etc. And, anyways, coding with React, for me, feels like torture lol.

![my stack](/static/images/biz-series/the_stack.png)

* **Front-end: Django Templates + HTMX**
* **Back-end: Django + Django REST framework**
* **Database: PostgreSQL**

Apart from that, I will need a payment processor. I've got a Stripe account, but I will probably choose either Paysera, SEB payments or Montonio, because these platforms support Lithuanian bank transfers. We'll see.

The next part will be about visual design. 

Stay tuned.